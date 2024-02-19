import csv
import os
import datetime
from datetime import datetime
from LotGenerator.LineOfTherapy import Drug
from LotGenerator.LotGenerator import LotGenerator
from LotGenerator.LotRuleConfig import get_settings, LotRuleConfig
from LotGenerator.lot_logger import logger

logger = logger(log_debug=False)


def process_lots(person_list: list[str], drugs_list: list[Drug], lot_rules=LotRuleConfig()) -> list[LotGenerator]:
    # for each person generate lots and append them to the list
        # get patient drugs and load them in an instance of LotGenerator
    lots = []
    logger.info(f'Total persons to process: {len(person_list)}\nTotal drugs to process: {len(drugs_list)}')
    logger.info(f'{str(lot_rules)}')
    for person in person_list:
        person_drugs = [d for d in drugs_list if d.person_id == person]
        logger.debug(f'working on..... person: {person}....drug count: {len(person_drugs)}')
        #lot_generator = LotGenerator(person_id=person)
        lot_generator = LotGenerator(person_id=person, lot_rules=lot_rules)
        lot_generator.set_drug_list(person_drugs)

        lot_generator.generate()
        lots.append(lot_generator)

    return lots



if __name__ == '__main__':

    # prep some data from a test file... 
    me_dir = os.path.dirname(os.path.realpath(__file__))
    file_name = 'data/drug_exposure.csv'  
    a_file = os.path.join(me_dir, file_name)

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

    #############################################
    # process LOTs
    #############################################
    # get the lot rules configured in the lot_rule_settings folder yml files by the rule_set.name
    lot_rules = get_settings(rule_set_name='test')
    #lots = process_lots(person_list=person_list, drugs_list=drugs_list, lot_rules=None)
    lots = process_lots(person_list=person_list, drugs_list=drugs_list, lot_rules=lot_rules)

    # print out the last lot.. 
    # drugs: 
    print(lots[-1])
    # lots
    for lot in lots[-1].lots:
        print({'lot': lot.lot, 'start_date': str(lot.start), 'end_date': str(lot.end), 'regimen': lot.get_regimen()})
