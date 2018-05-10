import telebot
import random
import flask
import re
from pymystem3 import Mystem
from pymorphy2 import MorphAnalyzer
import random
import conf

webhook_host = "anilotut.pythonanywhere.com"
webhook_port = "443"
webhook_url_base = "https://{}:{}".format(webhook_host, webhook_port)
webhook_url_path = "/{}/".format(conf.token)

bot = telebot.TeleBot(conf.token, threaded=False)

bot.remove_webhook()

bot.set_webhook(url=webhook_url_base+webhook_url_path)

app = flask.Flask(__name__)


def get_word_class(word):
    morph = Mystem()
    ana = morph.analyze(word)
    if 'analysis' in ana:
        gr = word['analysis'][0]['gr']
        word_class = gr.split('=')[0]
    return word_class


def dict_words():
    with open('1grams-3.txt', 'r', encoding='utf-8') as f:
        words_raw = f.readlines()
    words = []
    dictionary = {}
    for l in words_raw:
        word = re.sub(r'[^\w\s]+|[\d]+', r'', l).strip()
        words.append(word)
    for word in words:
        dictionary[word] = get_word_class(word)
    return dictionary


def inflect(word, form):
    m = MorphAnalyzer()
    prog = m.parse(word)[0]
    inflected = prog.inflect({form})
    return inflected.word


def reverse_dict():
    dictionary = dict_words()
    new_dictionary = {}
    for key in dictionary.keys():
        if dictionary[key] not in new_dictionary.keys():
            new_dictionary[dictionary[key]] = []
            new_dictionary[dictionary[key]].append(key)
        else:
            new_dictionary[dictionary[key]].append(key)
    return new_dictionary


def get_new_words(text):
    new_words = []
    dictionary = reverse_dict()
    for word in text:
        word_class = get_word_class(word)
        if word_class in dictionary.keys():
            new_word = random.choice(dictionary[word_class])
            new_words.append(new_word)
    return new_words


def get_new_text(text):
    m = MorphAnalyzer()
    new_words = get_new_words(text)
    new_text = []
    for word in text:
        form = []
        first = m.parse(word)[0]
        if first.tag.case != None:
            form.append(first.tag.case)
        if first.tag.number != None:
            form.append(first.tag.number)
        if first.tag.gender != None:
            form.append(first.tag.gender)
        if first.tag.person != None:
            form.append(first.tag.person)
        if first.tag.mood != None:
            form.append(first.tag.mood)
        if first.tag.tense != None:
            form.append(first.tag.tense)
        for new_word in new_words:
            new_text.append(inflect(new_word, form))
    return ' '.join(new_text)


@bot.message_handler(commands=['start', 'help'])
def info(message):
    user = message.chat.id

    bot.send_message(user, "Привет! Напиши какое-нибудь предложение.")


@bot.message_handler(content_types=['text'])
def print_new(message):
    text = message.text
    user = message.chat.id
    new_text = get_new_text(text)

    bot.send_message(user, new_text)


@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'ok'


@app.route(webhook_url_path, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


bot.polling(none_stop=True)
