import os
import glob
import json
from dtf.generate_test_sql import generate_test_sql, write_output_file
from dtf.config import UNIT_TEST_INPUT_PATH, INPUT_PATH
from dtf.logger import logger

logger = logger(log_debug=True)

for test_file in glob.glob(os.path.join(UNIT_TEST_INPUT_PATH, '*.json')):
    with open(test_file, 'r') as f:
        test_config = json.loads(f.read())
    file_name = test_config['name']
    test_data = test_config['test_data']
    expected_values = test_config['expected_values']

    print(f'processing test: {file_name}')

    in_sql_file = os.path.join(INPUT_PATH, f'sql/{file_name.split(".")[0]}.sql')
    #print(f'reading sql file: {in_sql_file}')
    with open(in_sql_file) as sf:
        sql = sf.read()

    if sql is None or sql.strip() == '':
        print('no sql in file: {in_sql_file}')
        continue
    test_sql = generate_test_sql(sql=sql, test_data=test_data, expected_values=expected_values)
    write_output_file(sql=test_sql, file_name=file_name)




#print(json.dumps(test_config, indent=4))

