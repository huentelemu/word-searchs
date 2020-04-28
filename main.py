from wordsearch import WordSearch

words = [
    'Perro',
    'Gato',
    'Ratón',
    'Araña',
]

w = WordSearch(original_words=words, shape=(10, 10))
w.print_soup()
