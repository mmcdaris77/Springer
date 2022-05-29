from dagster import op, Out 
from helpers import split_csv_into_parts
import os
import urllib.request
import zipfile
import pandas
import sqlite3


@op(
        required_resource_keys={"npi_data_resouce", "hrr_data_resource", "pop_data_resource"}, 
        out={"npi_data_vars": Out(), "hrr_data_vars": Out(), "pop_data_vars": Out()},
        description='''Set vars for multiple files to process so we can reuse some ops'''
        )
def set_vars(context):
    npi_data_vars = {}
    hrr_data_vars = {}
    pop_data_vars = {}

    npi_data_vars['url'] = context.resources.npi_data_resouce['url']
    npi_data_vars['download_file_dest'] = context.resources.npi_data_resouce['dest_file_path']
    npi_data_vars['download_dir'] = context.resources.npi_data_resouce['download_dir']
    npi_data_vars['csv_dir'] = context.resources.npi_data_resouce['csv_dir']
    npi_data_vars['quote_char'] = context.resources.npi_data_resouce['quote_char']

    hrr_data_vars['url'] = context.resources.hrr_data_resource['url']
    hrr_data_vars['download_file_dest'] = context.resources.hrr_data_resource['dest_file_path']
    hrr_data_vars['download_dir'] = context.resources.hrr_data_resource['download_dir']
    hrr_data_vars['csv_dir'] = context.resources.hrr_data_resource['csv_dir']
    hrr_data_vars['quote_char'] = context.resources.hrr_data_resource['quote_char']

    pop_data_vars['url'] = context.resources.pop_data_resource['url']
    pop_data_vars['download_file_dest'] = context.resources.pop_data_resource['dest_file_path']
    pop_data_vars['download_dir'] = context.resources.pop_data_resource['download_dir']
    pop_data_vars['csv_dir'] = context.resources.pop_data_resource['csv_dir']
    pop_data_vars['quote_char'] = context.resources.pop_data_resource['quote_char']

    return npi_data_vars, hrr_data_vars, pop_data_vars

@op()
def download_file(context, vars):
    url = vars['url']
    destination_file_path = vars['download_file_dest']
    context.log.info("downloading file from {} \nto destination {}".format(url, destination_file_path))
    response = urllib.request.urlretrieve(url, destination_file_path)
    return response

@op()
def unzip_file(context, after, vars):
    zip_file = vars['download_file_dest']
    destination_folder_path = vars['download_dir']
    with zipfile.ZipFile(zip_file, 'r') as z:
        z.extractall(destination_folder_path)

    return True

@op()
def split_csv_to_parts(context, after, vars):
    in_path = vars['download_dir']
    out_path = vars['csv_dir']
    quote_char = vars['quote_char']
    
    prefix='stg_'
    file_size=200000
    files = os.listdir(in_path)
    
    for f in files:
        file_to_part = os.path.join(in_path, f)
        if os.path.isfile(file_to_part):
            if f.split('.')[1] == 'csv':
                split_csv_into_parts(file_to_part, prefix=prefix, out_dir=out_path, file_size=file_size, quote_char=quote_char)

    return True

@op(required_resource_keys={"database_connection"}, )
def csv_parts_to_sqlite(context, after, vars):
    sql_con = sqlite3.connect(context.resources.database_connection)
    tmp_path = vars['csv_dir']

    context.log.info('TMP_PATH ' + tmp_path)

    files = os.listdir(tmp_path)
    i = 0

    for f in files:
        file_to_part = os.path.join(tmp_path, f)
        if os.path.isfile(file_to_part):
            if f.split('.')[1] == 'csv':
                table_name = f.split('.')[0]
                context.log.info('Importing csv: {0} \nas: {1}'.format(f, table_name))
                csv_file = file_to_part
                with open(csv_file, 'r') as cf:
                    h = cf.readline()

                # make all cols as strings
                dtypes = {}
                for col in h.split(','):
                    dtypes[col.replace('"', '').replace('\n', '')] = 'string'

                df = pandas.read_csv(csv_file, dtype=dtypes)
                df.columns.str.replace(' ', '_')
                df.to_sql(table_name, sql_con, if_exists='replace', index=False, dtype=dtypes)

                os.remove(csv_file)
                i += 1

@op(required_resource_keys={"dbt"})
def run_dbt(context, after):
    models_selector = 'npi_data.*'
    context.resources.dbt.run(models=models_selector)

@op(required_resource_keys={"dbt"})
def run_operation(context, after):
    context.resources.dbt.run_operation(macro='sqlite_drop_tables_by_pattern', args={'v_pattern':'stg_%', 'v_log_only': False})



