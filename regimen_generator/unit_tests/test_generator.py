import sys
sys.path.append(".")

import unittest
from datetime import datetime, date
from LotGenerator.LotRuleConfig import get_settings
from LotGenerator.LineOfTherapy import Drug, OtherTherapy
from LotGenerator.LotGenerator import LotGenerator
from LotGenerator.lot_logger import logger
logger = logger('lot_logger')

h = '*'*100
logger.debug(f'\n{h}\n**** UNIT TESTS\n{h}')

def to_date(dt:str, pattern: str = '%Y-%m-%d') -> date:
    return datetime.strptime(dt, pattern).date()

drug_data = [
    {'name': 'drug_a', 'start_date': to_date('2019-02-10')},
    {'name': 'drug_b', 'start_date': to_date('2019-02-10')},
    {'name': 'drug_b', 'start_date': to_date('2019-05-10')},
    {'name': 'drug_b-abc', 'start_date': to_date('2019-06-10')},
    {'name': 'drug_b', 'start_date': to_date('2020-03-10')}
]

other_therapy_data = [
    {'name': 'surgery', 'event_date': to_date('2019-01-01')},
    {'name': 'SCT', 'event_date': to_date('2020-04-01')}
]

drugs_list = []
other_therapy_list = []

for drug in drug_data:
    drugs_list.append(Drug(
        person_id='1',
        drug_name=drug['name'],
        start_dt=drug['start_date']
    ))

for ot in other_therapy_data:
    other_therapy_list.append(
        OtherTherapy(
            person_id='1',
            therapy_name=ot['name'],
            start_dt=ot['event_date']
        )
    )

lot_rules = get_settings(rule_set_name='unit_test_1')
lot_generator = LotGenerator('1', lot_rules)
lot_generator.set_drug_list(drug_list=drugs_list)
lot_generator.set_other_therapies_list(other_therapies=other_therapy_list)


class TestLotGenerator(unittest.TestCase):

    def test_init(self):
        lot_rules = get_settings(rule_set_name='unit_test_1')
        lot_generator = LotGenerator('1', lot_rules)
        lot_generator.set_drug_list(drug_list=drugs_list)

        self.assertEquals(lot_generator.init_drug_days, 28)
        self.assertEquals(lot_generator.allowable_drug_gap, 80)

    
    def test_set_drug_list(self):
        lot_rules = get_settings(rule_set_name='unit_test_1')
        lot_generator = LotGenerator('1', lot_rules)
        lot_generator.set_drug_list(drug_list=drugs_list)

        self.assertEquals(lot_generator.drug_start_dates, [to_date('2019-02-10'), to_date('2019-05-10'), to_date('2019-06-10'), to_date('2020-03-10')])
        self.assertEquals(len(lot_generator.patient_drugs), 5)

    def test_set_other_therapies_list(self):
        lot_rules = get_settings(rule_set_name='unit_test_1')
        lot_generator = LotGenerator('1', lot_rules)
        lot_generator.set_other_therapies_list(other_therapies=other_therapy_list)

        self.assertEquals(len(lot_generator.other_therapies), 2)

    def test_get_next_date(self):
        lot_rules = get_settings(rule_set_name='unit_test_1')
        lot_generator = LotGenerator('1', lot_rules)
        lot_generator.set_drug_list(drug_list=drugs_list)

        self.assertEquals(lot_generator.get_next_date(), to_date('2019-02-10'))
        self.assertEquals(lot_generator.get_next_date(), to_date('2019-05-10'))
        self.assertNotEquals(lot_generator.get_next_date(), to_date('2019-06-16'))
        self.assertEquals(lot_generator.get_next_date(), to_date('2020-03-10'))

    def test_get_next_drugs(self):
        lot_rules = get_settings(rule_set_name='unit_test_1')
        lot_generator = LotGenerator('1', lot_rules)
        lot_generator.set_drug_list(drug_list=drugs_list)

        next_drugs = lot_generator.get_next_drugs(to_date('2019-02-10'))
        self.assertEquals([x.drug_name for x in next_drugs], ['drug_a', 'drug_b'])

        next_drugs = lot_generator.get_next_drugs(to_date('2019-06-10'))
        self.assertEquals([x.drug_name for x in next_drugs], ['drug_b-abc'])
                                                  


    def test_add_drugs_to_lot(self):
        lot_rules = get_settings(rule_set_name='unit_test_1')
        lot_generator = LotGenerator('1', lot_rules)
        lot_generator.set_drug_list(drug_list=drugs_list)




if __name__ == '__main__':
    unittest.main()     









