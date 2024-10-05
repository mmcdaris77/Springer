from sqlglot import parse_one, exp 
from collections import Counter
import os


THINGS_TO_COUNT = {
    'CASE': {'type': exp.Case},
    'IFF': {'type': exp.If},
    'WINDOW': {'type': exp.Window}
}

def get_test_potential(sql):
    '''get count of potential unit tests in sql query'''
    output = {} 
    ast = parse_one(sql, dialect='snowflake')

    for k, v in THINGS_TO_COUNT.items():
        cnt = 0
        for e in ast.find_all(v['type']):
            cnt += 1
        output[k] = cnt

    if 'CASE' in output and 'IFF' in output:
        output['IFF'] = output['IFF'] - output['CASE']
    return output


def get_test_potential_from_file(sql_path):
    #print(f'processing file: {os.path.basename(sql_path)}')
    with open(sql_path, 'r', encoding='utf8') as f: 
        sql_data = f.read()

    return get_test_potential(sql=sql_data)


def get_test_potential_from_path(sql_path, potential_cnt: Counter = Counter()):
    '''get counts for possible unit test in file[s]'''
    if os.path.isdir(sql_path): 
        sql_files = [os.path.join(root, file) for root, dirs, files in os.walk(sql_path) for file in files if file.endswith(".sql")]
        for s in sql_files:
            cnt = get_test_potential_from_file(s)
            potential_cnt.update(cnt)
    elif os.path.isfile(sql_path): 
        cnt = get_test_potential_from_file(sql_path)
        potential_cnt.update(cnt)
    return dict(potential_cnt)



if __name__ == '__main__': 
    sql = '''with cte_zero as (select 0 as zero) select a.col_a, b.col_b 
        ,case when a.col_a % 2 = 0 then 1 else 0 end as case_col
        ,iif(1=1, 1, 0) as oneone
    from tbl_x as a join tbl_z b on a.id = b.id
    qualify row_number() over(partition by a.col1 order by case when a.col2 in (1,2) then 0 else 1 end) = 1
    '''
    ast = parse_one(sql, dialect='snowflake')
    with open(r'C:\_repos\Springer\data_test_framework\output\log\grr.ini', 'w') as f:
        f.write(repr(ast))

    x = get_test_potential(sql)
    print(x)



    repo_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    sql_path = os.path.join(repo_dir, 'omop','omop_54','target','compiled','omop_54','models','staging')
    print(dict(get_test_potential_from_path(sql_path)))