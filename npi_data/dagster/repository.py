from dagster import repository
from jobs import npi_job

'''
    dagit -f repository.py

    http://127.0.0.1:3000


'''

@repository
def my_repository():
    return [
        npi_job,
    ]

