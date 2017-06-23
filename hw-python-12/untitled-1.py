import re
file = input('Введите название файла ')

def read_file(): ## делим текст на предложения
    with open (file, 'r', encoding = 'utf-8') as f:
        text = f.read()
        sentences = re.split('\. |\\n|!|\?|»', text)
    return sentences

def count_words(): ## делим на слова и сохраняем те предложения, в которых больше 10 слов
    sentences = read_file()
    words = [i.split() for i in sentences]
    ten_words = [arr for arr in words if len(arr) > 10]   
    return ten_words

def print_capital(): ## в полученных предложениях находим слова с заглавной буквы и выписываем их в столбик
    words = count_words()
    all_words = [item for arr in words for item in arr]
    capital_words = [i for i in all_words if i.istitle()]
    capital_words = [i.strip('.,?-;:!()\n«»') for i in capital_words]
    return '\n'.join(capital_words)

print(print_capital())