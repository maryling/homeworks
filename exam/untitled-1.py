import os
import re

def read_file(file):
    with open (file, 'r', encoding='cp1251') as f:
        text = f.read()
    return text

def readlines_file(file):
    with open (file, 'r', encoding='cp1251') as f:
        text = f.readlines()
    return text

def count_se(text):
    se = '<se>(.*?)</se>'
    count_se = len(re.findall(se, text))
    return count_se

def find_author(text):
    author = r'<meta content="(.*?)" name="author"><\/meta>'
    for line in text:
        if author in line:
            author_f = re.match(author, text).group(1)
    return author_f
    
def find_topic(text):
    topic = '<meta content="(.*?)" name="topic"><\/meta>'
    return re.match(topic, text).group(1)    

def main():
    ##Задание 1: обойти все файлы, для каждого файла посчитать кол-во предложений, записать в словарь
    dic = {}
    for root, dirs, files in os.walk('.'):
        dic = {f: str(count_se(read_file(os.path.join(root, f)))) for f in files}
    array = [i+'\t'+dic[i] for i in dic.keys()]
    with open ('number of sentences.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(array))
    ##Задание 2: обойти все файлы, из каждого достать автора и тематику, записать в строку через ','
    for root, dirs, files in os.walk('news'):
        for f in files:           
            with open ('author and topic.csv', 'a', encoding='utf-8') as file:
                file.write(os.path.join(root, f) + '\t' + find_author(readlines_file(os.path.join(root, f))) + '\t' + find_topic(readlines_file(os.path.join(root, f))) + '\n')


if __name__ == '__main__':
    main()