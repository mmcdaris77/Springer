from typing import Callable
from datetime import date
import logging
from .LineOfTherapy import LineOfTherapy, Drug

logger = logging.getLogger('lot_logger')

#rules: 
class FactLotNextDrugs():
    def __init__(self, lot: LineOfTherapy, next_drugs: list[Drug]):
        self.lot: LineOfTherapy = lot 
        self.next_drugs: list[Drug] = next_drugs

    def is_past_allowable_gap(self, allowable_gap=90) -> bool:
        '''return False is min new drugs start date is beyond the allowable gap'''
        start_dtd: date = self.lot.end
        end_dtd: date = min(self.next_drugs, key=lambda x:x.start_dt).start_dt
        logger.debug(f'is_past_allowable_gap: {allowable_gap}: {(end_dtd - start_dtd).days > allowable_gap}')
        return (end_dtd - start_dtd).days > allowable_gap

    def is_within_allowable_gap(self, allowable_gap=90) -> bool:
        '''return True is min new drugs start date is within allowable gap'''
        start_dtd: date = self.lot.end
        end_dtd: date = min(self.next_drugs, key=lambda x:x.start_dt).start_dt
        logger.debug(f'is_within_allowable_gap: {allowable_gap}: {0 <= (end_dtd - start_dtd).days < allowable_gap}')
        return 0 <= (end_dtd - start_dtd).days < allowable_gap
    
    def is_within_init_range(self, allowable_gap=28) -> bool:
        '''return Flase if the new drugs are beyond the init range'''
        start_dtd: date = self.lot.start
        end_dtd: date = min(self.next_drugs, key=lambda x:x.start_dt).start_dt
        return 0 <= (end_dtd - start_dtd).days < allowable_gap
    
    def has_drug_additions(self, lot_rules: dict, allowable_gap:int = 0) -> bool: 
        '''return True if new drugs were added and are not in an exception'''
        rtn = False
        for d in self.next_drugs:
            if d not in [x.drug_name for x in self.lot.drugs] and self.is_past_allowable_gap(allowable_gap):
                rtn = True
        logger.debug(f'has_drug_additions: {rtn}')
        return rtn
    
    def has_drug_drops(self, lot_rules: dict, allowable_gap:int = 0) -> bool: 
        '''return True if drugs were dropped and are not in an exception'''
        rtn = False
        for d in [x.drug_name for x in self.lot.drugs]:
            if d not in self.next_drugs and self.is_past_allowable_gap(allowable_gap):
                rtn = True
        logger.debug(f'has_drug_drops: {rtn}')
        return rtn
            
    def is_mono_therapy(self) -> bool:
        logger.debug(f'is_mono_therapy: {self.lot.is_mono_therapy()}')
        return self.lot.is_mono_therapy()
    
    def new_drugs_contains_drugs(self, drugs: list[str]) -> bool: 
        rtn = False
        for d in self.next_drugs:
            if d.drug_name in drugs:
                rtn = True 
        logger.debug(f'new_drugs_contains_drugs: {drugs}: {rtn}')
        return rtn
    
    def new_drugs_contains_drug_class(self, classes: list[str]) -> bool: 
        rtn = False
        for d in self.next_drugs:
            if d.drug_class in classes:
                rtn = True 
        logger.debug(f'new_drugs_contains_drug_class: {classes}: {rtn}')
        return rtn
    
    def regimen_contains_drug_class(self, classes: list[str]) -> bool: 
        rtn = False
        for d in [x.drug_class for x in self.lot.drugs]:
            if d in classes:
                rtn = True
        logger.debug(f'regimen_contains_drug_class: {rtn}')
        return rtn


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

        logger.debug(f'evaluate: RuleName: {self.name} ---> true_state: {true_state}')
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