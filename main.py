from wordsearch import WordSearch
from MineroReader import MineroReader
words = [
    'Perro',
    'Gato',
    'Ratón',
    'Araña',
]

mr = MineroReader()
w = WordSearch(original_words=mr.groups_of_words[0], shape=(20, 25))
w.print_soup()
