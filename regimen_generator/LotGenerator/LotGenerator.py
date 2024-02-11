from datetime import date
from .LineOfTherapy import Drug, LineOfTherapy
from .LotRules import FactLotNextDrugs, LotCondition, LotAction, LotRule


INIT_DAYS = 28
ALLOWABLE_GAP = 90

class LotGenerator():
    def __init__(self, person_id: str, lot_rules: dict = None) -> None:
        self.person_id: str = person_id
        self.patient_drugs: list[Drug] = []
        self.drug_start_dates: list = []
        self.lot_number: int = 1
        self.lots: list[LineOfTherapy] = []
        self.lot_rules = lot_rules
        self.next_drugs: list[Drug]

    def get_conditions(self, fact_lot_next_drugs: FactLotNextDrugs):
        if 'gap_rules' in self.lot_rules.keys():

            conditions_list = []
            actions_list = []
            for rule in self.lot_rules['gap_rules']:
                for k, v in rule['conditions'].items():
                    if not hasattr(fact_lot_next_drugs, k):
                        print(f'condition function not found: {k}')
                    else:
                        func = (lambda k, v: lambda fact: getattr(fact_lot_next_drugs, k)(**v))(k, v)
                        conditions_list.append(LotCondition(v, func))

                for act in rule['actions']:
                    if not hasattr(self, act):
                        print(f'action function not found: {act}')
                    else:
                        if 'next_drugs' in rule['actions'][act].keys():
                            rule['actions'][act]['next_drugs'] = self.next_drugs
                        actions_list.append(LotAction(act, lambda fact: getattr(self, act)(**rule['actions'][act])))

        return conditions_list, actions_list

    def set_drug_list(self, drug_list: list[Drug]) -> None: 
        if len(drug_list) == 0:
            print('drug_list is empty.  nothing to do here')
            return None

        self.patient_drugs = sorted(drug_list, key=lambda d: d.start_dt) 
        self.drug_start_dates = sorted(list(set([x.start_dt for x in self.patient_drugs])))

    def generate(self) -> None: 
        iter_cnt = 0
        while len(self.drug_start_dates) > 0:
            self.next_drugs = []
            is_within_init_range = False
            start_date = self.get_next_date() 
            #print(f'\tIteration #: {iter_cnt} --> StartDate: {start_date}')
            iter_cnt+=1
            self.next_drugs = self.get_next_drugs(start_date)

            if self.get_current_lot() is None:
                self.lots.append(LineOfTherapy(self.lot_number, drugs=self.next_drugs))
                continue
            
            # if gap ok and drops ok and adds okay then add
            # else advance lot (flag maint?)

            #rules
            # set the fact (the current lot and the next set of drugs)
            fact_lot__next_drugs = FactLotNextDrugs(self.get_current_lot(), self.next_drugs)
            # create some actions to execute 
            action_merge_drugs = LotAction('merge drugs', lambda fact: self.add_drugs_to_lot(fact.next_drugs)) 
            action_in_init_range = LotAction('set is_within_init_range True', lambda is_within_init_range: True)
            action_advance_lot = LotAction('advance lot', lambda fact: self.advance_lot(self.next_drugs))

            # init days
            condition_init_days = LotCondition('Initital Drugs', lambda fact: fact.within_init(INIT_DAYS))
            init_rule = LotRule(
                name = 'init lot',
                conditions=[condition_init_days], 
                true_actions=[action_merge_drugs, action_in_init_range]
                )
            
            init_rule.evaluate(fact_lot__next_drugs)



            if not is_within_init_range:
                move_on = False
                cust_conditions, cust_actions = self.get_conditions(fact_lot__next_drugs)
                cust_rule = LotRule(
                    name='gap_rules',
                    conditions=cust_conditions,
                    true_actions=cust_actions
                )
                move_on = cust_rule.evaluate(fact_lot__next_drugs)
                if not move_on:
                    condition_gap = LotCondition('Gap Rule', lambda fact: fact.gap(ALLOWABLE_GAP))
                    condition_addions = LotCondition('Drug Adds', lambda fact: fact.chk_new_drugs(self.lot_rules))
                    condition_drops = LotCondition('Drug drops', lambda fact: fact.chk_drug_drops(self.lot_rules))
                    rules = LotRule(
                        name='def',
                        conditions=[condition_gap,condition_addions,condition_drops], 
                        true_actions=[action_merge_drugs], 
                        false_actions=[action_advance_lot]
                        )

                    rules.evaluate(fact_lot__next_drugs)

            print(self.get_current_lot())

            # remove date:
            for d in self.drug_start_dates:
                if start_date == d:
                    self.drug_start_dates.remove(d)

    def get_next_date(self): 
        return self.drug_start_dates.pop(0)

    def get_next_drugs(self, start_date: date) -> list[Drug]:
        next_drugs = []
        for drug in self.patient_drugs:
            if start_date == drug.start_dt:
                next_drugs.append(drug)

        return next_drugs

    def advance_lot(self, list_of_drugs: list[Drug]) -> None:
        self.lot_number += 1
        self.lots.append(LineOfTherapy(self.lot_number, drugs=list_of_drugs))
    
    def get_current_lot(self) -> LineOfTherapy:
        for lot in self.lots:
            if lot.lot == self.lot_number:
                return lot
        return None
    
    def add_drugs_to_lot(self, next_drugs) -> None:
        self.get_current_lot().add_drugs(next_drugs)

    def __str__(self) -> str:
        rtn = f'LotGenerator: person_id: {self.person_id}'
        for drug in self.patient_drugs:
            rtn += f'\n\t{drug}'
        return rtn