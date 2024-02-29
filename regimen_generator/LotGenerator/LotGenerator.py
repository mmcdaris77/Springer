from datetime import date
import logging
from .LineOfTherapy import Drug, LineOfTherapy, OtherTherapy
from .LotRules import FactLotNextDrugs, LotCondition, LotAction, LotRule
from .LotRuleConfig import LotRuleConfig
from datetime import datetime, timedelta

logger = logging.getLogger('lot_logger')

INIT_DAYS = 28
ALLOWABLE_GAP = 90

class LotGenerator():
    def __init__(self, person_id: str, lot_rules: LotRuleConfig) -> None:
        self.person_id: str = person_id
        self.patient_drugs: list[Drug] = []
        self.init_drug_days: int = INIT_DAYS
        self.allowable_drug_gap: int = ALLOWABLE_GAP
        self.drug_start_dates: list = []
        self.lot_number: int = 1
        self.lots: list[LineOfTherapy] = []
        self.lot_rules = self.set_lot_rules(lot_rules)
        self.next_drugs: list[Drug]
        self.other_therapies: list[OtherTherapy]

    def set_lot_rules(self, lot_rules: LotRuleConfig) -> LotRuleConfig:
        if not isinstance(lot_rules, LotRuleConfig):
            return LotRuleConfig()
        else: 
            self.init_drug_days = lot_rules.init_days
            self.allowable_drug_gap = lot_rules.allowable_drug_gap
            return lot_rules

    def set_drug_list(self, drug_list: list[Drug]) -> None: 
        if len(drug_list) == 0:
            logger.warning('drug_list is empty.  nothing to do here')
            return None

        self.patient_drugs = sorted(drug_list, key=lambda d: d.start_dt) 
        self.drug_start_dates = sorted(list(set([x.start_dt for x in self.patient_drugs])))

    def set_other_therapies_list(self, other_therapies: list[OtherTherapy]) -> None:
        self.other_therapies = sorted(other_therapies, key=lambda t: t.start_dt)

    def generate(self) -> None: 
        iter_cnt = 0
        while len(self.drug_start_dates) > 0:
            self.next_drugs = []
            is_is_within_init_range_range = False
            start_date = self.get_next_date() 
            logger.debug(f'\tIteration #: {iter_cnt} --> StartDate: {start_date}')
            iter_cnt+=1
            self.next_drugs = self.get_next_drugs(start_date)

            if self.get_current_lot() is None:
                self.lots.append(LineOfTherapy(self.lot_number, drugs=self.next_drugs))
                continue
            
            logger.debug(self.get_current_lot())

            # if gap ok and drops ok and adds okay then add
            # else advance lot (flag maint?)

            #rules
            # set the fact (the current lot and the next set of drugs)
            fact_lot__next_drugs = FactLotNextDrugs(self.get_current_lot(), self.next_drugs, other_therapies=self.other_therapies)
            # init drugs rules
            action_add_init_drugs = LotAction('merge drugs', lambda fact: self.add_drugs_to_lot()) 
            action_in_init_range = LotAction('set is_is_within_init_range_range True', lambda is_is_within_init_range_range: True)
            condition_init_days = LotCondition('Initital Drugs', lambda fact: fact.is_within_init_range(self.init_drug_days))
            init_rule = LotRule(
                name = 'init lot',
                conditions=[condition_init_days], 
                true_actions=[action_add_init_drugs, action_in_init_range]
                )
            init_rule.evaluate(fact_lot__next_drugs)


            if not is_is_within_init_range_range:
                '''
                    check for events [drops/adds/gaps]: if true then send to function to 
                    check for additional rules from a config
                '''
                # check gap overides first
                self.eval_rules('gap_rules', fact_lot__next_drugs, default_advance=False)

                # check for add/drop and pass to configured if true
                add_drug_condition = LotCondition('condition: drug_adds', lambda fact: fact.has_drug_additions())
                drop_drug_condition = LotCondition('condition: drug_drops', lambda fact: fact.has_drug_drops())
                add_drug_action = LotAction('action: drug_adds', lambda fact: self.eval_rules('addition_rules', fact_lot__next_drugs))
                drop_drug_action = LotAction('action: drug_drops', lambda fact: self.eval_rules('drop_rules', fact_lot__next_drugs))
                
                add_drug_rule = LotRule(
                    name='rule: drug_adds',
                    conditions=[add_drug_condition],
                    true_actions=[add_drug_action]
                )
                drop_drug_rule = LotRule(
                    name='rule: drug_drops',
                    conditions=[drop_drug_condition],
                    true_actions=[drop_drug_action]
                )

                add_drug_rule.evaluate(fact_lot__next_drugs)
                drop_drug_rule.evaluate(fact_lot__next_drugs)
                
                # default gaps
                gap_condition = LotCondition('condition: is_past_allowable_gap', lambda fact: fact.is_past_allowable_gap(self.allowable_drug_gap))
                gap_condition2 = LotCondition('condition: nex_drug_not_none', lambda fact: self.next_drugs is not None)
                gap_action = LotAction('action: is_past_allowable_gap', lambda fact: self.advance_lot())
                gap_rule = LotRule(
                    name='rule: is_past_allowable_gap',
                    conditions=[gap_condition, gap_condition2],
                    true_actions=[gap_action]
                    )
                gap_rule.evaluate(fact_lot__next_drugs)

                # if no rules then append
                if not self.next_drugs is None:
                    self.add_drugs_to_lot('no rule')

            # remove date:
            for d in self.drug_start_dates:
                if start_date == d:
                    self.drug_start_dates.remove(d)

        # check end date rules one last time
        self.eval_advance_rules('end_date_rules')
        self.eval_advance_rules('on_advance_rules')

    def get_next_date(self): 
        return self.drug_start_dates.pop(0)

    def get_next_drugs(self, start_date: date) -> list[Drug]:
        next_drugs = []
        for drug in self.patient_drugs:
            if start_date == drug.start_dt:
                next_drugs.append(drug)

        return next_drugs

    def set_maintenance_flag(self):
        self.get_current_lot().is_maint = True

    def advance_into_maintenance(self, msg: str = None):
        self.advance_lot(msg=msg)

    def do_nothing(self): 
        pass

    def advance_lot(self, msg: str = None) -> None:
        ############################################################################
        ## eval lot end rules
        ############################################################################
        self.get_current_lot().set_end_date()
        
        self.eval_advance_rules('end_date_rules')
        self.eval_advance_rules('on_advance_rules')

        self.lot_number += 1
        self.lots.append(LineOfTherapy(self.lot_number, drugs=self.next_drugs))
        self.next_drugs = None
    
    def get_current_lot(self) -> LineOfTherapy:
        for lot in self.lots:
            if lot.lot == self.lot_number:
                return lot
        return None
    
    def get_previous_lot(self) -> LineOfTherapy:
        for lot in self.lots:
            if lot.lot == self.lot_number - 1:
                return lot
        return None
    
    def add_drugs_to_lot(self, lot_rule: str = None) -> None:
        lot = self.get_current_lot()
        lot.add_drugs(self.next_drugs)
        lot.lot_rule = lot_rule
        self.next_drugs = None

    def add_lot_flag_true(self, flag_name: str) -> None:
        if not flag_name is None:
            self.get_current_lot().lot_flags[flag_name] = True

    def add_lot_flag_false(self, flag_name: str) -> None:
        if not flag_name is None:
            self.get_current_lot().lot_flags[flag_name] = False

    def add_lot_flag_value(self, flag_name: str, flag_value: object) -> None:
        if not flag_name is None:
            self.get_current_lot().lot_flags[flag_name] = flag_value

    def adjust_lot_enddate(self, num_days: int): 
        '''
            add up to num_days or the day prior to the next lot/drugs
        '''
        lot = self.get_current_lot()
        next_start = None
        if not self.next_drugs is None:
            next_start = min([x.start_dt for x in self.next_drugs])
        
        if len(self.drug_start_dates) > 0:
            lot.adjust_lot_end(num_days=num_days, next_lot_start=next_start)
        else:
            lot.adjust_lot_end(num_days=num_days)

    def eval_rules(self, rule_type: str, fact: FactLotNextDrugs, default_advance=True, msg: str = None) -> None:
        '''
            if there are not other rules to apply actions then 
            advance the lot
        '''
        if not self.next_drugs is None:
            rules = self.lot_rules.get_rules_by_type(rule_type)
            for rule in rules:            
                conditions = rule.get_configured_conditions(fact)
                actions = rule.get_configured_actions(self)
                lot_rule = LotRule(rule.name, conditions=conditions, true_actions=actions)

                if self.next_drugs is None: break
                logger.debug(f'eval configured rule: {rule_type}..... name: {rule.name}..... conditions_cnt: {len(lot_rule.conditions)}')
                lot_rule.evaluate(fact)

            if default_advance and not self.next_drugs is None:
                self.advance_lot(msg=msg)

    def eval_advance_rules(self, rule_type: str, msg: str = None) -> None:
        if len(self.drug_start_dates) == 0:
            next_drugs = []
        else: 
            next_drugs = self.get_next_drugs(self.drug_start_dates[0])

        fact = FactLotNextDrugs(self.get_current_lot(), next_drugs, other_therapies=self.other_therapies)

        for rule in self.lot_rules.get_rules_by_type(rule_type):
            conditions = rule.get_configured_conditions(fact)
            actions = rule.get_configured_actions(self)
            lot_rule = LotRule(rule.name, conditions=conditions, true_actions=actions)
            if lot_rule.evaluate(fact): break


    def __str__(self) -> str:
        rtn = f'LotGenerator: person_id: {self.person_id}'
        for drug in self.patient_drugs:
            rtn += f'\n\t{drug}'
        return rtn