import codecs
import numpy as np
from random import random, shuffle, choice
from time import perf_counter
from PIL import Image, ImageDraw, ImageFont


HORIZONTAL = 0
DIAGONAL = 1
VERTICAL = 2


class WordSearch:

    def __init__(self, original_words=[], shape=(20, 20), n_orientations=8, font_size=90, square_size=80):

        self.original_words = original_words
        self.n_orientations = n_orientations
        self.font_size = font_size
        self.square_size = square_size
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

        self.string_representation = self.represent_as_string()

        # Insert random characters in complete soup
        characters_list = list(range(65, 91))
        characters_list.append(209)
        characters_list = list(map(chr, characters_list))
        self.complete_soup = self.soup.copy()
        for (i, j), c in np.ndenumerate(self.complete_soup):
            if c == '':
                self.complete_soup[i, j] = choice(characters_list)


    def represent_as_string(self):
        print_string = ''
        for i in range(self.soup.shape[0]):
            for j in range(self.soup.shape[1]):
                if self.soup[i, j] and self.soup[i, j] != '*':
                    print_string += self.soup[i, j]
                else:
                    print_string += '-'
            print_string += '\n'
        return print_string

    def __str__(self):
        print_string = ''
        for i in range(self.soup.shape[0]):
            for j in range(self.soup.shape[1]):
                if self.soup[i, j] and self.soup[i, j] != '*':
                    print_string += self.soup[i, j]
                else:
                    print_string += '-'
            print_string = '\n'
        return print_string

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
            orientation = int(random() * self.n_orientations)

            if orientation == 0:
                x0 = int(random() * (self.width - len(word)))
                y0 = int(random() * self.height)
            elif orientation == 1:
                x0 = int(random() * (self.width - len(word)))
                y0 = int(random() * (self.height - len(word)))
            elif orientation == 2:
                x0 = int(random() * self.width)
                y0 = int(random() * (self.height - len(word)))
            elif orientation == 3:
                x0 = int(random() * (self.width - len(word))) + len(word) - 1
                y0 = int(random() * (self.height - len(word)))
            elif orientation == 4:
                x0 = int(random() * (self.width - len(word))) + len(word) - 1
                y0 = int(random() * self.height)
            elif orientation == 5:
                x0 = int(random() * (self.width - len(word))) + len(word) - 1
                y0 = int(random() * (self.height - len(word))) + len(word) - 1
            elif orientation == 6:
                x0 = int(random() * self.width)
                y0 = int(random() * (self.height - len(word))) + len(word) - 1
            elif orientation == 7:
                x0 = int(random() * (self.width - len(word)))
                y0 = int(random() * (self.height - len(word))) + len(word) - 1
            else:
                raise Exception('Orientation type not recognized')

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
            if orientation == 0:
                letter_coordinates.append((y0, x0 + i))
            elif orientation == 1:
                letter_coordinates.append((y0 + i, x0 + i))
            elif orientation == 2:
                letter_coordinates.append((y0 + i, x0))
            elif orientation == 3:
                letter_coordinates.append((y0 + i, x0 - i))
            elif orientation == 4:
                letter_coordinates.append((y0, x0 - i))
            elif orientation == 5:
                letter_coordinates.append((y0 - i, x0 - i))
            elif orientation == 6:
                letter_coordinates.append((y0 - i, x0))
            elif orientation == 7:
                letter_coordinates.append((y0 - i, x0 + i))
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

    def draw_image(self, character_matrix):
        square_size = self.square_size
        margin_offset = 10
        # widen_rectangle = 2

        image = Image.new(
            'RGBA',
            tuple(np.array(character_matrix.shape)[[1, 0]] * square_size + margin_offset * 2),
            color=(200, 200, 200, 0)
        )
        drawer = ImageDraw.Draw(image)
        font = ImageFont.truetype("static/fonts/tungab.ttf", self.font_size)

        for (i, j), c in np.ndenumerate(character_matrix):
            # # Prepare squares
            # rect_y = margin_offset + j * square_side
            # rect_x = margin_offset + i * square_side
            #
            # # Draw squares
            # for w in range(-widen_rectangle, widen_rectangle + 1):
            #     drawer.rectangle(((rect_y + w, rect_x + w), (rect_y + square_side - w, rect_x + square_side - w)),
            #                      outline="black")

            # Make squares interior not transparent but white
            # gris = 255
            # drawer.rectangle(((rect_y + widen_rectangle + 1, rect_x + widen_rectangle + 1),
            #                  (rect_y + square_side - widen_rectangle - 1, rect_x + square_side - widen_rectangle - 1)),
            #                  fill=(gris, gris, gris))

            if c == '-':
                continue

            # Draw letter
            text_w, text_h = drawer.textsize(c, font)
            char_h_offset = int((square_size - text_w) / 2 * 1.05)
            char_w_offset = int((square_size - text_h) / 2 * 0.6)

            drawer.text(
                (j * square_size + char_h_offset + margin_offset, i * square_size + char_w_offset + margin_offset),
                c,
                fill=(0, 0, 0),
                font=font
            )

        return image

    def draw_soup(self):
        return self.draw_image(self.complete_soup)

    def draw_solution(self):
        return self.draw_image(self.soup)

    def write_soup(self):
        image = self.draw_soup()
        image.save('Sopa.png', 'png')

    def write_solution(self):
        image = self.draw_solution()
        image.save('Solucion.png', 'png')


def read_words_file(file_path):

    groups_of_words = []
    # with codecs.open(file_path, "rb") as f:
    # with open(file_path, 'rb') as f:
    with open(file_path, "r", encoding="ISO-8859-1") as f:
        lines = [line.rstrip('\n').strip().upper() for line in f.readlines()]

        index = 0

        # Skip Header
        while index < len(lines):
            if lines[index][:11] == '* * * GRUPO':
                break
            index += 1

        # Read words
        words = []
        while index < len(lines):
            line = lines[index]
            if line[:11] == '* * * GRUPO':
                if len(words) > 0:
                    groups_of_words.append(sorted(words))
                    words = []
            elif len(line) > 0:
                words.append(line)
            index += 1
        else:
            if len(words) > 0:
                groups_of_words.append(sorted(words))

        return groups_of_words
