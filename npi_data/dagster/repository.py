from dagster import repository
from jobs import npi_job, npi_dbt_only_job

'''
    dagit -f repository.py

    http://127.0.0.1:3000


'''

@repository
def my_repository():
    return [
        npi_job,
        npi_dbt_only_job,
    ]

