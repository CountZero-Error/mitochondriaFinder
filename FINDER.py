import os
import sys
import time
import pandas as pd

class FINDER():
    def __init__(self) -> None:
        pass

    def ATCG_percent(self, ATCG_statistic, name, v):
        try:
            percent = int(ATCG_statistic[name])/len(v)
            percent = f'{round(percent*100, 2)}%'
        except KeyError:
            percent = '0%'
        
        return percent

#             | Method                                  | Variables
    def FINDER(self, input_checking, database_checking, inputFolder, output, database_path, limitation, files, total_number):
        if input_checking(inputFolder) == False:
            sys.exit()

        if database_checking(database_path) == False:
            sys.exit()

        csv_name, csv_len, csv_seq = [], [], []

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
                        csv_name.append(head_tmp)
                        csv_len.append(len(tmp))
                        csv_seq.append(tmp)
                    else:
                        tmp += line.replace('\n', '')

            print('Done.')
            time.sleep(1)
        
        print('\nReceiving mitochondria genome result...')
        sequences = {}
        for elm in P_list:
            length = len(elm)
            for i in range(length):
                sequences.setdefault(i,[])
                sequences[i].append(elm[i])

                # test
                #print(f'{i}: {sequences[i]}')

        
        standard = ''
        A_percent, T_percent, C_percent, G_percent = [], [], [], []
        for v in sequences.values():
            # Statistic about A, T, C, G in each colum(%)
            ATCG_statistic = {}
            
            for elm in v:
                ATCG_statistic.setdefault(elm, 0)
                ATCG_statistic[elm] += 1
            
            result_max = max(ATCG_statistic, key = lambda x:ATCG_statistic[x])
            standard += result_max

            A_percent.append(self.ATCG_percent(ATCG_statistic, 'A', v))
            T_percent.append(self.ATCG_percent(ATCG_statistic, 'T', v))
            C_percent.append(self.ATCG_percent(ATCG_statistic, 'C', v))
            G_percent.append(self.ATCG_percent(ATCG_statistic, 'G', v))

        statistic_csv = {'A': A_percent, 'T': T_percent, 'C': C_percent, 'G': G_percent}
        dirPath = os.path.dirname(output)
        statistic_path = os.path.join(dirPath, 'ATCG_statistic.csv')
        print('Generating ATCG statistic file...')
        df = pd.DataFrame(statistic_csv)
        df.to_csv(statistic_path)
        
        if limitation != 0:
            standard = standard[:limitation]

        print('Done')
        print(f'Total sequences: {total_number}.')
        time.sleep(1)

        print(f'\nGenerating result - {os.path.basename(output)}...')
        with open(output, 'w') as out:
            out.write(f'>Result_length_{len(standard)}\n{standard}\n')
        
        print(f'\nGenerating .csv file - {os.path.basename(database_path)}...')
        csv_data = {'name':csv_name, 'length':csv_len, 'sequence':csv_seq}
        df = pd.DataFrame(csv_data)
        df.to_csv(database_path)

        print('Done.')
