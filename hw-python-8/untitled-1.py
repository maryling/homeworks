import random

file = "words.csv"

def create_d():
    with open(file, "r") as f:
        lines = f.readlines()
        arr1 = []
        arr2 = []
        for i in range(len(lines)):
            line = lines[i].strip()
            line = line.split(';')
            arr1.append(line[0])
            arr2.append(line[1])
        dic = dict(zip(arr1, arr2))
    return dic
        
def dots(word):
    dic = create_d()
    definition = dic[word].split(" ")
    if definition[0] == word:
        definition[0] = "." * len(word)
    elif definition[1] == word:
        definition[1] = "." * len(word)
    return ' '.join(definition)

def riddle():
    dic = create_d()
    word = dic.popitem()
    guess = input("Отгадайте слово: " + dots(word[0]) + " ")
    if guess == word[0]:
        return "Верно!"
    else:
        return "Неверно! Правильный ответ: " + word[0]
            
print(riddle())




