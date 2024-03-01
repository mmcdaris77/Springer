
### This is an example of a rules engine to generate Lines Of Therapy from drug data. 
The idea is to make something that can be configurable for different variations. 
- python verison 3.10


### Features
- lot_rules configuration
    - the lot_rule_settings folder can contain N .yml files.  Get configuration (lot_rules) by name.
- deafult rules:
    - init days - a window where all drugs are added to the LOT initially
    - allowable_gap - a gap window between the current LOT end date and the next drugs
    - configurable gap rules
    - drug drops - advance to next lot number
    - drug add - advance to next lot number
    - end date adjustment - before advancing to the next lot, set the current lot end date based on conditions and actions
    - on advancement - before advancing, and after end date adjustments, check conditions and exec actions on the current lot.

### Rule Evaluation Order
1. configured gap rules: **gap_rules**
2. drug additions: **addition_rules**
3. drug drops: **drop_rules**
4. default gap rules: **allowable_drug_gap**
5. lot advancement:
    1. end date adjustments: **end_date_rules**
    2. before lot advances: **on_advance_rules**

### Condition Functions
|Name|Args|Desc|
| ----------- | ----------- | ----------- |
| is_past_allowable_gap | allowable_gap: int <br>Optional(therapy_routes: list[str]) | returns True if min drug date in next_drugs is beyond the allowable gap, else False |
| is_within_allowable_gap | allowable_gap: int | returns True if min drug date in next_drugs is within the allowable gap, else False |
| has_drug_additions | swap_drugs: list[list[str]] | returns True if there are drugs in next_drugs that are not in the current LOT regimen and drugs are not mapped in a swap list, else False |
| has_drug_drops | n/a | returns True if there are drugs in the current LOT regimen that are not in next_drugs, else False |
| is_mono_therapy | n/a | returns True if the current LOT regimen contains only one drug, else False |
| is_combo_therapy | n/a | returns True if the current LOT regimen contains more than one drug, else False |
| new_drugs_contains_drugs | drugs: list[str] | returns True if next_drugs contains any drug from a list of drugs, else False |
| new_drugs_contains_drug_class | classes: list[str] | returns True if next_drugs contains any class from a list of classes, else False |
| regimen_contains_drug_class | classes: list[str] | returns True if current LOT regimen contains any class from a list of classes, else False |
| has_other_therapy_by_lot_start | therapy_name: str <br>days_before_lot_start: int <br>days_after_lot_start: int | returns True if there is an 'other thereapy' within the range |
| has_other_therapy_by_lot_end | therapy_name: str <br>days_before_lot_end: int <br>days_after_lot_end: int | returns True if there is an 'other thereapy' within the range around the lot end date.  Use with **on_advance_rules** after lot end adjustments |
| has_other_therapy_within_lot | therapy_name: str | returns True if there is an 'other thereapy' between the lot start and end date.  Use with **on_advance_rules** after lot end adjustments |
| regimen_contains_any_drug | drugs: list[str] | returns True if the current regimen contains any drugs in the list, else False |
| regimen_contains_therapy_route | therapy_route: list[str] | returns True if the current regimen contains any drugs with a therapy_route in the list, else False |
| is_in_lot | lots_list: list[int] | If the current lot is in the lots_list return True, else False |


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
| add_lot_flag_value | flag_name: str, flag_value: any | add a lot flag = value |
| adjust_lot_enddate | num_days: int | adjust lot end date + num_days or 1 day before next lot start.  Use for **end_date_rules**  |
| eval_next_regardless | n/a | for evaluation of next rule regardless of state.  This is good when more than on flag setting is needed on_advance |



### Future
- add drug_list to rules class to make rules beyond just next_drugs
- next_drugs should be able to get more than just next date 
    - ex: all dates in first init_days
    - ex: all dates after init_days where no gap and no drop/adds
- post process actions
    - by lot/regimen