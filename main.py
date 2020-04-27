from wordsearch import WordSearch

words = [
    'perro',
    'gato',
    'raton',
]

w = WordSearch(words=words, shape=(20, 20))
print(w.soup)
