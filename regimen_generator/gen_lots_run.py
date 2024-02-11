import csv
import os
import datetime
from datetime import datetime
from LotGenerator.LineOfTherapy import Drug
from LotGenerator.LotGenerator import LotGenerator

me_dir = os.path.dirname(os.path.realpath(__file__))
file_name = 'data/drug_exposure.csv'  
a_file = os.path.join(me_dir, file_name)

lot_rules = {
        'gap_rules': [
            {
                'conditions': {
                    'is_mono_therapy': {}, 
                    'new_drugs_contains': {'drugs': ['40213227']},
                    'gap': {'allowable_gap': 5000}
                },
                'actions': {
                    'add_drugs_to_lot': {'next_drugs': 'self.next_drugs'}
                }
            }
        ],
        'addition_rules': [
            {
                'add_rule_1': {
                'is_mono_therapy': True, 
                'new_drug_contains': {'drugs': ['40213227', '40213228'], 'required_cnt': 1},
                'allowable_gap': 180
                }
            }
        ],
        'drop_rules': [
            {
                'drop_rule_2': {
                    'is_mono_therapy': False
                }
            }
        ],
        'maintenance_rules': [
            {
                'maint_rule_1': {
                    'drug_drop': {}
                }
            }
        ]
}


# get some data from a csv of synth omop.drug_exposure
# into a list of Drug class types
drugs_list = []
person_list = []
with open(a_file, 'r') as f:
    reader = csv.DictReader(f)

    for row in reader:
        if int(row['drug_concept_id']) > 0:
            if row['person_id'] not in person_list:
                person_list.append(row['person_id'])
            drugs_list.append(Drug(
                person_id=row['person_id'],
                drug_name=row['drug_concept_id'],
                start_dt=datetime.strptime(row['drug_exposure_start_date'], '%Y-%m-%d').date()
            ))

# for each person generate lots and append them to the list
    # get patient drugs and load them in an instance of LotGenerator
lots = []
print(f'Total persons to process: {len(person_list)}\nTotal drugs to process: {len(drugs_list)}')
for idx, person in enumerate(person_list):
    if person == '1127':
    #if 1==1':
        person_drugs = [d for d in drugs_list if d.person_id == person]
        print(f'working on..... person: {person}....drug count: {len(person_drugs)}')
        lot_generator = LotGenerator(person_id=person, lot_rules=lot_rules)
        lot_generator.set_drug_list(person_drugs)

        print(lot_generator)

        lot_generator.generate()
        lots.append(lot_generator)

        for lot in lot_generator.lots:
            print(lot)


