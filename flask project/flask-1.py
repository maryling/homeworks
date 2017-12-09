from flask import Flask
from flask import render_template, request
import json


app = Flask(__name__)


@app.route('/')
def index():
    if request.args:
        data = request.args
        with open('results.txt', 'r+', encoding='utf-8') as f:
            content = f.read()
            dic = {}
            if content != '':
                dic = json.loads(content)
            if data["language"] not in dic:
                dic[data["language"]] = [{"fire": data["fire"], "nose": data["nose"], "go": data["go"],
                                          "water": data["water"], "mouth": data["mouth"], "tongue": data["tongue"],
                                          "blood": data["blood"], "bone": data["bone"], "you_sg": data["you_sg"],
                                          "root": data["root"], "come": data["come"], "breast": data["breast"],
                                          "rain": data["rain"], "i": data["i"], "name": data["name"],
                                          "louse": data["louse"], "wing": data["wing"]}]
            else:
                dic[data["language"]].append({"fire": data["fire"], "nose": data["nose"], "go": data["go"],
                                              "water": data["water"], "mouth": data["mouth"], "tongue": data["tongue"],
                                              "blood": data["blood"], "bone": data["bone"], "you_sg": data["you_sg"],
                                              "root": data["root"], "come": data["come"], "breast": data["breast"],
                                              "rain": data["rain"], "i": data["i"], "name": data["name"],
                                              "louse": data["louse"], "wing": data["wing"]})
            results = json.dumps(dic, ensure_ascii=False)
            f.seek(0)
            f.write(results)
        return render_template('thanks.html')
    return render_template('main.html')


@app.route('/json')
def write_json():
    with open('results.txt', 'r', encoding='utf-8') as f:
        content = f.read()
    return render_template('json.html', content=content)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.form:
        language = request.form['language']
        word_list = request.form.getlist('words_select')
        with open('results.txt', 'r', encoding='utf-8') as f:
            content = json.loads(f.read())
        print(content)
        if content[language]:
            results = []
            for i in content[language]:
                for word in word_list:
                    results.append(i[word])
            return render_template('results.html', query=language+": "+", ".join(word_list), results=", ".join(results))
        else:
            return render_template('results.html', query=language+": "+", ".join(word_list), results='ничего')
    return render_template('search.html')


@app.route('/stats')
def stats():
    with open('results.txt', 'r', encoding='utf-8') as f:
        content = json.loads(f.read())
    number_of_languages = len(content)
    number_of_informants = 0
    informants_by_language = {}
    for key in content.keys():
        if key != '':
            informants_by_language[key] = len(content[key])
        else:
            informants_by_language['без языка'] = len(content[key])
    for key in informants_by_language.keys():
        number_of_informants += informants_by_language[key]
    dic = str(informants_by_language)
    dic = dic.strip("{}")
    dic = dic.replace("'", "")
    return render_template('stats.html', number_of_informants=number_of_informants, number_of_languages=number_of_languages,
                           informants_by_language=dic)


if __name__ == '__main__':
    app.run(debug=True)
