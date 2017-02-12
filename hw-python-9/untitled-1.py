import re
file = input('Введите название файла ')

def read_file():
    with open (file, 'r', encoding = 'utf-8') as f:
        text = f.read()
        text = text.lower()
        words = text.split()
        for i in range(len(words)):
            words[i] = words[i].strip('.,?-;:!()""\n')
    return words 

def find_forms():    
    future = r'найд(ут?|е(шь|те?|м|я))(с[ья])?'
    future_participle = r'найденн(ы(й|ми?|х)|ая|о(е|й|го|му|ю)|ую)'
    future_participle_short = r'найден[аоы]'
    past = r'наш(л(а|и)|ел|едш(и(й|ми?|х)|ая|е(е|й|го|му|ю)|ую))(с[ья])?'
    s = read_file()
    wordforms = []
    for i in range(len(s)):
        result = re.search(future, s[i])
        if result != None:
            wordforms.append(result.group(0))
        else:
            result = re.search(future_participle, s[i])
            if result != None:
                wordforms.append(result.group(0))
            else:
                result = re.search(future_participle_short, s[i])
                if result != None:
                    wordforms.append(result.group(0))
                else:
                    result = re.search(past, s[i])
                    if result != None:
                        wordforms.append(result.group(0))                    
        
    return wordforms
    
def cross_out_doubles():
    wordforms = find_forms()
    final = []
    for i in range(len(wordforms)):
        if wordforms[i] not in final:
            final.append(wordforms[i])
    return '\n'.join(final)

print (cross_out_doubles())
