with open('text.txt','r', encoding = 'utf-8') as f:
    
    lines = f.readlines()
    biggest = len(lines[0]) - 1
    for i in range(len(lines)):
        if biggest < len(lines[i]):
            if i + 1 != len(lines):
                biggest = len(lines[i]) - 1
            else:
                biggest = len(lines[i])
                
    smallest = len(lines[0]) - 1
    for i in range(len(lines)):
        if smallest > len(lines[i]):
            if i + 1 != len(lines):
                smallest = len(lines[i]) - 1
            else:
                smallest = len(lines[i]) 
    
    final = biggest / smallest
    
    print(final)
            
