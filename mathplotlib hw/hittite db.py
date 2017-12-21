# Таблица называется wordforms, имена полей: Lemma, Wordform, Glosses.

# Нужно извлечь из неё данные и на них построить новую многотабличную реляционную базу с тремя таблицами:
# слова (id, Lemma, Wordform, Glosses), глоссы (id, обозначение, расшифровка) и слова-глоссы (id слова, id глоссы).
# Глоссы из соответствующего поля требуется разбить на отдельные элементы (разбиваются по точке).

# Нужно посчитать и визуализировать на графике все глоссы. Нужно подсчитать, каких из этих глосс в базе больше:
# лучше подсчитать число падежей отдельно, число частей речи -- отдельно.
# Отдельный график для падежей, отдельный график для частей речи и т. д.


import sqlite3
import matplotlib.pyplot as plt
import re


def copy_to_new_db():
    wordforms = sqlite3.connect("hittite.db")
    glossed = sqlite3.connect("glossed_hittite.db")
    w = wordforms.cursor()
    g = glossed.cursor()
    all = w.execute("SELECT * FROM wordforms").fetchall()
    for i in range(len(all)):
        g.execute("INSERT INTO wordforms VALUES (?, ?, ?, ?)", (i, all[i][0], all[i][1], all[i][2]))
    glossed.commit()
    wordforms.commit()
    glossed.close()
    wordforms.close()
    return "ok"


def make_gloss_table():
    with open("Glossing_rules.txt", "r", encoding="utf-8") as f:
        glosses = f.read()
    glosses_arr = glosses.split("\n")
    glosses_dict = {}
    for i in glosses_arr:
        arr = i.split(" — ")
        glosses_dict[arr[0]] = arr[1]
    glossed = sqlite3.connect("glossed_hittite.db")
    g = glossed.cursor()
    i = 0
    for gloss in glosses_dict:
        g.execute("INSERT INTO glosses VALUES (?, ?, ?)", (i, gloss, glosses_dict[gloss]))
        i += 1
    glossed.commit()
    glossed.close()
    return "ok"


def get_ids():
    glossed = sqlite3.connect("glossed_hittite.db")
    g = glossed.cursor()
    wordforms = g.execute("SELECT id, glosses FROM wordforms").fetchall()
    glosses = g.execute("SELECT id, обозначение FROM glosses").fetchall()
    gloss_dict = {}
    id_dict = {}
    for i in range(len(glosses)):
        definition = glosses[i][1]
        gloss_dict[definition] = glosses[i][0]
    for wordform in range(len(wordforms)):
        wordform_glosses = wordforms[wordform][1]
        gloss_arr = []
        gloss_id_arr = []
        gloss_arr.append([gloss for gloss in wordform_glosses.split('.') if gloss.isupper() is True])
        for gloss in gloss_arr:
            if gloss in gloss_dict.keys():
                gloss_id_arr.append(gloss_dict[gloss])
            elif re.search(re.compile("\d.*", re.DOTALL)):
                length = len(g.execute("SELECT id FROM glosses").fetchall())
                g.execute("INSERT INTO glosses VALUES (?, ?, ?)", (length, gloss, "P&N"))
                gloss_dict[gloss] = length
                gloss_id_arr.append(gloss_dict[gloss])
            else:
                length = len(g.execute("SELECT id FROM glosses").fetchall())
                g.execute("INSERT INTO glosses VALUES (?, ?, ?)", (length, gloss, "case"))
                gloss_dict[gloss] = length
                gloss_id_arr.append(gloss_dict[gloss])
        id_dict[wordforms[wordform][0]] = gloss_id_arr
        g.execute("INSERT INTO ids VALUES (?, ?)", (wordforms[wordform][0], ", ".join(gloss_id_arr)))
    glossed.commit()
    glossed.close()
    return id_dict


def count_gloss(dic):
    glossed = sqlite3.connect("glossed_hittite.db")
    g = glossed.cursor()
    number_dict ={}
    for i in dic.keys():
        for id in dic[i]:
            gloss = g.execute("SELECT обозначение FROM glosses WHERE id=?", (id,)).fetchone()
            if gloss not in number_dict.keys():
                number_dict[gloss] = 0
            else:
                number_dict[gloss] += 1
    glossed.commit()
    glossed.close()
    return number_dict


def make_graph(gloss_dict):
    glosses = gloss_dict.keys()
    number = []
    for gloss in gloss_dict.keys():
        number.append(gloss_dict[gloss])
    plt.ylabel('количество вхождений')
    plt.xlabel('глоссы')
    plt.bar(gloss, number)
    plt.show()
    return "ok"


def main():
    copy_to_new_db()
    make_gloss_table()

    glossed = sqlite3.connect("glossed_hittite.db")
    g = glossed.cursor()
    pos = {}
    case = {}
    pn = {}
    number_dict = count_gloss(get_ids())
    item_of_pos = g.execute("SELECT FROM glosses WHERE расшифровка=?", ("POS",)).fetchall()
    item_of_case = g.execute("SELECT FROM glosses WHERE расшифровка=?", ("case",)).fetchall()
    item_of_pn = g.execute("SELECT FROM glosses WHERE расшифровка=?", ("P&N",)).fetchall()
    for i in item_of_pos:
        pos[i] = number_dict[i]
    for i in item_of_case:
        case[i] = number_dict[i]
    for i in item_of_pn:
        pn[i] = number_dict[i]
    glossed.commit()
    glossed.close()

    make_graph(pos)
    make_graph(case)
    make_graph(pn)


if __name__ == "__main__":
    main()


