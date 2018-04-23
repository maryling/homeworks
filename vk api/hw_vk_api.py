import urllib.request
import json
import sqlite3
import datetime
import matplotlib.pyplot as plt


def list_posts():
    req = urllib.request.Request("https://api.vk.com/method/wall.get?owner_id=-102652602&count=100&v=5.73&access_token=b6115d00b6115d00b6115d0015b673718fbb611b6115d00ecd0bed6fb1fbee7bdd1987a")
    response = urllib.request.urlopen(req)
    result = response.read().decode('utf-8')
    return result


def get_texts():
    result = list_posts()
    data = json.loads(result)
    texts = {}
    for i in range(100):
        texts[data["response"]["items"][i]["id"]] = data["response"]["items"][i]["text"]
    return texts


def get_signer_ids():
    result = list_posts()
    data = json.loads(result)
    signer_ids = {}
    for i in range(100):
        if "signer_id" in data["response"]["items"][i]:
            signer_ids[data["response"]["items"][i]["id"]] = data["response"]["items"][i]["signer_id"]
    return signer_ids


def get_posts_id():
    posts = list_posts()
    data = json.loads(posts)
    posts_id = []
    for i in range(100):
        posts_id.append(data["response"]["items"][i]["id"])
    return posts_id


def get_comments(post_id):
    req = urllib.request.Request(str.format("https://api.vk.com/method/wall.getComments?owner_id=-102652602&post_id={0}&count=100&v=5.73&access_token=b6115d00b6115d00b6115d0015b673718fbb611b6115d00ecd0bed6fb1fbee7bdd1987a", post_id))
    response = urllib.request.urlopen(req)
    result = (response.read().decode('utf-8'))
    comments = []
    data = json.loads(result)
    if data["response"]["count"] != 0:
        for i in range(data["response"]["count"]):
            comments.append(data["response"]["items"][i]["text"])
    return comments


def get_comments_authors(post_id):
    authors_id = {}
    req = urllib.request.Request(str.format("https://api.vk.com/method/wall.getComments?owner_id=-102652602&post_id={0}&count=100&v=5.73&access_token=b6115d00b6115d00b6115d0015b673718fbb611b6115d00ecd0bed6fb1fbee7bdd1987a", post_id))
    response = urllib.request.urlopen(req)
    result = (response.read().decode('utf-8'))
    data = json.loads(result)
    for i in range(data["response"]["count"]):
        authors_id[data["response"]["items"][i]["text"]] = data["response"]["items"][i]["from_id"]
    return authors_id


def posts_to_db():
    posts_id = get_posts_id()
    print(posts_id)
    texts = get_texts()
    signer_ids = get_signer_ids()
    print(signer_ids)
    conn = sqlite3.connect('today_i_heard.db')
    c = conn.cursor()
    c.execute("CREATE TABLE posts(post_id, text)")
    for p_id in texts:
        text = texts[p_id]
        c.execute("INSERT INTO posts VALUES(?, ?)", (p_id, text))
    c.execute("ALTER TABLE posts ADD author TEXT DEFAULT 0")
    conn.commit()
    for p_id in posts_id:
        if p_id in signer_ids.keys():
            author = signer_ids[p_id]
            c.execute("UPDATE posts SET author=? WHERE post_id=?", (author, p_id))
    conn.commit()
    conn.close()
    return "ok"


def comments_to_db():
    posts_id = get_posts_id()
    conn = sqlite3.connect('today_i_heard.db')
    c = conn.cursor()
    c.execute("CREATE TABLE comments(post_id, comment_text)")
    for p_id in posts_id:
        comments = get_comments(p_id)
        if comments != []:
            for comment in comments:
                c.execute("INSERT INTO comments VALUES(?, ?)", (p_id, comment))
    c.execute("ALTER TABLE comments ADD author TEXT DEFAULT 0")
    for p_id in posts_id:
        comments = get_comments(p_id) # список комментов одного поста
        authors_id = get_comments_authors(p_id) # словарь авторов всех комментов одного поста
        if comments != []:
            for comment in comments:
                author = authors_id[comment]
                c.execute("UPDATE comments SET author=? WHERE comment_text=?", (author, comment))
    conn.commit()
    conn.close()
    return "ok"


def count_posts_len():
    conn = sqlite3.connect('today_i_heard.db')
    c = conn.cursor()
    posts = c.execute("SELECT post_id, text FROM posts").fetchall()
    c.execute("ALTER TABLE posts ADD length FLOAT DEFAULT 0")
    conn.commit()
    for i in range(len(posts)):
        post_len = len(posts[i][1])
        c.execute("UPDATE posts SET length=? WHERE post_id=?", (post_len, posts[i][0]))
    conn.commit()
    conn.close()
    return "ok"


