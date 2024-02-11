
### This is an example of a rules engine to generate Lines Of Therapy from drug data. 
The idea is to make something that can be configurable for different variations. 


### Features
- lot_rules configuration
    - the lot_rules json in gen_lots_run.py is an example.  This may be changed to yaml.
- deafult rules:
    - init days - a window where all drugs are added to the LOT initially
    - allowable_gap - a gap window between the current LOT end date and the next drugs
    - drug drops - advance to next lot number
    - drug add - advance to next lot number


### Future
- add end date features
    - use drug end date can cause ovelapping LOT start/end dates
- add drug class and drug type
- add drug list to rules class to make rules beyond just next_drugs
- next_drugs should be able to get more than just next date 
    - ex: all dates in first init_days
    - ex: all dates after init_days where no gap and no drop/adds
- change lot_rules to yaml and formalize
    - add the rule_groups
    - fix get_conditions() to do more... 