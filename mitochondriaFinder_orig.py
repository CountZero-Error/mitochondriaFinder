import os
import sys
import csv
import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

# methods
def clock(Time):
    Time = str(Time)
    result = Time.index('.')
    
    return Time[:result]

def database_checking(database_path):
    if database_path == None:
        print('Need parameter "-D", OLD_DATA_CSV_COLLECTIONS_PATH, need ".csv" file.\n')
        return False

def input_checking(inputFolder):
    if inputFolder == None:
        print('Need parameter "-I", INPUT_FOLDER_PATH.\n')
        return False

def int_input_checking():
    target = input('Enter target sequence length:')

    try:
        target = int(target)
    except ValueError:
        int_input_checking()
    else:
        return target

def write_file(contents):
    file_path = input('Enter file path:')
    try:
        with open(file_path, 'w') as out:
            print(f'Generating file - {os.path.basename(file_path)}...')
            for content in contents:
                out.write(content)
        
        print('Done.')
    except(FileNotFoundError):
        write_file(contents)

def write_to_local_file(contents):
    YorN = input('Do you want to generate a file for this?(Y/n)')
    
    if YorN.lower() == 'y':
        write_file(contents)

    elif YorN.lower() == 'n':
        pass
    else:
        write_to_local_file(contents)

parse = argparse.ArgumentParser()
parse.add_argument('-I', '--INPUT_FOLDER_PATH', type=str)
parse.add_argument('-O', '--OUTPUT_FILE_PATH', type=str)
parse.add_argument('-Data', '--OLD_DATA_CSV_COLLECTIONS_PATH', type=str)
parse.add_argument('-M', '--MODE', required=True, type=str, choices=['length', 'finder', 'search'])
parse.add_argument('-L', '--LENGTH', type=int, default=0)
args =parse.parse_args()

inputFolder = args.INPUT_FOLDER_PATH
output = args.OUTPUT_FILE_PATH
database_path = args.OLD_DATA_CSV_COLLECTIONS_PATH
mode = args.MODE
limitation = args.LENGTH

clock = 0
total_number = 0
files = os.listdir(inputFolder)

# main
# length
# -I ../.. -O ../.. -M ../..
if mode == 'length':
    if input_checking(inputFolder) == False:
        sys.exit()

    start = time.time()
    print('Mode: length')
    time.sleep(1)
    
    L_dict = {}
    sequence_len = 0
    sequence = False

    for file in files:
        print(f'Processing file - {file}...')
        with open(os.path.join(inputFolder, file)) as filo:
            for line in filo:
                if line.startswith('>'):
                    total_number += 1
                elif line == '\n' and sequence_len != 0:
                    L_dict.setdefault(sequence_len, 0)
                    L_dict[sequence_len] += 1

                    # test
                    #print(f'{sequence_len}: {L_dict[sequence_len]}')
                    #time.sleep(1)

                    sequence_len = 0
                else:
                    length = len(line.replace('\n', ''))
                    sequence_len += length

                    # test
                    #print(f'{length}:{line}')
        
        print('Done.')
        time.sleep(1)
        
    print(f'Generating result - {os.path.basename(output)}...')
    L_list = sorted(L_dict.items(), key=lambda d: d[1], reverse=True)
    with open(output, 'w') as out:
        out.write(f'Total number: {total_number}\n')
        for elm in L_list:
            out.write(f'{elm[0]}: {elm[1]}\n')

    print('Done.')
    time.sleep(1)

    print(f'Generating plot...')
    x = []
    y = []

    for k , v in L_dict.items():
        rate = int(v)/int(total_number)
        if rate > 0.01:
            rate = round(rate, 2)
            x.append(f'{k}\n({int(rate*100)}%)')
            y.append(v)
        
    y = np.array(y)

    plt.figure(figsize=(20, 8), dpi=100)
    plt.bar(range(len(x)), y, width=0.5)
    plt.title('Genome length statistic\n' + r'1% and above', fontsize=20)
    plt.xticks(range(len(x)), x)
    plt.savefig(os.path.join(os.path.dirname(output), 'mt-Length.png'))
        
    print('Done.')

    end = time.time()
    T = clock(end - start)
    print(f'\nTime spend: {T}s')



# finder
# -I ../.. -O ../.. -M finder -Data ../.. -L 0
if mode == 'finder':
    if input_checking(inputFolder) == False:
        sys.exit()

    if database_checking(database_path) == False:
        sys.exit()

    header = ['name', 'length', 'sequence']
    rows = []

    start = time.time()
    print('Mode: finder')
    time.sleep(1)

    P_list = []
    head_tmp = ''
    sequence_tmp = ''

    for file in files:
        print(f'Processing file - {file}...')
        with open(os.path.join(inputFolder, file)) as filo:
            for line in filo:
                if line.startswith('>'):
                    total_number += 1
                    tmp = ''
                    head_tmp = line.replace('\n', '')

                elif line == '\n':
                    P_list.append(tmp)
                    rows.append([head_tmp, len(tmp), tmp])
                else:
                    tmp += line.replace('\n', '')

        print('Done.')
        time.sleep(1)
    
    print('Receiving mitochondria genome result...')
    sequences = {}
    for elm in P_list:
        length = len(elm)
        for i in range(length):
            sequences.setdefault(i,[])
            sequences[i].append(elm[i])

            # test
            #print(f'{i}: {sequences[i]}')

    perfect = ''
    for k, v in sequences.items():
        for k in Counter(v).keys():
            perfect += k
            break
    
    if limitation != 0:
        perfect = perfect[:limitation]

    print('Done')
    print(f'Total sequences: {total_number}.')
    time.sleep(1)

    print(f'Generating result - {os.path.basename(output)}...')
    with open(output, 'w') as out:
        out.write(f'>Result_length_{len(perfect)}\n{perfect}\n')
    
    with open(database_path, 'a') as db_path:
        csv_f = csv.writer(db_path)
        csv_f.writerow(header)
        csv_f.writerows(rows)

    print('Done.')

    end = time.time()
    T = clock(end - start)
    print(f'\nTime spend: {T}s')



# search
# -M search -Data ../..
if mode == 'search':
    if database_checking(database_path) == False:
        sys.exit()

    start = time.time()
    print('Mode: search')
    time.sleep(1)

    target = int_input_checking()

    find = False
    tmp = []
    i = 0
    with open(database_path) as db:
        csv_f = csv.reader(db)
        for row in csv_f:
            try:
                if row[1] == str(target):
                    print(f'Find genome with length: {target}')
                    print(f'{row[0]}({row[1]})\n')
                    tmp.append(f'{row[0]}({row[1]}):\n{row[2]}\n')
                    i += 1
                    find = True
            except IndexError:
                pass
    print(f'Total: {i}\n')

    if find:
        write_to_local_file(tmp)
    else:
        print('Not found.')

    end = time.time()
    T = clock(end - start)
    print(f'\nTime spend: {T}s')        
