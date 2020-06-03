from wordsearch import WordSearch
from MineroReader import MineroReader
words = [
    'Perro',
    'Gato',
    'Ratón',
    'Araña',
]

mr = MineroReader()

# for words in mr.groups_of_words:
#     w = WordSearch(original_words=words, shape=(29, 17))
#     if w.combination_found:
#         w.print_soup()
#     else:
#         print('Combination not found')
#     print('\n')

w = WordSearch(original_words=mr.groups_of_words[0], shape=(29, 17))
print(w.soup)
w.print_soup()
w.write_soup()
w.write_solution()
