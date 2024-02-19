import yaml
import os
import glob 
import json
from schema import Schema, Optional, And
import logging
from .LotRules import LotCondition, LotAction

logger = logging.getLogger('lot_logger')

me_dir = os.path.dirname(os.path.realpath(__file__))
RULE_SETTINGS_PATH = os.path.join(os.path.dirname(me_dir), 'lot_rule_settings')

RULE_TYPES = ['gap_rules', 'addition_rules', 'drop_rules']

'''
    get named configureations from a relitive path
    files need to be .yml and adheare to schema
    different configurations can be in different files or combined
'''

class Setting:
    def __init__(self, func_name: str, func_args: dict) -> None:
        self.func_name = func_name
        self.func_args = self.get_arg(func_args)

    def get_arg(self, func_args: dict):
        if func_args is None:
            return {}
        else: 
            return func_args
        
    def get_configured_setting(self, obj: any):
        if not hasattr(obj, self.func_name):
            logger.error(f'obj_type: {type(obj)} --> function not found: {self.func_name}')
        else:
            func = (lambda k, v: lambda fact: getattr(obj, self.func_name)(**self.func_args))(self.func_name, self.func_args)
            return f'{self.func_name} : {self.func_args}', func

        
    def __str__(self) -> str:
        return f'func: {self.func_name}......args: {self.func_args}'

class RuleSetting:
    def __init__(self, name: str, priority: int, conditions: list[dict], actions: list[dict]) -> None:
        self.name = name
        self.priority = priority
        self.conditions: list[Setting] = self.get_setting(conditions)
        self.actions: list[Setting] = self.get_setting(actions)

    def get_setting(self, settings: list[dict]) -> list[Setting]:
        rtn = []
        for d in settings:
            for k, v in d.items():
                rtn.append(Setting(k, v))
        return rtn
    
    def get_configured_conditions(self, obj): 
        cons = []
        for c in self.conditions:
            f_args, func = c.get_configured_setting(obj)
            cons.append(LotCondition(f_args, func))
        return cons
    
    def get_configured_actions(self, obj): 
        acts = []
        for a in self.actions:
            f_args, func = a.get_configured_setting(obj)
            acts.append(LotAction(f_args, func))
        return acts


    def __str__(self) -> str:
        rtn = f'\n\t\tRuleSetting.name: {self.name} \
                 \n\t\tRuleSetting.conditions:'
        for c in self.conditions:
            rtn += f'\n\t\t\t{c}'
        
        rtn += f'\n\t\tRuleSetting.actions:'
        for c in self.actions:
            rtn += f'\n\t\t\t{c}'

        return rtn

class LotRuleConfig:
    def __init__(self) -> None:
        self.init_days: int = 28
        self.allowable_drug_gap = 80
        self.gap_rules: list[RuleSetting] = []
        self.addition_rules: list[RuleSetting] = []
        self.drop_rules: list[RuleSetting] = []
        

    def get_rules_by_type(self, rule_type: str) -> list[dict]:
        if rule_type not in RULE_TYPES:
            logger.error(f'"{rule_type}" is not a valid rule_type')
            return None
        
        return sorted(getattr(self, rule_type), key=lambda r: r.priority) 
    
    def __str__(self) -> str:
        rtn = f'LotRuleConfig: '
        rtn += f'\n\tinit_days: {self.init_days}'
        rtn += f'\n\allowable_drug_gap: {self.allowable_drug_gap}'
        rtn += f'\n\tLotRuleConfig.gap_rules'
        for i in self.gap_rules:
            rtn += f'{i}'
        rtn += f'\n\tLotRuleConfig.addition_rules'
        for i in self.addition_rules:
            rtn += f'{i}'
        rtn += f'\n\tLotRuleConfig.drop_rules'
        for i in self.drop_rules:
            rtn += f'{i}'
        return rtn
    

