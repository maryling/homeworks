word = input()
list_of_words = []

while word:
    if len(word) > 5:
        list_of_words.append(word)
    word = input()

for element in list_of_words:
    print(element)
