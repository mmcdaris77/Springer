
import os
import re
import csv

def get_clean_file_name(file_name):
    ''' 
        takes a file name and removes stuff 
        and return a file name string without extension
    '''
    file_parts = file_name.split('.')
    # remove extension
    clean_name = re.sub(r'[0-9 -]', '', file_parts[0])
    # remove trailing underscore
    while clean_name[-1] == '_':
        clean_name = clean_name[0:len(clean_name) - 1]

    # add extension back
    return clean_name 


def split_csv_into_parts(csv_file, out_dir, prefix='', file_size=10000, delim=',', quote_char='"'):
    base_file_name = get_clean_file_name(csv_file.split('\\')[-1])

    with open(csv_file, 'r', newline='', errors='ignore') as f:
        counter = 0
        partition_num = 0
        if quote_char == '':
            quote_char = None

        csv_reader = csv.reader(f, delimiter=delim, quotechar=quote_char) 
        for row in csv_reader:
            if counter == 0:
                header_row = row
                header_row = [re.sub(r'[^A-Za-z0-9 \n]', '', i).replace('  ', ' ').replace(' ', '_').lower() for i in header_row]
                col_count = len(header_row)
            if counter % file_size == 0:
                current_out_path = os.path.join(out_dir, "{0}\\{1}{2}_{3}.csv".format(out_dir, prefix, base_file_name, partition_num))
                current_out_file = open(current_out_path, 'w', newline='', encoding='utf-8')
                current_out_writer = csv.writer(current_out_file, delimiter='\x01',quotechar='', quoting=csv.QUOTE_NONE, escapechar='~')
                current_out_writer.writerow(header_row)
                partition_num += 1
            else:
                # do some super basic validation; all rows should have the same # cols as the header row
                try:
                    if len(row) == col_count:
                        current_out_writer.writerow(i.replace('\n', '').replace('\r', '') for i in row)
                    else:
                        print("Line {} in file {} is not a valid line.  There are {} splitters when exactly {} are allowed".format(counter, csv_file, len(line.decode(encoding).split(split_by)), col_count))
                except Exception as e:
                    print('#'*100)
                    print("Line {} in file {} is not a valid line.  \n{}".format(counter, csv_file, e))
                    print('#'*100)

            counter += 1
                
def sqlite_power(x,n):
    return int(x)**n

def generate_dbt_profiles_yml(profiles_path, sqlite_db, postgres_host, postgres_user, postgres_pw, postgres_db):
    profiles_yml_file = os.path.join(profiles_path, 'profiles.yml')
    profiles_yml_content = '''
sqlite_npi:
    outputs:

        dev:
            type: sqlite
            threads: 1
            database: 'npi_db'
            schema: 'main'
            schemas_and_paths:
                main: '{}'
            schema_directory: '/my_project/data'

    target: dev

postgres_metest:
    target: dev
    outputs:
        dev:
            type: postgres
            host: {} 10.0.0.15
            user: {} pi
            password: {} raspberry
            port: 5432
            dbname: {} metest
            schema: public
            threads: 4
            keepalives_idle: 0 # default 0, indicating the system default. See below
            #connect_timeout: 10 # default 10 seconds

    '''.format(sqlite_db, postgres_host, postgres_user, postgres_pw, postgres_db)

    with open(profiles_yml_file, 'w') as f:
        f.write(profiles_yml_content)