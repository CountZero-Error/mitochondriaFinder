import os
import sys

class COMBINE():
    def __init__(self) -> None:
        pass

    def COMBINE(self, folder_path):
        while True:
            try:
                output_path = input('Please enter the path you want to generate combine standard file(file name no need):')

                files = os.listdir(folder_path)

                output = os.path.join(output_path, 'combine_standard.fasta')
                with open(output, 'w') as out:
                    print('Generating combine_standard.fasta:')
                    file_num = 0
                    for file in files:
                        file_num += 1
                        print(f'\tCurrent file - {file}')
                        with open(os.path.join(folder_path, file)) as filo:
                            for line in filo:
                                out.write(line)
                            out.write('\n')
                
                print(f'Done.\nTotal: {file_num}.')
                break
            except:
                pass

if __name__ == '__main__':
    folder_path = sys.argv[1]
    COMBINE = COMBINE()
    COMBINE.COMBINE(folder_path)
