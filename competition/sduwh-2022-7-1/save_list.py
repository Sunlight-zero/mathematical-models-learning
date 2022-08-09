import os

def writelist(lst: list, filename: str, path: str='./'):
    with open(os.path.join(path, filename), 'w') as f:
        for t in lst:
            f.write(str(t) + '\n')

if __name__ == '__main__':
    PATH = 'competition\\sduwh-2022-7-1'
    FILENAME = 'list.txt'
    a = [1, 2, -3, 4.0, 5, None, 'awa', 'qwq', 3.1415926]
    writelist(a, FILENAME, PATH)
