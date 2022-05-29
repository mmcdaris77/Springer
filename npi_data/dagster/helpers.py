
import os
import re


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
    split_by = "{}{}{}".format(quote_char, delim, quote_char)
    encoding = 'utf-8'
    print('#'*100)
    print('base_file_name', base_file_name)
    print('split_by', split_by)
    print('encoding', encoding)
    print('#'*100)
    with open(csv_file, 'r') as f:
        encoding = f.encoding

    with open(csv_file, "rb") as f:
        counter = 0
        partition_num = 0
        cols = f.readline().decode(encoding).split(split_by)
        col_count = len(cols)
        headers_row = bytes(",".join([re.sub(r'[^A-Za-z0-9 \n]', '', i).replace('  ', ' ').replace(' ', '_') for i in cols]), encoding)
        


        for line in f:
            if counter % file_size == 0:
                # set up new file partition
                current_out_path = os.path.join(out_dir, "{0}\\{1}{2}_{3}.csv".format(out_dir, prefix, base_file_name, partition_num))
                current_out_writer = open(current_out_path, 'wb')
                current_out_writer.write(headers_row)
                partition_num += 1

            if counter != 0:
                # do some super basic validation; all rows should have the same # cols as the header row
                try:
                    if len(line.decode(encoding, 'replace').split(split_by)) == col_count:
                        current_out_writer.write(line)
                    else:
                        print("Line {} in file {} is not a valid line.  There are {} splitters when exactly {} are allowed".format(counter, csv_file, len(line.decode(encoding).split(split_by)), col_count))
                except Exception as e:
                    print('#'*100)
                    print("Line {} in file {} is not a valid line.  \n{}".format(counter, csv_file, e))
                    print('#'*100)

            counter += 1
