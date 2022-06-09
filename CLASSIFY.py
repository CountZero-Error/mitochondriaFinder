import os
import sys
import time
import pandas as pd

class CLASSIFY():
    def __init__(self) -> None:
        pass

    #                 | Method           | Variables
    def CLASSIFY(self, database_checking, database_path, output):
        if database_checking(database_path) == False:
            sys.exit()
        
        try:
            os.makedirs(output)
        except FileExistsError:
            pass

        print('Mode: classify')
        time.sleep(1)

        infos = {}
        print(f'Reciciving info from {os.path.basename(database_path)}...')
        df = pd.read_csv(database_path)
        
        # Recive a dictionary
        i = 0
        for elm in df['length']:
            infos.setdefault(elm, [])
            infos[elm].append(f'{df["name"][i]}\n{df["sequence"][i]}\n\n')

            i += 1

        print('Done.')
        tmp = []
        for k in infos.keys():
            tmp.append(k)

        print(f'Find length*{len(infos.keys())}: {tmp}')

        print('\nGenerating result...')
        for k, v in infos.items():
            with open(os.path.join(output, f'{k}.fasta'), 'w') as out:
                for elm in v:
                    out.write(elm)
        
        print('Done.')
