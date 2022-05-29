

### This is an example of using Dagster to orchestrate a data pipeline with DBT transformations. 
### Features:
- download csv file
- unzip files
- split large files into smaller ones
- import into a sqlite database
- make ops reusbale 
- dbt
    - union parts 
    - split out some data into new tables
    - override some dbt_utils to support sqlite
    - drop staging tables

### Run:
- cd to <repo_path>/npi_data/dagster/
- run: dagit -f repository.py
- open browser to: http://127.0.0.1:3000