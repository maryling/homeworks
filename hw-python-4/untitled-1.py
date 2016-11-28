word = list(input('Insert a word '))

for i in range(len(word)):
 print(*word[:(i+1)], sep='')
 
 