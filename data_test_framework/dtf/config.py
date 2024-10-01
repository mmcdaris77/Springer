import os 

ME_DIR = os.path.dirname(os.path.realpath(__file__))
PROJECT_PATH = os.path.dirname(ME_DIR)

OUTPUT_PATH = os.path.join(PROJECT_PATH, 'output')
INPUT_PATH = os.path.join(PROJECT_PATH, 'input')
UNIT_TEST_OUTPUT_PATH = os.path.join(OUTPUT_PATH, 'unit_test')
UNIT_TEST_INPUT_PATH = os.path.join(INPUT_PATH, 'unit_test')

if not os.path.isdir(OUTPUT_PATH):
    os.makedirs(OUTPUT_PATH, exist_ok=True)

if not os.path.isdir(UNIT_TEST_OUTPUT_PATH):
    os.makedirs(UNIT_TEST_OUTPUT_PATH, exist_ok=True)

if not os.path.isdir(INPUT_PATH):
    os.makedirs(INPUT_PATH, exist_ok=True)

if not os.path.isdir(UNIT_TEST_INPUT_PATH):
    os.makedirs(UNIT_TEST_INPUT_PATH, exist_ok=True)