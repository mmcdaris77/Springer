
### This is an example of a rules engine to generate Lines Of Therapy from drug data. 
The idea is to make something that can be configurable for different variations. 
- python verison 3.10


### Features
- lot_rules configuration
    - the lot_rule_settings folder can contain N .yml files.  Get configuration (lot_rules) by name.
- deafult rules:
    - init days - a window where all drugs are added to the LOT initially
    - allowable_gap - a gap window between the current LOT end date and the next drugs
    - drug drops - advance to next lot number
    - drug add - advance to next lot number

### Condition Functions
|Name|Args|Desc|
| ----------- | ----------- | ----------- |
| is_past_allowable_gap | allowable_gap: int <br>Optional(therapy_routes: list[str]) | returns True if min drug date in next_drugs is beyond the allowable gap, else False |
| is_within_allowable_gap | allowable_gap: int | returns True if min drug date in next_drugs is within the allowable gap, else False |
| has_drug_additions | swap_drugs: list[list[str]] | returns True if there are drugs in next_drugs that are not in the current LOT regimen and drugs are not mapped in a swap list, else False |
| has_drug_drops | n/a | returns True if there are drugs in the current LOT regimen that are not in next_drugs, else False |
| is_mono_therapy | n/a | returns True if the current LOT regimen contains only one drug, else False |
| new_drugs_contains_drugs | drugs: list[str] | returns True if next_drugs contains any drug from a list of drugs, else False |
| new_drugs_contains_drug_class | classes: list[str] | returns True if next_drugs contains any class from a list of classes, else False |
| regimen_contains_drug_class | classes: list[str] | returns True if current LOT regimen contains any class from a list of classes, else False |
| has_other_therapy_by_lot_start | therapy_name: str <br>days_before_lot_start: int <br>days_after_lot_start: int | returns True if there is an 'other thereapy' within the range |


### Action Functions
|Name|Args|Desc|
| ----------- | ----------- | ----------- |
| add_drugs_to_lot | n/a | add next_drugs to the current LOT |
| advance_lot | n/a | advance to the next LOT and init with the current next_drugs |
| set_maintenance_flag | n/a | set the maint_flag = True for the current LOT |
| advance_into_maintenance | n/a | advance to the next LOT and init with the current next_drugs and set maint_flag = True |
| do_nothing | n/a | go to the next rule |
| add_lot_flag_true | flag_name: str | add a lot flag = True |
| add_lot_flag_false | flag_name: str | add a lot flag = False |

### Future
- add end date features
    - use drug end date can cause ovelapping LOT start/end dates
- add drug_list to rules class to make rules beyond just next_drugs
- next_drugs should be able to get more than just next date 
    - ex: all dates in first init_days
    - ex: all dates after init_days where no gap and no drop/adds
- post process actions
    - by lot/regimen