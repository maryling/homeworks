import re

def open_file():
    with open(file, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()
    return lines


def count_lines():
    lines = open_file()
    length = len(lines)
    with open ('lines.txt', 'w', encoding = 'utf-8') as f:
        f.write (str(length))
    return length

file = "F.xml"

print(count_lines())


def counter(element):
    lines = open_file()
    num = 0
    for i in range (count_lines()):
        if element in lines[i]:
            num += 1
    return num

def create_dic():
    with open(file, 'r', encoding = 'utf-8') as f:
        text = f.read()
    arr = []
    reg = r'lemma="(.*?)"\stype="(.*?)"'
    for i in range(count_lines()):
        if re.search(reg, text) != None:
            m = re.search(reg, text).group(2)
            arr.append(m)
    keys = []
    for i in range(len(arr)):
        if arr[i] not in keys:
            keys.append(arr[i])
    definitions = []
    for i in range(len(keys)):
        num = counter(keys[i])
        definitions.append(num)
    dic = dict(zip(keys, definitions))
    return dic

def print_dic():
    dic = create_dic()
    keys = dic.keys()
    keys = '\n'.join(keys)
    with open('dic.txt', 'w', encoding = 'utf-8') as f:
        f.write(keys)
    return keys
    
print(create_dic())
print(print_dic())
