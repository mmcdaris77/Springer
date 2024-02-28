from typing import Callable
from datetime import date, timedelta
import logging
from .LineOfTherapy import LineOfTherapy, Drug, OtherTherapy

logger = logging.getLogger('lot_logger')

none_to_empty_str = lambda s: s or ''

#rules: 
class FactLotNextDrugs():
    def __init__(self, lot: LineOfTherapy, next_drugs: list[Drug], other_therapies: list[OtherTherapy] = []):
        self.lot: LineOfTherapy = lot 
        self.next_drugs: list[Drug] = next_drugs
        self.other_therapies: list[OtherTherapy] = other_therapies

    def is_past_allowable_gap(self, allowable_gap=90, therapy_routes: list[str] = []) -> bool:
        '''return False is min new drugs start date is beyond the allowable gap'''
        start_dtd: date = self.lot.end
        if len(therapy_routes) == 0:
            drugs_to_consider = self.next_drugs
        else:
            drugs_to_consider = self.__get_next_drugs_by_therapy_routes(therapy_routes)

        if len(drugs_to_consider) == 0:
            return False
        
        end_dtd: date = min(drugs_to_consider, key=lambda x:x.start_dt).start_dt
        logger.debug(f'is_past_allowable_gap:  allowable {allowable_gap}  actual: {(end_dtd - start_dtd).days}  response:{(end_dtd - start_dtd).days > allowable_gap}  therapy_routes: {therapy_routes}')
        return (end_dtd - start_dtd).days > allowable_gap

    def is_within_allowable_gap(self, allowable_gap=90) -> bool:
        '''return True if min new drugs start date is within allowable gap'''
        start_dtd: date = self.lot.end
        end_dtd: date = min(self.next_drugs, key=lambda x:x.start_dt).start_dt
        logger.debug(f'is_within_allowable_gap: {allowable_gap}: {0 <= allowable_gap <= (end_dtd - start_dtd).days}')
        return 0 <= allowable_gap <= (end_dtd - start_dtd).days
    
    
    def is_within_init_range(self, allowable_gap=28) -> bool:
        '''return Flase if the new drugs are beyond the init range'''
        start_dtd: date = self.lot.start
        end_dtd: date = min(self.next_drugs, key=lambda x:x.start_dt).start_dt
        return 0 <= (end_dtd - start_dtd).days < allowable_gap
    
    def has_drug_additions(self, swap_drugs: list[list[str]] = []) -> bool: 
        '''return True if new drugs were added and are not in an exception'''

        drug_results = []
        for d in self.next_drugs:
            # if not in lot and not swappable then it is True that its an addition
            if d.drug_name.lower() not in [x.drug_name.lower() for x in self.lot.drugs] \
                and not self.__is_swappable(d.drug_name.lower(), swap_drugs):
                drug_results.append(True)
            else: 
                drug_results.append(False)

        rtn = any(drug_results)
        logger.debug(f'has_drug_additions: {rtn}   swap_drugs: {swap_drugs}')
        logger.debug(f'............ next_drugs: {[x.drug_name.lower() for x in self.next_drugs]}       regimen: {self.lot.get_regimen()}')
        logger.debug(f'............ {drug_results}')
        return rtn
    
    def __is_swappable(self, drug_name: str, swap_list: list[list[str]]) -> bool:
        
        def get_swap_list(new_drug: str) -> list[str]: 
            for i in swap_list:
                if new_drug.lower() in [x.lower() for x in i]:
                    return i
            return []
        
        swap_drugs = get_swap_list(drug_name)
        # if there aren't any swappable drugs then just return true
        if len(swap_drugs) == 0:
            return False
        
        for drug in self.lot.get_regimen():
            if drug.lower() in [x.lower() for x in swap_drugs]:
                return True
        return False

    
    def has_drug_drops(self) -> bool: 
        '''return True if drugs were dropped and are not in an exception'''
        rtn = False
        for d in [x.drug_name for x in self.lot.drugs]:
            if d not in [x.drug_name for x in self.next_drugs]:
                rtn = True
        logger.debug(f'has_drug_drops: {rtn}')
        return rtn
            
    def is_mono_therapy(self) -> bool:
        logger.debug(f'is_mono_therapy: {self.lot.is_mono_therapy()}')
        return self.lot.is_mono_therapy()
            
    def is_combo_therapy(self) -> bool:
        logger.debug(f'is_combo_therapy: {not self.lot.is_mono_therapy()}')
        return not self.lot.is_mono_therapy()
    
    def new_drugs_contains_drugs(self, drugs: list[str]) -> bool: 
        rtn = False
        for d in self.next_drugs:
            if d.drug_name in drugs:
                rtn = True 
        logger.debug(f'new_drugs_contains_drugs: {drugs}: {rtn}')
        return rtn
    
    def new_drugs_contains_therapy_route(self, routes: list[str]) -> bool: 
        rtn = False
        for d in self.next_drugs:
            if d.therapy_route in routes:
                rtn = True 
        logger.debug(f'new_drugs_contains_therapy_route: {routes}: {rtn}')
        return rtn
    
    def new_drugs_contains_drug_class(self, drug_classs: list[str]) -> bool: 
        rtn = False
        for d in self.next_drugs:
            if d.drug_class in drug_classs:
                rtn = True 
        logger.debug(f'new_drugs_contains_drug_class: {drug_classs}: {rtn}')
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

    def regimen_contains_therapy_route(self, therapy_route: list[str]) -> bool: 
        for drug in self.lot.drugs:
            if drug.therapy_route.lower() in [x.lower() for x in therapy_route]:
                return True 
        return False
    
    def regimen_contains_any_drug(self, drugs: list[str]) -> bool: 
        for drug in self.lot.drugs:
            if drug.drug_name.lower() in [x.lower() for x in drugs]: 
                return True
        return False
    
    def has_other_therapy_by_lot_start(self, therapy_name: str, days_before_lot_start: int, days_after_lot_start: int) -> bool:
        if days_before_lot_start < 0:
            days_before_lot_start = days_before_lot_start * -1
        _lower_dt = self.lot.start - timedelta(days=days_before_lot_start)
        _upper_dt = self.lot.start + timedelta(days=days_after_lot_start)

        for t in self.other_therapies:
            if t.therapy_name.lower() == therapy_name.lower():
                if _lower_dt <= t.start_dt <= _upper_dt:
                    return True
        return False
    
    def has_other_therapy_by_lot_end(self, therapy_name: str, days_before_lot_end: int, days_after_lot_end: int) -> bool:
        if days_before_lot_end < 0:
            days_before_lot_end = days_before_lot_end * -1
        _lower_dt = self.lot.end - timedelta(days=days_before_lot_end)
        _upper_dt = self.lot.end + timedelta(days=days_after_lot_end)

        for t in self.other_therapies:
            if t.therapy_name.lower() == therapy_name.lower():
                if _lower_dt <= t.start_dt <= _upper_dt:
                    return True
        return False
    
    def has_other_therapy_within_lot(self, therapy_name: str) -> bool:
        for t in self.other_therapies:
            if t.therapy_name.lower() == therapy_name.lower() and self.lot.start < t.start_dt < self.lot.end:
                return True 
        return False 
    



    def __get_new_drugs(self):
        new_drugs_not_in_regimen = []
        for d in self.next_drugs:
            if not d in self.lot.get_regimen():
                new_drugs_not_in_regimen.append(d.drug_name)
        return new_drugs_not_in_regimen
    
    def __get_next_drugs_by_therapy_routes(self, therapy_routes: list[str] = []) -> list[Drug]:
        return [x for x in self.next_drugs if x.therapy_route.upper() in [rt.upper() for rt in therapy_routes]]



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
            #rule_conditions = ' ~ '.join([c.name for c in conditions])
            #print(rule_conditions)

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