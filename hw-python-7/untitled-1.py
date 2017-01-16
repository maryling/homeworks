fname = input("Введите название файла ")

def read_file():
    with open (fname, 'r', encoding = 'utf-8') as f:
        text = f.read()
        text = text.lower()
        words = text.split()
        for i in range(len(words)):
            words[i] = words[i].strip('.,?-;:!()""')
    return words        

def print_ness():
    ness = []
    words = read_file()
    for i in range(len(words)):
        if words[i][-4:] == "ness":
            ness.append(words[i])
    return ness

def not_repeating_ness():
    ness = print_ness()
    not_repeating_ness = []
    for i in range(len(ness)):
        if ness[i] not in not_repeating_ness:
            not_repeating_ness.append(ness[i])
    return not_repeating_ness


def freq():
    ness = print_ness()
    nr_ness = not_repeating_ness()
    words_freq = []
    for a in range(len(nr_ness)):
        freq = 0
        word = nr_ness[a]
        for i in range(len(ness)):
            if ness[i] == word:
                freq+=1
        words_freq.append(freq)
    return words_freq

def most_freq():
    frq = freq()
    ness = not_repeating_ness()
    x = frq[0]
    a = 1
    for i in range(len(frq)):
        if frq[i] > x:
            x = frq[i]
            a = i
    return ness[a]

print("Количество разных существительных с суффиксом -ness:", len(not_repeating_ness()))
print("Слово с максимальной частотностью:", most_freq())
            