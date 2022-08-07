from dagster import resource
from dagster_dbt import dbt_cli_resource
import os
import sqlite3
import psycopg2
from helpers import sqlite_power,generate_dbt_profiles_yml

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, 'data')
DBT_PROJECT_PATH = os.path.join(PROJECT_ROOT, 'dbt')
TMP_DATA_OUT_PATH = os.path.join(DATA_PATH, 'tmp\\')
SQLITE_PATH = os.path.join(DATA_PATH, 'sqlite\\') 
SQLITE_DB = os.path.join(DATA_PATH, 'sqlite\\npi_db.db') 

"""
    setup some stuff:
        - make a local profiles.yml for dbt with SQLITE_DB path
        - create dirs if they are not there
        - create sqlite db if not there
"""

if not os.path.isdir(DATA_PATH):
    os.makedirs(DATA_PATH)
    
if not os.path.isdir(TMP_DATA_OUT_PATH):
    os.makedirs(TMP_DATA_OUT_PATH)

if not os.path.isdir(os.path.dirname(SQLITE_PATH)):
    os.makedirs(os.path.dirname(SQLITE_PATH))

# make db
con = sqlite3.connect(SQLITE_DB)
# add power function for dbt_utils.generate_series()
con.create_function("power", 2, sqlite_power)
con.close()


npi_dbt_resource = dbt_cli_resource.configured(
    {
        "project_dir": DBT_PROJECT_PATH,
        "profile": "sqlite_npi",
        "profiles-dir": PROJECT_ROOT
    }
)

'''
    dagster resources and helpers
    vars for importing csv from web:
        - url
        - udest_file_name
        - udest_file_path
        - uunzip_path
'''
def make_data_dirs(str_name):
    '''make tmp sub dirs for named resource/csv configuration'''
    download_dir = os.path.join(os.path.join(TMP_DATA_OUT_PATH, str_name), 'download')
    csv_dir = os.path.join(os.path.join(TMP_DATA_OUT_PATH, str_name), 'csv_files')

    if not os.path.isdir(download_dir):
        os.makedirs(download_dir)
    if not os.path.isdir(csv_dir):
        os.makedirs(csv_dir)

    return download_dir, csv_dir


@resource(
    config_schema={"con_type": str, "postgres_host": str, "postgres_user": str, "postgres_pw": str, "postgres_db": str},
    description='''I am a SQLITE database path'''
)
def database_connection(context):
    postgres_host = context.resource_config["postgres_host"]
    postgres_user = context.resource_config["postgres_user"]
    postgres_pw = context.resource_config["postgres_pw"]
    postgres_db = context.resource_config["postgres_db"]
    con = None
    con_type = context.resource_config["con_type"].upper()
    if con_type == 'SQLITE':
        con = sqlite3.connect(SQLITE_DB)
    if con_type == 'POSTGRES':
        con = psycopg2.connect(
                                host=postgres_host,
                                database=postgres_db,
                                user=postgres_user,
                                password=postgres_pw)

    # make a project yml file locally for the sqlite connection  
    generate_dbt_profiles_yml(PROJECT_ROOT, SQLITE_DB, postgres_host, postgres_user, postgres_pw, postgres_db)

    return {'connection':con, 'con_type': con_type}
# 

@resource(
    description='''vars for processing the npi data'''
)
def npi_data_resouce(context):
    url = 'https://download.cms.gov/nppes/NPPES_Data_Dissemination_May_2022.zip'
    dest_file_name = 'NPPES_Data_Dissemination.zip'
    download_dir, csv_dir = make_data_dirs('npi_data')
    dest_file_path = os.path.join(download_dir, dest_file_name)

    vars = {
        'url': url,
        'download_dir': download_dir,
        'dest_file_path': dest_file_path,
        'csv_dir': csv_dir,
        'quote_char': '"'
    }
    return vars


@resource(
    description='''vars for processing the hrr data'''
)
def hrr_data_resource(context):
    url = 'https://data.dartmouthatlas.org/downloads/geography/ZipHsaHrr19.csv.zip'
    dest_file_name = 'ZipHsaHrr19.zip'
    download_dir, csv_dir = make_data_dirs('hrr_data')
    dest_file_path = os.path.join(download_dir, dest_file_name)

    vars = {
        'url': url,
        'download_dir': download_dir,
        'dest_file_path': dest_file_path,
        'csv_dir': csv_dir,
        'quote_char': ''
    }
    return vars


@resource(
    description='''vars for processing the population data'''
)
def pop_data_resource(context):
    url = 'https://data.lacity.org/api/views/nxs9-385f/rows.csv?accessType=DOWNLOAD'
    dest_file_name = '2010_Census_Populations_by_Zip_Code.csv'
    download_dir, csv_dir = make_data_dirs('pop_data')

    dest_file_path = os.path.join(download_dir, dest_file_name)

    vars = {
        'url': url,
        'download_dir': download_dir,
        'dest_file_path': dest_file_path,
        'csv_dir': csv_dir,
        'quote_char': ''
    }
    return vars

