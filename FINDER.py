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
    
    def SorM(self):
        answer = input('You want to generate a standard genome base on single file or multi files(s/m):')
        return answer
    
    def finder(self, P_list, output, limitation, total_number, database_path, csv_name, csv_len, csv_seq, answer):
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

        if answer.lower() == 'm':
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
        
        if answer.lower() == 'm':
            print(f'\nGenerating .csv file - {os.path.basename(database_path)}...')
            csv_data = {'name':csv_name, 'length':csv_len, 'sequence':csv_seq}
            df = pd.DataFrame(csv_data)
            df.to_csv(database_path)

        print('Done.')

    #               | Method                           | Variables
    def FINDER(self, input_checking, database_checking, inputFolder, output, database_path, limitation, files, total_number):
        if input_checking(inputFolder) == False:
            sys.exit()

        csv_name, csv_len, csv_seq = [], [], []

        print('Mode: finder')
        time.sleep(1)

        answer = self.SorM()
        while True:
            if answer.lower() == 's' or answer.lower() == 'm':
                break
            else:
                answer = self.SorM()
        
        if answer.lower() == 'm':
            if database_checking(database_path) == False:
                sys.exit()
        
        P_list = []
        head_tmp = ''
        file_num = 0
        for file in files:
            file_num += 1
            print(f'\nProcessing file {file_num} - {file}...')
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
            
            if answer.lower() == 's':
                print('Done.')
                time.sleep(1)

                # 'output' must be a folder path
                try:
                    os.makedirs(output)
                except FileExistsError:
                    pass
                tmp_output = os.path.join(output, f'standard_{file}')
                self.finder(P_list, tmp_output, limitation, total_number, database_path, csv_name, csv_len, csv_seq, answer)
            
        if answer.lower() == 'm':
            print('Done.')
            time.sleep(1)
            
            self.finder(P_list, output, limitation, total_number, database_path, csv_name, csv_len, csv_seq, answer)
        else:
            sys.exit()
