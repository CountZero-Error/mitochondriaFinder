import os
import sys
import csv
import time
from collections import Counter

from joblib import PrintTime

class FINDER():
    def __init__(self) -> None:
        pass

    def ATCG_percent(self, ATCG_statistic, name, v):
        try:
            percent = int(ATCG_statistic[name])/len(v)
        except KeyError:
            percent = 0
        
        return percent

#             | Method                                  | Variables
    def FINDER(self, input_checking, database_checking, clock, inputFolder, output, database_path, limitation, files, total_number):
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
        statistic_rows = []
        for k, v in sequences.items():
            for key in Counter(v).keys():
                perfect += key
                break

            # Statistic about A, T, C, G in each colum(%)
            ATCG_statistic = {}
            
            for elm in v:
                ATCG_statistic.setdefault(elm, 0)
                ATCG_statistic[elm] += 1
            
            A_percent = self.ATCG_percent(ATCG_statistic, 'A', v)
            T_percent = self.ATCG_percent(ATCG_statistic, 'T', v)
            C_percent = self.ATCG_percent(ATCG_statistic, 'C', v)
            G_percent = self.ATCG_percent(ATCG_statistic, 'G', v)
            statistic_rows.append([k, A_percent, T_percent, C_percent, G_percent])

        statistic_header = ['number', 'A', 'T', 'C', 'G']
        dirPath = os.path.dirname(output)
        statistic = os.path.join(dirPath, 'ATCG_statistic.csv')
        print('Generating ATCG statistic file...')
        with open(statistic, 'w') as out:
            csv_f = csv.writer(out)
            csv_f.writerow(statistic_header)
            csv_f.writerows(statistic_rows)
        
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
        TIME = clock(end - start)
        print(f'\nTime spend: {TIME}s')
