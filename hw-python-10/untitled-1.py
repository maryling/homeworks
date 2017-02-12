import re

def open_file():
    with open(file, 'r', encoding='utf-8') as f:
        text = f.read()
    return text

def find_reg():
    s = open_file()
    reg = r'Часовой пояс(.*?)\s+title="(.*?)">(.*?)'
    if re.search(reg, s):
        title = re.search(reg, s).group(2)
        return title

def print_data():
    data = find_reg()
    with open ('data.txt', 'w', encoding = 'utf-8') as f:
        f.write(data)
    return data

file = input()

print(print_data())