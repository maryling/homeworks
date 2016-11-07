word = input()
for index, letter in enumerate(word):
    if index % 2 == 0 and (letter == "п" or letter == "о" or letter == "е"):
        print (letter)
