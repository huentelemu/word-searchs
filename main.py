from wordsearch import WordSearch
from MineroReader import MineroReader
words = [
    'Perro',
    'Gato',
    'Ratón',
    'Araña',
]

mr = MineroReader()

for words in mr.groups_of_words:
    w = WordSearch(original_words=words, shape=(29, 17))
    if w.combination_found:
        w.print_soup()
    else:
        print('Combination not found')
    print('\n')
