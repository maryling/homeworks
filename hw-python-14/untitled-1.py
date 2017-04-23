import os
import re

a = 0
for root, dirs, files in os.walk('.'):
    for d in dirs:
        cyrillic = re.match(u'[а-яА-Я]+', d)
        other = re.search(r'[a-zA-Z\d.-_:"()=]', d)
        if cyrillic != None and other == None:
            a += 1
print(a)
