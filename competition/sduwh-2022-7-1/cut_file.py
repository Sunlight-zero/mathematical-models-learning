import os

def cut_file(filename, path='./', num_lines=7):
    """
    Cut the first n lines of the file.
    """
    file_path = os.path.join(path, filename)
    with open(file_path, mode='r') as f:
        lines = f.readlines()
    
    with open(file_path, mode='w') as f:
        f.writelines(lines[num_lines:])

if __name__ == '__main__':
    import pandas as pd

    PATH = 'competition/sduwh-2022-7-1/'
    os.chdir(PATH)

    FILE = 'INFLUENCERS_0_lvl_4.txt'
    cut_file(FILE)
