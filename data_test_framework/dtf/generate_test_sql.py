
from sqlglot import parse_one, exp
from sqlglot.expressions import Select, Literal, Null, Boolean
from sqlglot.optimizer import build_scope
from .config import UNIT_TEST_OUTPUT_PATH
import logging
import os

logger = logging.getLogger('dtf_logger')


DTF_CTE_PREFIX = 'dtf__cte__'
DTF_FINAL_WRAPPER_CTE = f'{DTF_CTE_PREFIX}_final'
DTF_FINAL_WRAPPER_CTE = f'{DTF_FINAL_WRAPPER_CTE}_{id(DTF_FINAL_WRAPPER_CTE)}'

def make_literal(schema: dict, column: str, value: any) -> Literal:
    # match a psudo datatype for quoting a literal
    NUMBER_MATCHES = ['number', 'int', 'decimal']
    STRING_MATCHES = ['string', 'text', 'varchar']
    BOOL_MATCHES = ['boolean', 'bit']
    NULL_MATCHES = ['null', 'blank', 'none']

    if isinstance(value, str) and value.lower() in NULL_MATCHES:
        return Null().as_(column) 
    if schema[column].lower() in NUMBER_MATCHES:
        return Literal.number(value).as_(column)
    if schema[column].lower() in STRING_MATCHES:
        return Literal.string(value).as_(column)
    if schema[column].lower() in BOOL_MATCHES:
        return Boolean(this=value).as_(column)


def make_mock_union(mock_node: dict) -> Select:
    for i, row in enumerate(mock_node['data']):
        schema = mock_node['schema']
        row_select = Select().select(*[make_literal(schema, k, v) for k, v in row.items()])

        if i == 0:
            cte_dtf_mock_data = row_select
        else:
            cte_dtf_mock_data = cte_dtf_mock_data.union(row_select, distinct=False)

    return cte_dtf_mock_data


def inject_mock_data_sql(sql, test_data: dict) -> str:
    dtf_mock_map = {}

    for x in list(test_data.keys()):
        dtf_mock_map[x] = {'id': id(x)}

    ast = parse_one(sql)
    root = build_scope(ast)
    for k, v in test_data.items():
        mock_cte_name = f"{DTF_CTE_PREFIX}{dtf_mock_map[k]['id']}"
        cte_dtf_mock_data = make_mock_union(v)

        for t in root.find_all(exp.Table):
            if str(t.this).lower() == k.lower():
                # set the cte name and remove db.schema if they exist
                t.set('this', mock_cte_name)
                t.set('db', None)
                t.set('catalog', None)

        ast = ast.with_(mock_cte_name, as_=cte_dtf_mock_data)
    
    return ast.sql()


def inject_test_data_sql(sql: str, expected_values: dict) -> str:
    ast = parse_one(sql)
    test_cte_qurey = make_mock_union(expected_values)

    test_cte_name = f'{DTF_CTE_PREFIX}expected_values_{id(test_cte_qurey)}'
    ast = ast.with_(test_cte_name, as_=test_cte_qurey)

    return ast.sql(), test_cte_name


def write_output_file(sql: str, file_name: str) -> None:
    # NOTE: the output should be the test name not the file name
    # a file may require more than one unit test... 
    f_name = f"{file_name.split('.')[0]}_unit_test.sql"
    logger.debug(f'generating output file for unit test: {f_name}')
    with open(os.path.join(UNIT_TEST_OUTPUT_PATH, f_name), 'w', encoding='utf8') as f:
        f.write(sql)


def generate_test_sql(sql, test_data, expected_values) -> str:
    sql = inject_mock_data_sql(sql=sql, test_data=test_data)

    sql, expected_values_cte_name = inject_test_data_sql(sql, expected_values)

    ast = parse_one(sql)
 
    join_on = [f'{DTF_FINAL_WRAPPER_CTE}.{k} = {expected_values_cte_name}.{k}' for k, v in expected_values['schema'].items()]
    where_test = ' or '.join([f'{expected_values_cte_name}.{k} is null' for k, v in expected_values['schema'].items()])

    final_select = Select().select('*').from_(DTF_FINAL_WRAPPER_CTE).join(expected_values_cte_name, on=join_on, join_type='left')
    final_select = final_select.where(where_test)

    root = build_scope(ast)
    for cte in root.find_all(exp.CTE):
        final_select = final_select.with_(cte.alias, cte.this)

    ast.find(exp.With).pop()
    final_select = final_select.with_(DTF_FINAL_WRAPPER_CTE, ast)

    return final_select.sql(pretty=True)


if __name__ == '__main__': 
    sql = '''with cte_zero as (select 0 as zero) select a.col_a, b.col_b 
        ,case when a.col_a % 2 = 0 then 1 else 0 end as case_col
    from tbl_x as a join tbl_z b on a.id = b.id'''

    test_data = {
        'tbl_x': {
            'schema': {'id': 'number', 'col_a': 'number', 'col_b': 'number', 'col_c': 'string', 'bol': 'boolean'},
            'data': [
                {'id': 1, 'col_a': 1, 'col_b': 2, 'col_c': 'null', 'bol': 'null'},
                {'id': 2, 'col_a': 3, 'col_b': 4.55, 'col_c': 'a', 'bol': 'True'},
                {'id': 3, 'col_a': 1, 'col_b': 2, 'col_c': 'null', 'bol': 0},
            ]
        },
        'another_tbl': {
            'schema': {'id': 'number', 'value': 'string'},
            'data': [
                {'id': 100, 'value': 'grr'},
                {'id': 103, 'value': 'fur'}
            ]
        }
    }

    expected_values = {
        'schema': {'col_a': 'number', 'case_col': 'int'},
        'data':[
            {'col_a': 1, 'case_col': 0},
            {'col_a': 2, 'case_col': 1},
        ]
        
    }

    
    test_query = generate_test_sql(sql, test_data, expected_values)

    #sql, expected_values_cte_name = inject_test_data_sql(sql, expected_values)
    
    write_output_file(test_query, 'test_mod.sql')
