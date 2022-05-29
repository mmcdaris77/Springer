from dagster import job 
from resources import npi_dbt_resource
from resources import npi_data_resouce, hrr_data_resource, database_connection, pop_data_resource
from ops import download_file, unzip_file, split_csv_to_parts, csv_parts_to_sqlite, run_dbt
from ops import set_vars, run_operation, dbt_deps

@job(
        resource_defs={
                        "dbt": npi_dbt_resource, 
                        "npi_data_resouce": npi_data_resouce, 
                        "hrr_data_resource":hrr_data_resource, 
                        "database_connection": database_connection,
                        "pop_data_resource": pop_data_resource}, 
        description='''
            Job used to:
            - download some csv files
            - split them into parts with some basic validation
            - import parts in to sqlite
            - run dbt
                - union parts
                - split out sequenced columns into their own tables
            - drop stg_ tables
        '''
)
def npi_job():
    npi_data_vars, hrr_data_vars, pop_data_vars = set_vars()
    deps = dbt_deps()
    download_npi_zip_response = download_file(vars=npi_data_vars)
    download_hrr_zip_response = download_file(vars=hrr_data_vars)
    download_pop_zip_response = download_file(vars=pop_data_vars)
    unzip_npi_file = unzip_file(after=download_npi_zip_response, vars=npi_data_vars)
    unzip_hrr_file = unzip_file(after=download_hrr_zip_response, vars=hrr_data_vars)
    split_npi_files = split_csv_to_parts(after=unzip_npi_file, vars=npi_data_vars)
    split_hrr_files = split_csv_to_parts(after=unzip_hrr_file, vars=hrr_data_vars)
    split_pop_files = split_csv_to_parts(after=download_pop_zip_response, vars=pop_data_vars)
    csv_to_sqlite_hrr = csv_parts_to_sqlite(after=[
                                                    split_npi_files, 
                                                    split_hrr_files, 
                                                    split_pop_files
                                                ], vars=hrr_data_vars)
    csv_to_sqlite_pop = csv_parts_to_sqlite(after=csv_to_sqlite_hrr, vars=pop_data_vars)
    csv_to_sqlite_npi = csv_parts_to_sqlite(after=csv_to_sqlite_pop, vars=npi_data_vars)
    run_dbt_npi = run_dbt(after=[
                                    csv_to_sqlite_npi,
                                    csv_to_sqlite_hrr,
                                    csv_to_sqlite_pop,
                                    deps
                                ])
    drop_stg_tables = run_operation(after=run_dbt_npi)

