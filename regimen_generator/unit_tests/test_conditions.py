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

# case 1
regimen_drugs = [Drug('person_1', 'drug_a', to_date('2009-05-18'))]
line_of_therapy = LineOfTherapy(lot=1, drugs=regimen_drugs)
next_drugs = [
    Drug('person_1', 'drug_b', to_date('2012-05-21')),
    Drug('person_1', 'drug_a', to_date('2012-05-21'))
]
case_1_fact_lot_next_drugs = FactLotNextDrugs(lot=line_of_therapy, next_drugs=next_drugs)
# case 2
regimen_drugs = [
    Drug('person_1', 'drug_b', to_date('2012-05-21')),
    Drug('person_1', 'drug_a', to_date('2012-05-21'))
]
line_of_therapy = LineOfTherapy(lot=1, drugs=regimen_drugs)
next_drugs = [Drug('person_1', 'drug_a', to_date('2012-07-21'))]
case_2_fact_lot_next_drugs = FactLotNextDrugs(lot=line_of_therapy, next_drugs=next_drugs)
# case 3
regimen_drugs = [
    Drug('person_1', 'drug_b', to_date('2012-05-21')),
    Drug('person_1', 'drug_a', to_date('2012-05-21'))
]
line_of_therapy = LineOfTherapy(lot=1, drugs=regimen_drugs)
next_drugs = [Drug('person_1', 'drug_c', to_date('2012-07-21'))]
case_3_fact_lot_next_drugs = FactLotNextDrugs(lot=line_of_therapy, next_drugs=next_drugs)
# case 4
regimen_drugs = [
    Drug('person_1', 'drug_b', to_date('2012-05-21')),
    Drug('person_1', 'drug_a', to_date('2012-05-21'))
]
line_of_therapy = LineOfTherapy(lot=1, drugs=regimen_drugs)
next_drugs = [Drug('person_1', 'drug_x', to_date('2012-07-21'))]
case_4_fact_lot_next_drugs = FactLotNextDrugs(lot=line_of_therapy, next_drugs=next_drugs)

# case 5
regimen_drugs = [Drug('person_1', 'drug_a', to_date('2012-05-18'))]
line_of_therapy = LineOfTherapy(lot=1, drugs=regimen_drugs)
next_drugs = [
    Drug('person_1', 'drug_b', to_date('2012-08-15'), therapy_route='Oral'),
    Drug('person_1', 'drug_a', to_date('2012-07-15'), therapy_route='IV')
]
case_5_fact_lot_next_drugs = FactLotNextDrugs(lot=line_of_therapy, next_drugs=next_drugs)
class TestFactLotNextDrugs(unittest.TestCase):

    def test_is_mono_therapy(self):
        logger.debug('>>>>>>>>>   START test_is_mono_therapy <<<<<<<<<<')
        #######################################################################
        self.assertTrue(case_1_fact_lot_next_drugs.is_mono_therapy())
        self.assertFalse(case_2_fact_lot_next_drugs.is_mono_therapy())

    def test_new_drugs_contains_drugs(self):
        logger.debug('>>>>>>>>>   START test_new_drugs_contains_drugs <<<<<<<<<<')
        #######################################################################
        self.assertTrue(case_1_fact_lot_next_drugs.new_drugs_contains_drugs('drug_b'))
        self.assertFalse(case_1_fact_lot_next_drugs.new_drugs_contains_drugs('drug_x'))

    def test_has_drug_additions(self):
        logger.debug('>>>>>>>>>   START test_has_drug_additions <<<<<<<<<<')
        #######################################################################
        self.assertTrue(case_1_fact_lot_next_drugs.has_drug_additions(), msg='test_has_drug_additions: assertTrue')
        self.assertFalse(case_2_fact_lot_next_drugs.has_drug_additions(swap_drugs=[]))


    def test_has_drug_additions_swappable(self):
        logger.debug('>>>>>>>>>   START test_has_drug_additions_swappable <<<<<<<<<<')
        #######################################################################
        swap_drugs = [['drug_a', 'drug_c']]
        self.assertFalse(case_3_fact_lot_next_drugs.has_drug_additions(swap_drugs=swap_drugs))
        self.assertTrue(case_4_fact_lot_next_drugs.has_drug_additions(swap_drugs=swap_drugs))
        swap_drugs = [['drug_x', 'drug_c']]
        self.assertTrue(case_3_fact_lot_next_drugs.has_drug_additions(swap_drugs=swap_drugs))


    def test_has_drug_drops(self):
        logger.debug('>>>>>>>>>   START test_has_drug_drops <<<<<<<<<<')
        #######################################################################
        self.assertFalse(case_1_fact_lot_next_drugs.has_drug_drops())
        self.assertTrue(case_2_fact_lot_next_drugs.has_drug_drops())

    def test_is_within_allowable_gap(self):
        logger.debug('>>>>>>>>>   START test_is_within_allowable_gap <<<<<<<<<<')
        #######################################################################
        self.assertTrue(case_2_fact_lot_next_drugs.is_within_allowable_gap(allowable_gap=20))

    def test_is_past_allowable_gap(self):
        logger.debug('>>>>>>>>>   START test_is_past_allowable_gap <<<<<<<<<<')
        #######################################################################
        self.assertTrue(case_2_fact_lot_next_drugs.is_past_allowable_gap(allowable_gap=20))
        self.assertFalse(case_2_fact_lot_next_drugs.is_past_allowable_gap(allowable_gap=90))

    def test_is_past_allowable_gap_w_therapy_routes(self):
        logger.debug('>>>>>>>>>   START test_is_past_allowable_gap_w_therapy_routes <<<<<<<<<<')
        #######################################################################
        self.assertTrue(case_5_fact_lot_next_drugs.is_past_allowable_gap(allowable_gap=80, therapy_routes=['oral']))
        self.assertFalse(case_5_fact_lot_next_drugs.is_past_allowable_gap(allowable_gap=90, therapy_routes=['oral']))



if __name__ == '__main__':
    unittest.main()     
