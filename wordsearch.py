import numpy as np
from random import random
from random import shuffle

HORIZONTAL = 0
DIAGONAL = 1
VERTICAL = 2


class WordSearch:

    def __init__(self, original_words=[], shape=(20, 20)):

        # If any word might not fit in the soup, raise exception
        if max(map(len, ['asd', 'qwer'])) > min(shape):
            raise Exception('A word is longer than shortest soup side')

        self.width = shape[0]
        self.height = shape[1]
        self.soup = np.zeros(shape, dtype=str)

        words = self.clean_words(original_words)
        self.coords_words_list = self.add_words(self.soup.copy(), words)
        if not self.coords_words_list:
            raise Exception('Combination not found')

        # Insert words in empty soup:
        for word_coords in self.coords_words_list:
            self.insert_word_in_soup(
                self.soup,
                word_coords['word'],
                word_coords['x0'],
                word_coords['y0'],
                word_coords['orientation'],
            )

    def clean_words(self, original_words):
        # Remove spanish tildes but not ñ
        words = []
        for original_word in original_words:
            word = original_word.upper()
            word = word.replace('Á', 'A')
            word = word.replace('É', 'E')
            word = word.replace('Í', 'I')
            word = word.replace('Ó', 'O')
            word = word.replace('Ú', 'U')
            word = word.replace('Ü', 'U')
            words.append(word)
        return words

    def add_words(self, soup, words, max_n_tries=10):
        # Recursively try to add list of words in given numpy 2d array

        n_tries = 0
        while n_tries < max_n_tries:

            shuffle(words)
            word, *rest_of_words = words

            orientation = int(random() * 3)
            if orientation <= 1:
                x0 = int(random() * (self.width - len(word)))
            else:
                x0 = int(random() * self.width)
            if orientation >= 1:
                y0 = int(random() * (self.height - len(word)))
            else:
                y0 = int(random() * self.height)

            soup_copy = soup.copy()
            if self.insert_word_in_soup(soup_copy, word, x0, y0, orientation):
                word_coords_dict = {
                    'word': word,
                    'x0': x0,
                    'y0': y0,
                    'orientation': orientation,
                }
                if rest_of_words:
                    coords_list = self.add_words(soup_copy, rest_of_words)
                    if coords_list:
                        coords_list.append(word_coords_dict)
                        return coords_list
                else:
                    return [word_coords_dict]
            n_tries += 1
        else:
            return None

    @staticmethod
    def insert_word_in_soup(soup, word, x0, y0, orientation):
        # Add single word in numpy 2d array, given location and orientation
        # No check if it fits, that must be done before

        # Prepare letter coordinates
        letter_coordinates = []
        for i, letter in enumerate(word):
            if orientation == HORIZONTAL:
                letter_coordinates.append((y0, x0 + i))
            elif orientation == DIAGONAL:
                letter_coordinates.append((y0 + i, x0 + i))
            elif orientation == VERTICAL:
                letter_coordinates.append((y0 + i, x0))
            else:
                raise Exception('Orientation type not recognized')

        # Check if every letter fits
        for i, coords in enumerate(letter_coordinates):
            if soup[coords] and soup[coords] != word[i]:
                return False

        # Insert word into soup
        for i, coords in enumerate(letter_coordinates):
            soup[coords] = word[i]

        return True

    def print_soup(self):
        for i in range(self.soup.shape[0]):
            print_string = ''
            for j in range(self.soup.shape[0]):
                print_string += self.soup[i, j] if self.soup[i, j] else '-'
            print(print_string)
