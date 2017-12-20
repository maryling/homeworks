# Страница, при заходе пользователя на которую с определённого вами новостного ресурса с помощью urllib.request
# скачивается главная страница, все кириллические слова на ней транслитерируются в старую орфографию и показываются пользователю.
# Кроме того, на экран должна выводиться информация о том, какие 10 самых частотных слов присутствуют на странице в данный момент.

# При создании страницы обязательно использовать render_template и циклы и условия в html-шаблонах, как это описано здесь.

from flask import Flask
from flask import render_template, request
import urllib.request
import re
from bs4 import BeautifulSoup
import os


app = Flask(__name__)


def i_ten(string):
    ok = {'у', 'о', 'а', 'э', 'ы', 'ю', 'ё', 'я', 'е', 'и'}
    for i in range(len(string)-1):
        if string[i] == "и" and string[i+1] in ok:
            string = string[:i] + "i" + string[i+1:]
    return string


def bez(string):
    bez = re.compile(r"^(бес).*")
    cherez = re.compile(r"^(черес).*")
    chrez = re.compile(r"^(чрес).*")
    if bez.match(string):
        string.replace("бес", "без")
    elif cherez.match(string):
        string.replace("черес", "через")
    elif chrez.match(string):
        string.replace("чрес", "чрез")
    return string


def jer(string):
    ok = re.compile(r".*[бвгджзклмнпрстфхцчшщ]$")
    if ok.match(string):
        string += "ъ"
    return string


def get_dictionary():
    html_names = ['a', 'b', 'v', 'g', 'd', 'e', 'sch', 'z', 'i', 'k', 'l', 'm', 'n', 'o', 'p', 'po', 'pr', 'r', 's',
                  'sm', 't', 'u', 'f', 'x', 'c', 'ch', 'sh', 'ya']
    common_url = 'http://slovnik.narod.ru/old/slovar/'
    for letter in html_names:
        page = urllib.request.urlopen(common_url + letter + '.html')
        text = page.read().decode('utf-8')
        word_table = re.compile('<table border=1 width=100%>.*?</table>', flags=re.DOTALL)
        words = re.search(word_table, text)
        words = str(words.group(0))
        regTag = re.compile('<.*?>', re.DOTALL)
        regSpace = re.compile('\s\s+')
        words = regTag.sub("", words)
        words = regSpace.sub("\n", words)
        with open('dict.txt', 'a', encoding='utf-8') as f:
            f.write(words)
    return 'ok'


def translate_word(word):
    with open('dict.txt', 'r', encoding='utf-8') as f:
        dictionary = f.read()
        needed_word = re.search('^' + word + '\n(.*?)\n', dictionary)
        if needed_word != None:
            translated_word = str(needed_word.group(1))
        else:
            translated_word = bez(word)
            translated_word = jer(translated_word)
            translated_word = i_ten(translated_word)
    return translated_word


@app.route('/')
def index():
    source = urllib.request.Request("https://yandex.ru/pogoda/skopje")
    with urllib.request.urlopen(source) as response:
        weather = response.read().decode("utf-8")
    r_temp = re.compile('<div class="temp fact__temp">.*?</div>', flags=re.DOTALL)
    r_clouds = re.compile('<div class="fact__condition.*?>.*?</div>', flags=re.DOTALL)
    temp_skopje = re.search(r_temp, weather)
    clouds_skopje = re.search(r_clouds, weather)
    skopje = str(temp_skopje.group(0) + clouds_skopje.group(0))
    regTag = re.compile('<.*?>', re.DOTALL)
    weather = regTag.sub("", skopje)
    if request.args:
        word = request.args['word']
        translated_word = translate_word(word)
        return render_template('result.html', word=translated_word)
    else:
        return render_template('main.html', weather=weather)


@app.route('/news')
def news():
    page = urllib.request.urlopen('http://www.pravoslavie.ru/')
    text = page.read().decode('utf-8')
    beautiful_text = BeautifulSoup(text, 'html.parser')
    news = beautiful_text.get_text()
    latin = re.compile(r'([a-zA-Z])')
    news = latin.sub("", news)
    news = re.compile(r'[(),[\]\\;:{}"?!*/<>=0-9_\'\r\n]').sub(" ", news)
    news = re.compile(r'\s\s+').sub(" ", news)
    with open("news.txt", 'w', encoding='utf-8') as f:
        f.write(news)
    os.system("C:" + os.sep + "mystem.exe -di news.txt newsmstm.txt")
    with open("newsmstm.txt", 'r', encoding='utf-8') as f:
        news = f.read()
    mstm_tags = re.compile('{.*?}', re.DOTALL)
    plain_news = mstm_tags.sub(" ", news)
    plain_news = re.compile(r'\s\s+').sub(" ", plain_news)
    arr = plain_news.split(" ")
    fin_news = []
    for word in arr:
        old_word = translate_word(word)
        fin_news.append(old_word)
        print(fin_news)
    return render_template('news.html', news=" ".join(fin_news))


@app.route('/test')
def test():
    correct = 0
    yat = ['colour', 'century', 'log', 'honey', 'note']
    nyat = ['dream', 'throw', 'lion', 'ban', 'family']
    if request.args:
        for i in yat:
            if request.args[i] == 'yat':
                correct += 1
        for w in nyat:
            if request.args[i] == 'nyat':
                correct += 1
        return render_template('testresults.html', result=correct)
    else:
        return render_template('test.html')


if __name__ == '__main__':
    app.run(debug=True)