def validate_schema(rule_set_name: str, data: dict) -> dict:
    logger.info("validating yml configuration")

    CONDITIONS_DEFS = [
        Schema({'regimen_contains_drug_class': {'classes': list[str]}}), 
        Schema({'new_drugs_contains_drug_class': {'classes': list[str]}}), 
        Schema({'new_drugs_contains_drugs': {'drugs': list[str]}}), 
        Schema({'is_mono_therapy': None}), 
        Schema({'has_drug_drops': None}), 
        Schema({'has_drug_additions': {Optional('swap_drugs'): list[list[str]]}}), 
        Schema({'is_within_allowable_gap': {'allowable_gap': int}}), 
        Schema({'is_past_allowable_gap': {'allowable_gap': int, Optional('therapy_routes'): list[str]}}),
        Schema({'has_other_therapy_by_lot_start': {'therapy_name': str, 'days_before_lot_start': int, 'days_after_lot_start': int}})
    ]

    ACTION_DEFS = [
        Schema({'add_drugs_to_lot': None}),
        Schema({'advance_lot': None}),
        Schema({'set_maintenance_flag': None}),
        Schema({'advance_into_maintenance': None}),
        Schema({'do_nothing': None}),
        Schema({'add_lot_flag_true': {'flag_name': str}}),
        Schema({'add_lot_flag_false': {'flag_name': str}})
    ]


    valid_rule_set = lambda x: x in RULE_TYPES

    def get_func_args_msg(func_list: list[Schema]) -> str:
        msg = ''
        for x in func_list:
            f = list(x.schema.keys())[0]
            msg += f'\n\t{f}: ('
            val = x.schema[f]
            if isinstance(val, dict):
                for k, v in val.items():
                    msg += f'{str(k)} --> {str(v)}, '
                msg+=')'
            else:
                msg += f'{val})'
        return msg


    condition_error_msg = f'Invalid condition function def. Valid conditions include: {get_func_args_msg(CONDITIONS_DEFS)}\n'
    action_error_msg = f'Invalid action function def. Valid action include: {get_func_args_msg(ACTION_DEFS)}\n'
    error_msg = 'Invalid yml configuration. Valid rule_set names: \n\t{}\nThere may be more info below:\n'.format(',\n\t'.join(RULE_TYPES))


    config_schema = Schema(
        {
            Optional('version'): str, 
            'rule_sets': [ 
                {
                    'name': str, 
                    'init_days': int,
                    'allowable_drug_gap': int,
                    valid_rule_set: [
                        {
                            'name': str, 
                            'conditions': And(list, CONDITIONS_DEFS, error=condition_error_msg), 
                            'actions': And(list, ACTION_DEFS, error=action_error_msg)
                            }
                        ]
                    }
                ]
            }
            , error=error_msg
        )

    try:
        return config_schema.validate(data)
    except Exception as e:
        logger.error(json.dumps(data, indent=4))
        logger.error(f'ERROR validating the lot_rules yml configuration: {rule_set_name}s\n{e}')
        exit()


def get_settings(rule_set_name: str, config_path: str = RULE_SETTINGS_PATH) -> LotRuleConfig:
    for yml_file in glob.glob(os.path.join(config_path, '*.yml')):
        with open(yml_file, 'r') as f:
            data = yaml.safe_load(f)
            data = validate_schema(rule_set_name, data)

        for rule_set in data['rule_sets']:
            if rule_set['name'] == rule_set_name:
                generator_config = LotRuleConfig()
                generator_config.init_days = rule_set['init_days']
                generator_config.allowable_drug_gap = rule_set['allowable_drug_gap']
                for k, v in rule_set.items():

                    priority = 0
                    if k in RULE_TYPES:
                        for rule in rule_set[k]:
                            priority += 10
                            c = RuleSetting(rule['name'], priority, rule['conditions'], rule['actions'])
                            getattr(generator_config, k).append(c)
                return generator_config
    return None




