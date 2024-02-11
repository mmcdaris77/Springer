from typing import Callable
from datetime import date
from .LineOfTherapy import LineOfTherapy, Drug


#rules: 
class FactLotNextDrugs():
    def __init__(self, lot: LineOfTherapy, next_drugs: list[Drug]):
        self.lot: LineOfTherapy = lot 
        self.next_drugs: list[Drug] = next_drugs

    def gap(self, allowable_gap=90) -> bool:
        '''return False is min new drugs start date is beyond the allowable gap'''
        start_dtd: date = self.lot.end
        end_dtd: date = min(self.next_drugs, key=lambda x:x.start_dt).start_dt
        return 0 <= (end_dtd - start_dtd).days < allowable_gap
    
    def within_init(self, allowable_gap=28) -> bool:
        '''return Flase if the new drugs are beyond the init range'''
        start_dtd: date = self.lot.start
        end_dtd: date = min(self.next_drugs, key=lambda x:x.start_dt).start_dt
        return 0 <= (end_dtd - start_dtd).days < allowable_gap
    
    def chk_new_drugs(self, lot_rules: dict) -> bool: 
        '''return False if new drugs were added and are not in an exception'''
        for d in self.next_drugs:
            if d not in [x.drug_name for x in self.lot.drugs]:
                return False
    
    def chk_drug_drops(self, lot_rules: dict) -> bool: 
        '''return False if drugs were dropped and are not in an exception'''
        for d in [x.drug_name for x in self.lot.drugs]:
            if d not in self.next_drugs:
                return False
            
    def is_mono_therapy(self) -> bool:
        return self.lot.is_mono_therapy()
    
    def new_drugs_contains(self, drugs: list[str]) -> bool: 
        for d in self.next_drugs:
            if d.drug_name in drugs:
                return True 
        return False


class LotCondition():
    def __init__(self, name: str, eval_func: Callable[[FactLotNextDrugs], bool]): 
        self.name = name
        self.eval_func = eval_func 

    def evaluation(self, fact: FactLotNextDrugs) -> bool:
        return self.eval_func(fact)


class LotAction():
    def __init__(self, name: str, exec_func: Callable[[FactLotNextDrugs], None]):
        self.name = name
        self.exec_func = exec_func 

    def execute(self, fact: FactLotNextDrugs) -> None:
        self.exec_func(fact)


class LotRule():
    def __init__(self, name: str,  
                 conditions: list[LotCondition], 
                 true_actions: list[LotAction], 
                 false_actions: list[LotAction] = None, 
                 any_actions: list[LotAction] = None):
        
        self.conditions = conditions
        self.true_actions = true_actions
        self.false_action = false_actions
        self.any_actions = any_actions
        self.name = name

    def add_condition(self, condition: LotCondition) -> None:
        self.conditions.append(condition)

    def add_true_action(self, action: LotAction) -> None:
        self.true_actions.append(action)

    def add_false_action(self, action: LotAction) -> None:
        self.false_action.append(action)

    def add_any_actions(self, action: LotAction) -> None:
        self.any_actions.append(action)

    def evaluate(self, fact: FactLotNextDrugs):
        def fact_generator(conditions: list[LotCondition], fact: FactLotNextDrugs):
            results = [condition.eval_func(fact) for condition in conditions]

            if all(results):
                return 'all', fact
            elif any(results):
                return 'any', fact
            else:
                return 'none', fact

        true_state, true_fact = fact_generator(self.conditions, fact)

        print(f'RuleName: {self.name}......... true_state: {true_state}')
        if not true_fact is None:
            if true_state == 'all' and not self.true_actions is None:
                for action in self.true_actions:
                    action.exec_func(fact)
                return True
            else:
                if true_state != 'all' and not self.false_action is None:
                    for action in self.false_action:
                        action.exec_func(fact)
                    return True
                if true_state == 'any' and not self.any_actions is None:
                    for action in self.any_actions:
                        action.exec_func(fact)
                    return True