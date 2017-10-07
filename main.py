import re
import urllib.request
import os
import shutil



def write_to_file(file, text):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(text)


def crawl():
    for n in range(1, 718):
        try:
            source = urllib.request.Request("http://www.vecherniy.com/wall?id=" + str(n))
            with urllib.request.urlopen(source) as response:
                html = response.read().decode("utf-8")
                write_to_file(str(n) + ".txt", html)
        except:
            print("Error at http://www.vecherniy.com/wall?id=" + str(n))
            return


def find_created(text):
    created = re.search(r"<div>Время: (.*?)</div>", text, flags=re.DOTALL)
    if created != None:
        return created.group(1)
    else:
        return ''


def find_author(text):
    author = re.search(r"<div>Автор: (.*?)</div>", text, flags=re.DOTALL)
    if author != None and author != '<a href="author?user=" class="c_w"></a>':
        return author.group(1)
    else:
        return "Noname"


def find_header(text):
    header = re.search(r'<div class="f26 crd ovh myr_HelveticaNeue"(.*?)>(.*?)</div>', text, flags=re.DOTALL)
    if header != None:
        return header.group(2)
    else:
        return "None"


def find_main_text(text):
    main_text = re.search(r'<div id="material_text"(.*?)>(.*?)<!--подробный Текст-->', text, flags=re.DOTALL)
    if main_text != None:
        return main_text.group(2)
    else:
        return "None"


def make_mystem():
    lst = os.listdir('.')
    all_meta = get_meta_data()
    for index, file in enumerate(lst):
        dic = all_meta[index]
        all_meta = get_meta_data()
        file_number = int(file.replace('.txt', ''))
        dic = all_meta[file_number - 1]
        text = dic.get('text')
        if text != "None":   
            with open (file, 'w', encoding='utf-8') as f:
                f.write(text)
            get_clean_text(file)
            file_final = str(file_number) + 'mstm.txt'
            os.system("C:" + os.sep + "mystem.exe " + file + ' ' + file_final)
        else:
            os.remove(file)
        
        
def make_xml():
    all_meta = get_meta_data()
    lst = os.listdir('.')
    for index, file in enumerate(lst):
        dic = all_meta[index]
        text = dic.get('text')
        if text != "None":
            with open (file, 'w', encoding='utf-8') as f:
                f.write(text)
            get_clean_text(file)        
            file_final = file.replace('.txt', '.xml')
            os.system("C:" + os.sep + "mystem.exe " + "--format xml " + file + ' ' + file_final)
        else:
            os.remove(file)
        

def clean(text):
    regTag = re.compile('<.*?>', re.DOTALL)
    clean_t = regTag.sub("", text)
    return clean_t


def meta(path, author, header, created, source, publ_year):
    meta_text = "{0}; {1}; ; ; {2}; {3}; публицистика; ; ; ; ; нейтральный; н-возраст; н-уровень; городская; {4}; Вечерний Якутск; ; {5}; газета; Россия; Якутия (респ. Саха); ru"
    return meta_text.format(path, author, header, created, source, publ_year)


def move_to_dir(file, from_dir, to_dir):
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
    shutil.move(os.path.join(from_dir, file), to_dir)

def copy_to_dir(file, from_dir, to_dir):
    if not os.path.exists(to_dir):
        os.mkdir(to_dir)
    shutil.copy(os.path.join(from_dir, file), to_dir)   
    

def is_file(path):
    return (not os.path.isdir(path)) and (re.search('\d', path) is not None)


def get_meta_data():
    all_meta = []
    lst = [file for file in os.listdir() if is_file(file)]
    lst.sort(key=lambda f: int(os.path.splitext(f)[0]))
    print(lst)    
    for file in lst:
        print('Getting meta data for {}'.format(file))
        with open (file, 'r', encoding="utf-8") as f:
            text = f.read()

        created = find_created(text)
        if find_author(text) == '<a href="author?user=" class="c_w"></a>':
            author = 'Noname'
        else:
            author = find_author(text)
        
        header = find_header(text)
        text = find_main_text(text)                
        path = os.path.abspath(file)
        date = created.split(' ')
        source = "http://www.vecherniy.com/wall?id=" + str(lst.index(file) + 1)
        publ_year = ''
        if date != ['']:
            publ_year = date[3]
        
        dic = {
            'created' : created, 
            'author' : author, 
            'header' : header,
            'path' : path,
            'publ_year' : publ_year,
            'text' : text,
            'source' : source
            }
        all_meta.append(dic)
    return all_meta
                    


def get_clean_text(file):
    if re.search(r'\d', file) != None:
        with open (file, 'r', encoding="utf-8") as f:
            text = f.read()
            text = clean(text)
            with open(file, 'w', encoding="utf-8") as f:
                f.write(text)
                
                
