with open('freq.txt','r', encoding = 'utf-8') as f:
    lines = f.readlines()
    
    for i in lines:
        i = i.strip()
        if i.count('союз') == 1:
            print(i)
    
    words = []    
    sum_ipm = 0        
    for line in lines:
        line = line.strip()
        if line.count(' ед жен ') == 1:
            word, features, ipm = line.split(' | ', 2)
            words.append(word)
            ipm = float(ipm)
            sum_ipm += ipm 
    print(*words, sep=', ')
    print(sum_ipm)
    
    
    query = input('Введите слово в начальной форме ')
    while query:
        for line in lines:
            line = line.strip()
            word, features, ipm = line.split(' | ', 2)
            if word == query:
                print (features, ipm)
        query = input('Введите слово в начальной форме ')
     
        
        
        
                
