import yaml
import os
import glob 
from .lot_logger import logger
from .LotRules import LotCondition, LotAction


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
            logger.error(f'pbj_type: {type(obj)} --> function not found: {self.func_name}')
        else:
            func = (lambda k, v: lambda fact: getattr(obj, self.func_name)(**self.func_args))(self.func_name, self.func_args)
            return self.func_args, func

        
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
        rtn += f'\n\tLotRuleConfig.gap_rules'
        for i in self.gap_rules:
            rtn += f'{i}'
        rtn += f'\n\tLotRuleConfig.addition_rules'
        for i in self.addition_rules:
            rtn += f'{i}'
        return rtn
    


def get_settings(rule_set_name: str, config_path: str = RULE_SETTINGS_PATH) -> LotRuleConfig:
    for yml_file in glob.glob(os.path.join(config_path, '*.yml')):
        with open(yml_file, 'r') as f:
            data = yaml.safe_load(f)

        for rule_set in data['rule_sets']:
            if rule_set['name'] == rule_set_name:
                generator_config = LotRuleConfig()
                for k, v in rule_set.items():
                    priority = 0
                    if k in RULE_TYPES:
                        for rule in rule_set[k]:
                            priority += 10
                            c = RuleSetting(rule['name'], priority, rule['conditions'], rule['actions'])
                            getattr(generator_config, k).append(c)
                return generator_config
    return None




