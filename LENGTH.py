import os
import sys
import time
import numpy as np
import matplotlib as plt

class LENGTH():
    def __init__(self) -> None:
        pass

#             | Method               | Variables
    def LENGTH(self, input_checking, clock, inputFolder, output, files, total_number):
        if input_checking(inputFolder) == False:
            sys.exit()

        start = time.time()
        print('Mode: length')
        time.sleep(1)
        
        L_dict = {}
        sequence_len = 0

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
