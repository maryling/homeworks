import os
import re

def num_files():
    files = [i for i in os.listdir('.') if re.search(r'[0-9]', i) == None]
    
    return len(files)

def list_files():
    files = [i for i in os.listdir('.') if re.search(r'[0-9]', i) == None]
    list_files = []
    for i in files:
        i2 = i.split('.')
        if i2[0] not in list_files:
            list_files.append(i2[0])
    return list_files


print(num_files(), list_files())