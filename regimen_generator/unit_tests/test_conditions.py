import sys
sys.path.append(".")

import unittest
from datetime import datetime, date
from LotGenerator.LotRules import FactLotNextDrugs
from LotGenerator.LineOfTherapy import LineOfTherapy, Drug
from LotGenerator.lot_logger import logger
logger = logger('lot_logger')

h = '*'*100
logger.debug(f'\n{h}\n**** UNIT TESTS\n{h}')


def to_date(dt:str, pattern: str = '%Y-%m-%d') -> date:
    return datetime.strptime(dt, pattern).date()


regimen_drugs = [Drug('person_1', 'drug_a', to_date('2009-05-18'))]
line_of_therapy = LineOfTherapy(lot=1, drugs=regimen_drugs)
next_drugs = [
    Drug('person_1', 'drug_b', to_date('2012-05-21')),
    Drug('person_1', 'drug_a', to_date('2012-05-21'))
]
case_1_fact_lot_next_drugs = FactLotNextDrugs(lot=line_of_therapy, next_drugs=next_drugs)

regimen_drugs = [
    Drug('person_1', 'drug_b', to_date('2012-05-21')),
    Drug('person_1', 'drug_a', to_date('2012-05-21'))
]
line_of_therapy = LineOfTherapy(lot=1, drugs=regimen_drugs)
next_drugs = [Drug('person_1', 'drug_a', to_date('2012-07-21'))]
case_2_fact_lot_next_drugs = FactLotNextDrugs(lot=line_of_therapy, next_drugs=next_drugs)

class TestFactLotNextDrugs(unittest.TestCase):\

    def test_is_mono_therapy(self):
        self.assertTrue(case_1_fact_lot_next_drugs.is_mono_therapy())
        self.assertFalse(case_2_fact_lot_next_drugs.is_mono_therapy())

    def test_new_drugs_contains_drugs(self):
        self.assertTrue(case_1_fact_lot_next_drugs.new_drugs_contains_drugs('drug_b'))
        self.assertFalse(case_1_fact_lot_next_drugs.new_drugs_contains_drugs('drug_x'))

    def test_has_drug_additions(self):
        self.assertTrue(case_1_fact_lot_next_drugs.has_drug_additions())
        self.assertTrue(case_2_fact_lot_next_drugs.has_drug_additions())

    def test_has_drug_drops(self):
        self.assertFalse(case_1_fact_lot_next_drugs.has_drug_drops())
        self.assertTrue(case_2_fact_lot_next_drugs.has_drug_drops())

    def test_is_within_allowable_gap(self):
        self.assertTrue(case_2_fact_lot_next_drugs.is_within_allowable_gap(allowable_gap=20))



if __name__ == '__main__':
    unittest.main()        
