import sys
import csv
import time

class SEARCH():
    def __init__(self) -> None:
        pass

#             | Method                                                           | Variables
    def SEARCH(self, database_checking, int_input_checking, write_to_local_file, clock, database_path):
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
