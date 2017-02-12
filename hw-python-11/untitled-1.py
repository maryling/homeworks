import re

def open_file():
    with open (file, 'r', encoding = 'utf-8') as f:
        text = f.read()
    return text

def find_and_replace():
    text = open_file()
    reg = re.sub(u'\b[Вв]икинг(и|у|а(м|ми|х)?|о[мв]|е)?\b', u'\\1', text)
    return reg

file = 'vikings.htm'
print(find_and_replace())
    