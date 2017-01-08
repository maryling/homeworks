# пирожок: таТА таТА таТА таТАта / таТА таТА таТА таТА repeat
# варианты: клитика(та) сущ(ТА) сущ(таТА) сущ(ТАта) сущ(таТАта) гл(таТА) гл(таТАта)
import random
def clitic():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[0]
        line = line.strip()
        clitic = line.split(' ')
        return random.choice(clitic)

def nom1():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[1]
        line = line.strip()
        nom1 = line.split(' ')
        return random.choice(nom1)
    
def gen1():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[2]
        line = line.strip()
        gen1 = line.split(' ')
        return random.choice(gen1)
    
def nom2():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[3]
        line = line.strip()
        nom2 = line.split(' ')
        return random.choice(nom2)
    

def gen2():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[4]
        line = line.strip()
        gen2 = line.split(' ')
        return random.choice(gen2)
    
def nom3():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[5]
        line = line.strip()
        nom3 = line.split(' ')
        return random.choice(nom3)
    
def verb1():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[6]
        line = line.strip()
        verb1 = line.split(' ')
        return random.choice(verb1)
    
def verb2():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[7]
        line = line.strip()
        verb2 = line.split(' ')
        return random.choice(verb2)
    
def verb3():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[8]
        line = line.strip()
        verb3 = line.split(' ')
        return random.choice(verb3)
    
def dat():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[9]
        line = line.strip()
        dat = line.split(' ')
        return random.choice(dat)

def verb4():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[10]
        line = line.strip()
        verb4 = line.split(' ')
        return random.choice(verb4)
    
def acc1():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[11]
        line = line.strip()
        acc = line.split(' ')
        return random.choice(acc)
    
def acc2():
    with open('words.txt','r', encoding = 'utf-8') as f:
        lines = f.readlines()
        line = lines[12]
        line = line.strip()
        acc = line.split(' ')
        return random.choice(acc)
    
def verse1():
    return clitic() + ' ' + nom1() + ' ' + gen1() + ' ' + nom2() + ' ' + gen2()

def verse2():
    return nom3() + ' ' + verb1() + ' ' + nom3() + ' ' + verb1()

def verse3():
    return clitic() + ' ' + verb2() + ' ' + acc2() + ' ' + nom2() + ' ' + verb3()

def verse4():
    return nom3() + ' ' + dat() + ' ' + verb4() + ' ' + acc1()

def half_1():
    verse = random.choice([1,2])
    if verse == 1:
            return verse1()
    else:
            return verse3()
        
def half_2():
    verse = random.choice([1,2])
    if verse == 1:
            return verse2()
    else:
            return verse4()

for n in range(2):
    print(half_1())
    print(half_2())