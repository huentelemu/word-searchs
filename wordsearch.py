import numpy as np

HORIZONTAL = 0
DIAGONAL = 1
VERTICAL = 2


class WordSearch:

    def __init__(self, words=[], shape=(20, 20)):
        self.soup = np.zeros(shape, dtype=str)
        self.soup = self.add_words(self.soup, words)

    def add_words(self, soup, words, max_n_tries=100):
        # Recursively try to add list of words in given numpy 2d array
        self.insert_word_in_soup(soup, words[0], 0, 0, 0)
        return soup

    @staticmethod
    def insert_word_in_soup(soup, word, x0, y0, orientation):
        # Add single word in numpy 2d array, given location and orientation
        # No check if it fits, that must be done before

        for i, letter in enumerate(word):
            if orientation == HORIZONTAL:
                x = x0 + i
                y = y0
            elif orientation == DIAGONAL:
                x = x0 + 1
                y = y0 + 1
            elif orientation == VERTICAL:
                x = x0
                y = y0 + 1
            else:
                raise Exception('Orientation type not recognized')

            soup[y, x] = letter