def make_plain_text():
    all_meta = get_meta_data()
    lst = os.listdir('.')
    for index, file in enumerate(lst):
        dic = all_meta[index]
        path = dic.get('path')
        author = dic.get('author')
        header = dic.get('header')
        created = dic.get('created')
        source = dic.get('source')
        publ_year = dic.get('publ_year')
        text = dic.get('text')
        if text != "None":
            with open(file, 'w', encoding="utf-8") as f:
                f.write(make_shapka(file, author, header, created, source) + '\n' + text)
            get_clean_text(file)
            with open('..' + os.sep + 'meta.csv', 'a', encoding='utf-8') as f:
                source = "http://www.vecherniy.com/wall?id=" + file.replace('.txt', '')                    
                f.write(meta(path, author, header, created, source, publ_year) + '\n')
        else:
            os.remove(file)
         
                    
def move_to_year(directory, ending, all_meta):
    lst = os.listdir(directory)
    for file in lst:
        file_number = int(file.replace(ending, ''))
        dic = all_meta[file_number - 1]
        publ_year = dic.get('publ_year')
        if publ_year == "(.*?)2015(.*?)":
            move_to_dir(file, directory, "2015")
        elif publ_year == "(.*?)2016(.*?)":
            move_to_dir(file, directory, "2016")
        else:
            move_to_dir(file, directory, "2017")


def move_to_month(directory, ending, all_meta):
    for root, dirs, files in os.walk(directory):
        for d in dirs:
            if re.search(r"20(.*?)", d) != None:
                lst = os.listdir(d)
                for file in lst:
                    if re.search(r'\d', file) != None and os.path.isdir(file) == False:
                        file_number = int(file.replace(ending, ''))
                        dic = all_meta[file_number - 1]
                        created = dic.get('created')
                        if re.search(r"(.*?)января(.*?)", created, flags=re.DOTALL) != None:
                            move_to_dir(file, d, d + os.sep + "1")
                        elif re.search(r"(.*?)февраля(.*?)", created, flags=re.DOTALL) != None:
                            move_to_dir(file, d, d + os.sep + "2")
                        elif re.search(r"(.*?)марта(.*?)", created, flags=re.DOTALL) != None:
                            move_to_dir(file, d, d + os.sep + "3")  
                        elif re.search(r"(.*?)апреля(.*?)", created, flags=re.DOTALL) != None:
                            move_to_dir(file, d, d + os.sep + "4")
                        elif re.search(r"(.*?)мая(.*?)", created, flags=re.DOTALL) != None:
                            move_to_dir(file, d, d + os.sep + "5")
                        elif re.search(r"(.*?)июня(.*?)", created, flags=re.DOTALL) != None:
                            move_to_dir(file, d, d + os.sep + "6")
                        elif re.search(r"(.*?)июля(.*?)", created, flags=re.DOTALL) != None:
                            move_to_dir(file, d, d + os.sep + "7")
                        elif re.search(r"(.*?)августа(.*?)", created, flags=re.DOTALL) != None:
                            move_to_dir(file, d, d + os.sep + "8")
                        elif re.search(r"(.*?)сентября(.*?)", created, flags=re.DOTALL) != None:
                            move_to_dir(file, d, d + os.sep + "9")
                        elif re.search(r"(.*?)октября(.*?)", created, flags=re.DOTALL) != None:
                            move_to_dir(file, d, d + os.sep + "10")
                        elif re.search(r"(.*?)ноября(.*?)", created, flags=re.DOTALL) != None:
                            move_to_dir(file, d, d + os.sep + "11")
                        elif re.search(r"(.*?)декабря(.*?)", created, flags=re.DOTALL) != None:
                            move_to_dir(file, d, d + os.sep + "12")

                    
                    
def make_shapka(file, author, header, created, source):
    return('@au ' + author + '\n' + '@ti ' + header + '\n' + '@da ' + created + '\n' + '@url ' + source)

  
def main():
    crawl()
    all_meta = get_meta_data()
    for f in os.listdir('.'):
        if re.search(r'\d', f) != None:    
            copy_to_dir(f, '.', "plain")
            copy_to_dir(f, '.', "mystem-xml")
            move_to_dir(f, '.', "mystem-plain")
    os.chdir('plain')
    make_plain_text()
    move_to_year('.', '.txt', all_meta)
    move_to_month('.', '.txt', all_meta)
    os.chdir('..' + os.sep + 'mystem-plain')
    make_mystem()
    move_to_year('.', 'mstm.txt', all_meta)
    move_to_month('.', 'mstm.txt', all_meta)    
    os.chdir('..' + os.sep + 'mystem-xml')
    make_xml()
    move_to_year('.', '.xml', all_meta)
    move_to_month('.', '.xml', all_meta)    
    return "ok"

print(main())