def count_comments_len(post_id):
    conn = sqlite3.connect('today_i_heard.db')
    c = conn.cursor()
    comments = c.execute("SELECT comment_text FROM comments WHERE post_id=?", post_id).fetchall()
    comments_len = 0
    for i in range(len(comments)):
        comments_len += len(comments[i])
    av_comments_len = comments_len / len(comments)
    print(av_comments_len)
    return av_comments_len


def len_comments_to_db():
    conn = sqlite3.connect('today_i_heard.db')
    c = conn.cursor()
    posts = get_posts_id()
    c.execute("ALTER TABLE posts ADD av_comm_len FLOAT DEFAULT 0")
    for p_id in posts:
        av_comm_len = count_comments_len(p_id)
        c.execute("UPDATE posts SET av_comm_len=? WHERE post_id=?", (av_comm_len, p_id))
    conn.commit()
    conn.close()
    return "ok"


def get_bday():
    signer_ids = get_signer_ids()
    signers_bday = {}
    for i in signer_ids:
        req = urllib.request.Request("https://api.vk.com/method/users.get?user_ids={}&fields=bdate&v=5.73&access_token=b6115d00b6115d00b6115d0015b673718fbb611b6115d00ecd0bed6fb1fbee7bdd1987a".format(i))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        print(data)
        if "bdate" in data["response"][0]:
            signers_bday[i] = (data["response"][0]["bdate"])
    return signers_bday


def get_city():
    signer_ids = get_signer_ids()
    signers_city = {}
    for i in signer_ids:
        req = urllib.request.Request(
            "https://api.vk.com/method/users.get?user_ids={}&fields=city&v=5.73&access_token=b6115d00b6115d00b6115d0015b673718fbb611b6115d00ecd0bed6fb1fbee7bdd1987a".format(
                i))
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        data = json.loads(result)
        if "city" in data["response"][0]:
            signers_city[i] = (data["response"][0]["city"]["title"])
    return signers_city


def count_age(bday):
    now = datetime.datetime.now()
    date = bday.split(".")
    if len(date) == 3:
        day = int(date[0])
        month = int(date[1])
        year = int(date[2])
        if month <= now.month and day < now.day:
            age = now.year - (year + 1)
        else:
            age = now.year - year
    else:
        age = 0
    return age


def authors_to_db():
    bdays = get_bday()  # словарь автор: др
    cities = get_city()  # словарь автор: город
    conn = sqlite3.connect('today_i_heard.db')
    c = conn.cursor()
    c.execute("CREATE TABLE people(author, age)")
    conn.commit()
    for author in bdays.keys():
        age = count_age(bdays[author])
        c.execute("INSERT INTO people VALUES (?, ?)", (author, age))
    c.execute("ALTER TABLE people ADD city TEXT DEFAULT 0")
    for author in cities.keys():
        city = cities[author]
        c.execute("UPDATE people SET city=? WHERE author=?", (city, author))
    conn.commit()
    conn.close()
    return "ok"


def av_len_age():
    conn = sqlite3.connect("today_i_heard.db")
    c = conn.cursor()
    ages = c.execute("SELECT age FROM people").fetchall()
    print(ages)
    authors_age = {}
    for age in ages:
        authors_age[age] = c.execute("SELECT author FROM people WHERE age=?", age).fetchall()
    print(authors_age)
    for age in authors_age:
        authors_len = {}
        for author in authors_age[age]:
            authors_len[author] = c.execute("SELECT length FROM posts WHERE author=?", author).fetchall()
        authors_age[age] = authors_len
    print(authors_age)
    return authors_age


def av_len_city():
    conn = sqlite3.connect("today_i_heard.db")
    c = conn.cursor()
    cities = c.execute("SELECT city FROM people").fetchall()
    authors_city = {}
    for city in cities:
        authors_city[city] = c.execute("SELECT author FROM people WHERE city=?", city).fetchall()
    print(authors_city)
    for city in authors_city:
        authors_len = {}
        for author in authors_city[city]:
            authors_len[author] = c.execute("SELECT length FROM posts WHERE author=?", author).fetchall()
        authors_city[city] = authors_len
    print(authors_city)
    return authors_city


def draw_len_age():
    authors_age = av_len_age()
    age = authors_age.keys()
    length = []
    for key in age:
        length.append(age[key])
    plt.ylabel('Средняя длина поста')
    plt.xlabel('Возраст автора поста')
    plt.bar(age, length)
    plt.show()
    return "ok"


def draw_len_city():
    authors_city = av_len_city()
    cities = authors_city.keys()
    length = []
    for key in cities:
        length.append(cities[key])
    plt.ylabel('Средняя длина поста')
    plt.xlabel('Город автора поста')
    plt.bar(cities, length)
    plt.show()
    return "ok"


def main():
    posts_to_db()
    count_posts_len()
    comments_to_db()
    len_comments_to_db()
    authors_to_db()
    draw_len_age()
    draw_len_city()


if __name__ == "__main__":
    main()