import numpy as np
from save_list import writelist

nodes = list(range(1, 2001))

lines = [nodes]

def is_single_node(lines):
    for line in lines:
        if len(line) > 1:
            return False
    return True

def cut(line_idx, lines: list):
    line = lines[line_idx]
    lines.pop(line_idx)

    if len(line) >= 3:
        if len(line) % 2 == 1:
            mid_pos = (len(line) - 1) // 2
        else:
            mid_pos = len(line) // 2
        line1 = line[:mid_pos]
        line2 = line[mid_pos+1:]
        lines.append(line1)
        lines.append(line2)
        return line[mid_pos]
    
    else:
        lines.append([line[1]])
        return line[0]

nodes_to_cut = []
while not is_single_node(lines):
    # Find the longest lines
    longest_line_idx = np.argmax(list(map(len, lines)))
    nodes_to_cut.append(cut(longest_line_idx, lines))

writelist(nodes_to_cut, "problem3-nodes.txt")
print('qwq')
