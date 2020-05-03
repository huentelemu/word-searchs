import numpy as np
from random import random, shuffle
from time import perf_counter


HORIZONTAL = 0
DIAGONAL = 1
VERTICAL = 2


class WordSearch:

    def __init__(self, original_words=[], shape=(20, 20)):

        self.original_words = original_words
        words = self.clean_words(self.original_words)

        # Append words with edge space savers
        # words = list(map(lambda x: '*' + x + '*', words))

        # If any word might not fit in the soup, raise exception
        if max(map(len, words)) > min(shape):
            raise Exception('A word is longer than shortest soup side')

        self.height = shape[0]
        self.width = shape[1]
        self.soup = np.zeros(shape, dtype=str)

        self.coords_words_list = self.add_words(self.soup.copy(), words, perf_counter())
        if not self.coords_words_list:
            self.combination_found = False
            return
        else:
            self.combination_found = True

        # Insert words in empty soup:
        for word_coords in self.coords_words_list:
            self.insert_word_in_soup(
                self.soup,
                word_coords['word'],
                word_coords['letter_coordinates']
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

    def add_words(self, soup, words, init_time, max_n_tries=10, max_n_backtracks=3, max_seconds=3):
        # Recursively try to add list of words in given numpy 2d array

        n_failed_insertions = 0
        n_backtracks = 0
        while n_failed_insertions < max_n_tries and n_backtracks < max_n_backtracks:

            # Check if we are already out of time
            if perf_counter() - init_time > max_seconds:
                return None

            shuffle(words)
            word, *rest_of_words = words

            # Get random feasible coordinates for word
            orientation = int(random() * 3)
            if orientation <= 1:
                x0 = int(random() * (self.width - len(word)))
            else:
                x0 = int(random() * self.width)
            if orientation >= 1:
                y0 = int(random() * (self.height - len(word)))
            else:
                y0 = int(random() * self.height)

            # Prepare letter coordinates
            letter_coordinates = self.prepare_letter_coordinates(word, x0, y0, orientation)

            # Check if word doesn't fit
            if not self.check_word_in_soup(soup, word, letter_coordinates):
                n_failed_insertions += 1
                continue

            # Insert word into soup and prepare coords dict
            soup_copy = soup.copy()
            self.insert_word_in_soup(soup_copy, word, letter_coordinates)
            word_coords_dict = {
                'word': word,
                'x0': x0,
                'y0': y0,
                'orientation': orientation,
                'letter_coordinates': letter_coordinates,
            }

            # Stop recursion and return if there are no words left
            if not rest_of_words:
                return [word_coords_dict]

            # Continue recursion with rest of the words
            coords_list = self.add_words(soup_copy, rest_of_words, init_time)

            # If coords_list is None, then that means somewhere down the line the max number of failed insertions was
            # reached, so we should scrap this path and try again.
            if not coords_list:
                # return None
                n_backtracks += 1
                continue

            # If coord_list was valid, then return this
            coords_list.append(word_coords_dict)
            return coords_list

        else:
            return None

    @staticmethod
    def prepare_letter_coordinates(word, x0, y0, orientation):
        # Prepare letter coordinates
        letter_coordinates = []
        for i in range(len(word)):
            if orientation == HORIZONTAL:
                letter_coordinates.append((y0, x0 + i))
            elif orientation == DIAGONAL:
                letter_coordinates.append((y0 + i, x0 + i))
            elif orientation == VERTICAL:
                letter_coordinates.append((y0 + i, x0))
            else:
                raise Exception('Orientation type not recognized')
        return letter_coordinates

    @staticmethod
    def check_word_in_soup(soup, word, letter_coordinates):
        # Check if every letter fits
        for i, coords in enumerate(letter_coordinates):
            if soup[coords] and soup[coords] != word[i]:
                return False
        return True

    @staticmethod
    def insert_word_in_soup(soup, word, letter_coordinates):
        # Insert word into soup
        for i, coords in enumerate(letter_coordinates):
            soup[coords] = word[i]

    def print_soup(self):
        for i in range(self.soup.shape[0]):
            print_string = ''
            for j in range(self.soup.shape[1]):
                if self.soup[i, j] and self.soup[i, j] != '*':
                    print_string += self.soup[i, j]
                else:
                    print_string += '-'
            print(print_string)
