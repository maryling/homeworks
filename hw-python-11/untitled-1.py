import re

def open_file():
    with open (file, 'r', encoding = 'utf-8') as f:
        text = f.read()
    return text

def find_and_replace():
    text = open_file()
    reg = re.sub(r'викинг((и|а|ам|ами|ах|у|ов|ом|е)?)([\s,.!\?:"\(\)\'»])', r'бурундук\1\3', text)
    reg = re.sub(r'Викинг((и|а|ам|ами|ах|у|ов|ом|е)?)([\s,.!\?:"\(\)\'»])', r'Бурундук\1\3', reg)
    return reg

def print_text():
    text = find_and_replace()
    with open ('chipmunks.txt', 'w', encoding = 'utf-8') as f:
        f.write(text)
    return text

file = 'vikings.txt'
print(print_text())
    