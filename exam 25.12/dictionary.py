# 1. (5 баллов) Скачать отсюда архив страниц интернет-сайта с тайско-английским словарём. Извлечь с каждой страницы пары
# "тайское слово -- английское слово" и поместить их в питоновскую структуру данных типа "словарь",
# где ключом будет тайское слово, а значением - английское.

# 2. (8 баллов) Использовать структуру данных из предыдущего задания, записать её в файл формата json на диск,
#а также создать ещё одну структуру данных, где будет наоборот: английское слово ключ, а массив тайских слов - значение.
# Её тоже записать на диск в формате json.

# 3. (10 баллов) Создать на фласке веб-приложение "Англо-тайский словарь",
# где можно было бы в текстовом поле ввести английское слово
# и получить в качестве результата запроса - его перевод на тайский.

import re
import os
import json
from flask import Flask
from flask import render_template, request


def get_words():
    words_dict = {}
    regTag = re.compile('<.*?>', re.DOTALL)
    for file in os.listdir('.'):
        filename, file_extension = os.path.splitext('.' + os.sep + file)
        if file_extension == '.html':
            with open(file, 'r', encoding='utf-8') as f:
                text = f.read()
                words = re.compile('<td class=th>(.*?)</td><td>(.*?)</td><td class=pos>(.*?)<td>(.*?)</td>',
                                   flags=re.DOTALL)
                all_words = re.findall(words, text)
                if all_words is not None:
                    print(all_words)
                    for i in range(len(all_words)):
                        th_word = str(all_words[i][0])
                        th_word = regTag.sub("", th_word)
                        print(th_word)
                        e_word = str(all_words[i][3])
                        e_word = regTag.sub("", e_word)
                        e_word = e_word.split("; ")
                        print(e_word)
                    words_dict[th_word] = e_word
    return words_dict


def make_json(text, file):
    jsoned = json.dumps(text, ensure_ascii=False)
    with open(file, 'w', encoding='utf-8') as f:
        f.write(jsoned)
    return jsoned


def make_dictionaries():
    words = get_words()
    make_json(words, "TEdict.json")
    ETdict = {}
    for th_word in words.keys():
        for i in words[th_word]:
            ETdict[i] = th_word
    make_json(ETdict, "ETdict.json")


print(make_dictionaries())


app = Flask(__name__)


@app.route('/')
def index():
    if request.args:
        word = request.args['word']
        with open('ETdict.json', 'r', encoding='utf-8') as f:
            dictionary = json.loads(f.read())
        if word in dictionary.keys():
            result = dictionary[word]
        else:
            result = 'None'
        return render_template("result.html", word=word, result=result)
    return render_template("dictionary.html")


if __name__ == '__main__':
    app.run(debug=True)
