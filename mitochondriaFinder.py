holy_img = '''
                                            ;@#@@$|;'`.                                            `
                                            ;@#############&|:`                                    `
                                            ;@####################|`                               `
                                            ;@####################@@##$:                           `
                                            :@#@#########################@!.                       `
                                      .%####$;::;$###########################|.                    `
                                      .%####|    |#############################&:                  `
                       .;&#%.         .%####|    |###########$!$##################|.               `
                    '&##@##@$`        `%####|    |#@@#######%.    '$################|              `
                 `%##########&: `:|&########|     .`:%#####%.        `$##############@;            `
                  :&#############@@#########|                       .%###############@@$'          `
                   '$#######################|                      .|###################@!.        `
                    `$#############@########%.                    .|######################$`       `
                   !##############@|'       :@#####&!'             .!@#####################&`      `
       .%@;.     |#############%`           ;######@@###$`            ;@##################@@&'     `
      :&#####&:|##########@#&:              ;@#############$.           ;@#&;`   |###########&:    `
     |########@###########&'                :@#############@#$`                   '&##########&'   `
    !####################|.                 :@################@;                   '&##########$`  `
   ;@@@#################!                   :@##################|                   ;@##########|  `
     '$@###############!                    :@##################@;               ;&#############@: `
        .%############$`                    :@###################$`           `$#@###############%.`
        `$############|                     :@###################&'            |#################@:'
        |#############|                     :@###################@:            '&#################|:
       `$#############|.                    :@###################&'             |#################$!
   ...`%##############&'                    :@#################@#%.             '$################@%
&######################$.                   :@##################&:                      |##########$
&#######################|                   :@#################@;                       ;@#########$
&#######################@:                  :@#################%.                       :@#########$
&########################|                  ;@#################!                        !##########$
@########################|                  ;@#########@@@@#@#@;                       `%##########$
       ;@###############$`    `::`          :@####@@###$:';&###&'               '&################@%
       .%##############|    `$#@@###$;`.    ;@@##&|:        ;@##@:             .%#################$!
        !#############&:    `$#######@@@#%. :@@;            |####|.            ;@#################|'
        .%#############&:    :@#@@@##@%'    :@##@!`        '$#@@%`            .%#################@:'
        :$##############&:    .::`.        :;;&######@%!:;$##@@%.             '$#################%.`
    .;@##################|                ;@! `&######@@#@#####!                 '%##@##########&: `
   '&@@###################!              `$#!  !#########@#@@#|                     |###########|  `
    :@#####################&!'`:!|'      '' :@$!&#####$``;!;'                      ;@##########$`  `
     :@#####################@#@@#|          ;&@########|                          |###########&'   `
      `$#@##@|.'%#############@#$`          ;@########@$'              '%###$'  .%###########&:    `
       .|$:      '$#############%.       .  ;@#$|&##@@#&:            `$#####################&'     `
                   `%###########!  .'.  |!  ;##%:%#&;$##|          '$######################&'      `
                    '$######################|.                     ;######################%.       `
                   |########################|.                      '&##################@!         `
                  %################@@#######|           `;:.         `$##############@@%`          `
                 .|##@#####@#%.   `:|$@#####|    '|&####@&#$        .|@############@@&'            `
                     :&###@@|.        .%####|    |##########&'   `%##@###########@@&:              `
                        `|@|          .%####|    |############@@#################&:                `
                                      .$#@@#|    |###########################@#%`                  `
                                       :|%$&$$&&&###########################$'                     `
                                            :@#@######################@@#$'                        `
                                            :@###################@###$;.                           `
                                            :@############@@####@|'                                `
                                            ;@#@@########@%;'.                                     `
'''
holy_words = [ 
'\t"There is no truth in flesh, only betrayal."', 
'\t"There is no strength in flesh, only weakness."', 
'\t"There is no constancy in flesh, only decay."', 
'\t"There is no certainty in flesh but death."', 
'\t??? Credo Omnissiah\n'
]

import os
import time
import argparse
from LENGTH import *
from FINDER import *
from SEARCH import *
from CLASSIFY import *

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



# main
if __name__ == '__main__':
    # We shall praise the great Omnissiah!
    print(holy_img)
    for holy_word in holy_words:
        print(holy_word)
        time.sleep(1)

    parse = argparse.ArgumentParser()
    parse.add_argument('-M', '--MODE', required=True, type=str, choices=['length', 'finder', 'search', 'classify'])
    parse.add_argument('-I', '--INPUT_FOLDER_PATH', type=str)
    parse.add_argument('-O', '--OUTPUT_FILE_PATH', type=str)
    parse.add_argument('-Data', '--OLD_DATA_CSV_COLLECTIONS_PATH', type=str)
    parse.add_argument('-L', '--LENGTH', type=int, default=0)
    args =parse.parse_args()

    inputFolder = args.INPUT_FOLDER_PATH
    output = args.OUTPUT_FILE_PATH
    database_path = args.OLD_DATA_CSV_COLLECTIONS_PATH
    mode = args.MODE
    limitation = args.LENGTH

    LENGTH = LENGTH()
    FINDER = FINDER()
    SEARCH = SEARCH()
    CLASSIFY = CLASSIFY()

    total_number = 0
    files = os.listdir(inputFolder)

    # length
    # -M length -I ../<folder> -O ../<file>
    if mode == 'length':
        start = time.time()

        LENGTH.LENGTH(input_checking, inputFolder, output, files, total_number)

        end = time.time()
        TIME = clock(end - start)
        print(f'\nTime spend: {TIME}s')

    # finder
    # -M finder -I ../<folder> -O ../<file> or <folder> -Data(no need if base on single file) ../<file> -L 0
    if mode == 'finder':
        start = time.time()

        FINDER.FINDER(input_checking, database_checking, inputFolder, output, database_path, limitation, files, total_number)
        
        end = time.time()
        TIME = clock(end - start)
        print(f'\nTime spend: {TIME}s')

    # search
    # -M search -Data ../<file>
    if mode == 'search':
        start = time.time()

        SEARCH.SEARCH(database_checking, int_input_checking, write_to_local_file, database_path)
        
        end = time.time()
        TIME = clock(end - start)
        print(f'\nTime spend: {TIME}s')
    
    # classify
    # -M classify -Data ../.. -O ../<folder>
    if mode == 'classify':
        start = time.time()

        CLASSIFY.CLASSIFY(database_checking, database_path, output)
        
        end = time.time()
        TIME = clock(end - start)
        print(f'\nTime spend: {TIME}s')
    
