

# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

from time import perf_counter

from unidecode import unidecode

from PIL import Image, ImageDraw, ImageFont


def str2df(words):
    df = pd.DataFrame()
    for w, word in enumerate(words):
        word_df = pd.DataFrame()
        for l, letter in enumerate(word):
            letter_df = pd.DataFrame({'letter': [ord(letter)], 'letter_index': [l]})
            word_df = word_df.append(letter_df)
        word_df['word_index'] = w
        df = df.append(word_df)
    return df


def print_crossword(own_words):
    coords_word = own_words.copy()

    def insert_word_and_length(row):
        word = words.loc[words.word_index == row.word_index, 'letter'].tolist()
        word = ''.join(chr(c) for c in word)
        row['word'] = word
        row['len_word'] = len(word)
        if row.horizontal:
            row['y_min'] = row.y
            row['y_max'] = row.y
            row['x_min'] = row.x - row.letter_index
            row['x_max'] = row.x - row.letter_index + len(word)
        else:
            row['x_min'] = row.x
            row['x_max'] = row.x
            row['y_min'] = row.y - row.letter_index
            row['y_max'] = row.y - row.letter_index + len(word)
        return row

    coords_word = coords_word.apply(insert_word_and_length, axis=1)

    coords_word[['x', 'x_min', 'x_max']] -= coords_word.x_min.min()
    coords_word[['y', 'y_min', 'y_max']] -= coords_word.y_min.min()

    crossword = np.zeros((int(coords_word.y_max.max()), int(coords_word.x_max.max())), dtype=str)
    crossword[:] = '-'

    for _, row in coords_word.iterrows():
        word = row.word
        for i, letter in enumerate(word):
            if row.horizontal:
                y = row.y
                x = row.x_min + i
            else:
                y = row.y_min + i
                x = row.x
            crossword[int(y), int(x)] = letter
    print('#######')
    print('Shape: ' + str(crossword.shape))
    area = crossword.shape[0] * crossword.shape[1]
    print('Area: ' + str(area))
    n_words = coords_word.shape[0]
    print('N words: ' + str(n_words))
    print('N crossings: ' + str(coords_word.n_crossings.sum()))
    for i in range(crossword.shape[0]):
        word = ''
        for c in crossword[i, :]:
            word += c
        print(word)
    return area, n_words


def prepare_character_matrices(own_words, words_original, n_initial_words, n_versions=9):
    coords_word = own_words.copy()

    def insert_word_and_length(row):
        word = words.loc[words.word_index == row.word_index, 'letter'].tolist()
        word = ''.join(chr(c) for c in word)
        row['word'] = word
        row['word_original'] = words_original[int(row.word_index)]
        row['len_word'] = len(word)
        if row.horizontal:
            row['y_min'] = row.y
            row['y_max'] = row.y
            row['x_min'] = row.x - row.letter_index
            row['x_max'] = row.x - row.letter_index + len(word)
        else:
            row['x_min'] = row.x
            row['x_max'] = row.x
            row['y_min'] = row.y - row.letter_index
            row['y_max'] = row.y - row.letter_index + len(word)
        return row

    coords_word = coords_word.apply(insert_word_and_length, axis=1)

    coords_word[['x', 'x_min', 'x_max']] -= coords_word.x_min.min()
    coords_word[['y', 'y_min', 'y_max']] -= coords_word.y_min.min()

    # Choice words which will be part of the initial group in the crossword
    for i in range(n_versions):
        chosen_words = np.random.choice(coords_word.word_index, n_initial_words, replace=False).tolist()
        coords_word['is_initial_word_' + str(i)] = coords_word.word_index.isin(chosen_words)
        # coords_word = coords_word.sort_values('is_initial_word')

    crosswords = []
    for i in range(n_versions + 1):
        crossword = np.zeros((int(coords_word.y_max.max()), int(coords_word.x_max.max())), dtype=str)
        crossword[:] = '-'
        crosswords += [crossword]

    for _, row in coords_word.iterrows():
        word = row.word
        for i, letter in enumerate(word):
            if row.horizontal:
                y = row.y
                x = row.x_min + i
            else:
                y = row.y_min + i
                x = row.x
            crosswords[0][int(y), int(x)] = letter
            for a in range(1, len(crosswords)):
                if row['is_initial_word_' + str(a - 1)]:
                    crosswords[a][int(y), int(x)] = letter
                elif crosswords[a][int(y), int(x)] == '-':
                    crosswords[a][int(y), int(x)] = '?'

    return crosswords, coords_word


def draw_images(crosswords, coords_word, group):
    square_side = 80
    margin_offset = 10
    widen_rectangle = 2

    n_versions = len(crosswords) - 1

    images = []
    drawers = []
    for i in range(n_versions + 1):
        images += [Image.new('RGBA', tuple(np.array(crosswords[0].shape)[[1, 0]] * square_side + margin_offset * 2),
                             color=(200, 200, 200, 0))]
        drawers += [ImageDraw.Draw(images[i])]
    font = ImageFont.truetype("arial.ttf", 60)

    for (i, j), c in np.ndenumerate(crosswords[0]):
        if c == '-':
            continue

        # Prepare squares
        rect_y = margin_offset + j * square_side
        rect_x = margin_offset + i * square_side
        for d in drawers:
            # Draw squares
            for w in range(-widen_rectangle, widen_rectangle + 1):
                d.rectangle(((rect_y + w, rect_x + w), (rect_y + square_side - w, rect_x + square_side - w)),
                            outline="black")

            # Make squares interior not transparent but white
            gris = 255
            d.rectangle(((rect_y + widen_rectangle + 1, rect_x + widen_rectangle + 1),
                         (rect_y + square_side - widen_rectangle - 1, rect_x + square_side - widen_rectangle - 1)),
                        fill=(gris, gris, gris))

        # Draw letter
        text_w, text_h = d.textsize(c, font)
        char_h_offset = int((square_side - text_w) / 2 * 1.05)
        char_w_offset = int((square_side - text_h) / 2 * 0.6)
        drawers[0].text(
            (j * square_side + char_h_offset + margin_offset, i * square_side + char_w_offset + margin_offset), c,
            fill=(0, 0, 0), font=font)
        for a in range(1, len(crosswords)):
            if crosswords[a][i, j] != '?':
                drawers[a].text(
                    (j * square_side + char_h_offset + margin_offset, i * square_side + char_w_offset + margin_offset),
                    c, fill=(0, 0, 0), font=font)

    images[0].save('Resultados/' + str(group).zfill(3) + '-Solucion.png', 'png')
    for a in range(n_versions):
        images[a + 1].save('Resultados/' + str(group).zfill(3) + '-Cruzada' + str(a + 1) + '.png', 'png')

    coords_word = coords_word.sort_values('word')
    with open('Resultados/' + str(group).zfill(3) + '-Palabras.txt', "w", encoding="ISO-8859-1") as writer:
        for _, row in coords_word.iterrows():
            writer.write(row.word_original + '\n')


class Crossword:

    def __init__(self, cw, own_word, new_words=np.zeros(0)):

        self.score = 0
        self.n_visits = 0
        self.child_Crosswords = []
        self.is_virgin = True

        self.UCB1_ratio = 2

        if new_words.shape[0] > 0:
            ## Complete new Crossword object

            # Expand a new child for every single word

            for word_index in words.word_index.unique():
                # Give them the current words
                rest_of_words_df = new_words.loc[new_words.word_index != word_index].copy()

                child_cw = new_words.loc[new_words.word_index == word_index, ['letter']].copy()

                own_word = {}
                own_word['y'] = [0]
                own_word['x'] = [0]
                own_word['horizontal'] = [True]
                own_word['letter_index'] = [0]
                own_word['word_index'] = [word_index]
                own_word['n_crossings'] = [0]
                own_word = pd.DataFrame(own_word)

                child_cw['y'] = 0
                child_cw['x'] = np.arange(child_cw.shape[0])
                child_cw['horizontal'] = True

                new_child_node = Crossword(child_cw, own_word)

                self.child_Crosswords += [new_child_node]

            self.n_visits = 1
            self.N = 1

            self.own_word = pd.DataFrame()
            self.new_words = new_words

        else:

            # Normal initialization with current crossword and dict of its corresponding word
            self.cw = cw
            self.own_word = own_word

    def get_possible_crossings(self, current, new_words):

        # Cross the current crossword with the new word
        possible_crossings = pd.merge(current, new_words)

        possible_crossings['n_crossings'] = -1
        possible_crossings['too_close_contacts'] = -1
        possible_crossings['time1'] = 0.0
        possible_crossings['time2'] = 0.0
        possible_crossings['time3'] = 0.0
        possible_crossings['time4'] = 0.0
        possible_crossings['time5'] = 0.0
        possible_crossings['time6'] = 0.0
        possible_crossings['time7'] = 0.0
        possible_crossings['time8'] = 0.0
        possible_crossings['time9'] = 0.0

        new_possible_crossings = pd.DataFrame()

        max_n_crossings = 0

        # def check_crossings(pc, current, new_words):
        for _, pc in possible_crossings.iterrows():

            init = perf_counter()

            # Define fixed and go-along axes, depending on the orientation of the current word
            fix_axis = ['y', 'x'][pc.horizontal]
            along_axis = ['x', 'y'][pc.horizontal]
            pc['time1'] = perf_counter() - init;
            init = perf_counter()

            # Extract new word as possible_new_word
            possible_new_word = new_words.loc[new_words.word_index == pc.word_index].copy()
            len_word = possible_new_word.shape[0]
            pc['time2'] = perf_counter() - init;
            init = perf_counter()

            # Insert would-be coordinates in possible_new_word dataframe
            init_coord = pc[along_axis] - pc.letter_index
            possible_new_word[along_axis] = np.arange(init_coord, init_coord + len_word)
            possible_new_word[fix_axis] = pc[fix_axis]
            pc['time3'] = perf_counter() - init;
            init = perf_counter()

            # Check where the new possible word crosses with the current crossword
            crossings_with_current_cw = pd.merge(possible_new_word, current, on=['y', 'x'],
                                                 suffixes=('_new', '_current'))
            pc['time4'] = perf_counter() - init;
            init = perf_counter()

            # Check that all the crossings have the same letter. If not, stop this iteration
            if not np.all(crossings_with_current_cw.letter_new == crossings_with_current_cw.letter_current):
                continue
            pc['time5'] = perf_counter() - init;
            init = perf_counter()

            # if crossings_with_current_cw.shape[0]<max_n_crossings:
            #    continue

            # if crossings_with_current_cw.shape[0]>max_n_crossings:
            #    new_possible_crossings = pd.DataFrame()
            #    max_n_crossings = crossings_with_current_cw.shape[0]

            ## Check that new word is not touching other words in the current crossword
            # btp: border touching positions

            # Add contact at beginning of word
            fa = [pc[fix_axis]]
            aa = [possible_new_word[along_axis].iloc[0] - 1]
            # btp = pd.DataFrame({fix_axis:[pc[fix_axis]],
            #                    along_axis:[possible_new_word[along_axis].iloc[0]-1]
            #                   })

            # Add contact at the end of word
            fa += [pc[fix_axis]]
            aa += [possible_new_word[along_axis].iloc[-1] + 1]
            # btp = btp.append(pd.DataFrame({fix_axis:[pc[fix_axis]],
            #                               along_axis:[possible_new_word[along_axis].iloc[-1]+1]
            #                              }))

            # Add contact along one side of the word
            fa += [pc[fix_axis] - 1] * len_word
            aa += possible_new_word[along_axis].tolist()
            # btp = btp.append(pd.DataFrame({fix_axis:[pc[fix_axis]-1]*len_word,
            #                               along_axis:possible_new_word[along_axis]
            #                              }))

            # Add contact at the other side
            fa += [pc[fix_axis] + 1] * len_word
            aa += possible_new_word[along_axis].tolist()
            # btp = btp.append(pd.DataFrame({fix_axis:[pc[fix_axis]+1]*len_word,
            #                               along_axis:possible_new_word[along_axis]
            #                              }))
            btp = pd.DataFrame({fix_axis: fa, along_axis: aa})
            pc['time6'] = perf_counter() - init;
            init = perf_counter()

            # Trim contacts related to crossed words
            btp = btp.loc[~btp[along_axis].isin(crossings_with_current_cw[along_axis])]
            pc['time7'] = perf_counter() - init;
            init = perf_counter()

            # Check contacts with current crossword
            contacts_current = pd.merge(btp, current[['x', 'y']])
            pc['time8'] = perf_counter() - init;
            init = perf_counter()

            # Storing values
            pc['n_crossings'] = crossings_with_current_cw.shape[0]
            pc['too_close_contacts'] = contacts_current.shape[0]
            pc['time9'] = perf_counter() - init;
            init = perf_counter()

            # Incrementing new dataframe
            new_possible_crossings = new_possible_crossings.append(pc)

        ## Check factibility of each crossing
        # possible_crossings = possible_crossings.apply(lambda x:check_crossings(x, cw, nw), axis=1)

        # Check times
        print(new_possible_crossings.shape)
        for c in new_possible_crossings.columns:
            if 'time' in c:
                # print(c)
                # print(new_possible_crossings[c].sum())
                pass
        print('')

        # Filter out non legit crossings
        new_possible_crossings = new_possible_crossings.loc[new_possible_crossings.n_crossings > 0]
        new_possible_crossings = new_possible_crossings.loc[new_possible_crossings.too_close_contacts == 0]

        return new_possible_crossings

    def cross_word_with_crossword(self, crossing, new_words, cw):

        # Store details about the chosen word to cross and where
        own_word = crossing[['y', 'x', 'horizontal', 'letter_index', 'word_index', 'n_crossings']]
        own_word.horizontal = np.logical_not(own_word.horizontal)

        # Prepare new word
        new_word = new_words.loc[new_words.word_index == own_word.word_index, ['letter']]

        new_word['horizontal'] = own_word.horizontal
        if own_word.horizontal:
            fix_axis = 'y'
            along_axis = 'x'
        else:
            fix_axis = 'x'
            along_axis = 'y'

        new_word[fix_axis] = own_word[fix_axis]

        init_along = own_word[along_axis] - own_word['letter_index']
        new_word[along_axis] = np.arange(init_along, init_along + new_word.shape[0])

        # Obtain the different crossings of the new word with the current crossword
        new_word_crossings = pd.merge(new_word[['y', 'x']], cw[['y', 'x']])

        # Join the new word to the current crossword
        new_cw = cw.append(new_word).reset_index(drop=True)

        # Trim intersections
        to_trim_elements = []
        for i, row in self.cw.iterrows():
            if min(np.abs(new_word_crossings.y - row.y) + np.abs(new_word_crossings.x - row.x)) <= 1:
                to_trim_elements += [i]
        new_cw.loc[to_trim_elements, 'letter'] = -1

        return own_word, new_cw

    def iterate(self, N=-1):

        if N == -1:
            N = self.n_visits

        # Select a child node to iterate
        selected_child = self.child_Crosswords[self.selection(N)]

        if selected_child.n_visits == 0:
            # Rollout
            own_words = selected_child.rollout(self.new_words)
            own_words = self.own_word.append(own_words)
            self.score = own_words.n_crossings.sum()
        else:
            # Expand if the selected node hasn't spawned childs yet
            if selected_child.is_virgin:
                selected_child.expand(self.new_words)
            own_words = selected_child.iterate(N=N)
            own_words = self.own_word.append(own_words)
            self.score = own_words.n_crossings.sum()

        self.n_visits += 1

        return own_words

    def expand(self, new_words):
        self.is_virgin = False

        # Remove own word from list of new words, and store the rest
        self.new_words = new_words.loc[new_words.word_index != self.own_word.word_index.iloc[0]]

        # Obtain factible crossings
        possible_crossings = self.get_possible_crossings(self.cw, self.new_words)

        # Create a child node for every possible crossing
        for _, crossing in possible_crossings.iterrows():
            # Cross new word with current crossword
            own_word, cw = self.cross_word_with_crossword(crossing, self.new_words, self.cw)
            # Create new child node
            new_child_node = Crossword(cw, own_word.to_frame().T)
            self.child_Crosswords += [new_child_node]

    def selection(self, N):
        # Selection using UCB1
        prev_UCB1 = -1
        child_index = -1
        for i, cc in enumerate(self.child_Crosswords):
            UCB1 = cc.score + self.UCB1_ratio * np.sqrt(np.log(N + 0.0001) / cc.n_visits)
            if UCB1 > prev_UCB1:
                prev_UCB1 = UCB1
                child_index = i
        return child_index

    def rollout(self, new_words, n_sampled_words=4):

        # Iteration that completes the crossword to the end
        cw = self.cw.copy().reset_index(drop=True)
        nw = new_words.copy()

        # Remove own word from list of new words
        nw = nw.loc[nw.word_index != self.own_word.word_index.iloc[0]]

        own_words = self.own_word.copy()

        while True:

            # Sample only N words from the pool of new words
            unique_word_indexes = np.array(nw.word_index.unique())
            if len(unique_word_indexes) > n_sampled_words:
                chosen_words = np.random.choice(unique_word_indexes, n_sampled_words, replace=False).tolist()
                sampled_nw = nw.loc[nw.word_index.isin(chosen_words), :]
            else:
                sampled_nw = nw.copy()

            # Obtain factible crossings
            possible_crossings = self.get_possible_crossings(cw, sampled_nw)

            # Give preference to more numerous crossings
            max_n_crossings = possible_crossings.n_crossings.max()
            possible_crossings = possible_crossings.loc[possible_crossings.n_crossings == max_n_crossings]

            # Sample a single crossing randomly
            if possible_crossings.shape[0] == 0:
                break
            crossing = possible_crossings.sample().squeeze()

            # Cross new word with current crossword
            own_word, cw = self.cross_word_with_crossword(crossing, nw, cw)

            # Add new word to current dataframe
            own_words = own_words.append(own_word)

            # Remove inserted word from new words' list
            nw = nw.loc[nw.word_index != own_word.word_index, :]

            # Break iteration if we have inserted all words
            if nw.shape[0] == 0:
                break

        self.score = own_words.n_crossings.sum()

        self.n_visits += 1
        return own_words


with open('Parametros.txt', 'r') as file_pars:
    pars = {}
    while True:
        line = file_pars.readline().strip('\n')
        if (len(line) == 0):
            break
        line = line.split('=')
        pars[line[0]] = int(line[1])

with open('Palabras minadas.txt', "r", encoding="ISO-8859-1") as f:
    f.seek(0, 2)  # Jumps to the end
    end_location = f.tell()  # Give you the end location (characters from start)
    f.seek(0)  # Jump to the beginning of the file again
    while True:
        line = f.readline().strip().upper()
        if line[:11] == '* * * GRUPO':
            break
    group = 0
    while True:
        words = []
        words_original = []
        while True:
            line = f.readline().strip().upper()
            if line[:11] == '* * * GRUPO' or f.tell() == end_location:
                break
            if line == '':
                continue
            words_original += [line]
        for wo in words_original:
            wo = wo.replace('Á', 'A')
            wo = wo.replace('É', 'E')
            wo = wo.replace('Í', 'I')
            wo = wo.replace('Ó', 'O')
            wo = wo.replace('Ë', 'E')
            wo = wo.replace('Ü', 'U')
            wo = wo.replace('Ú', 'U')
            words += [wo]

        words = str2df(words)
        C = Crossword(pd.DataFrame(), {}, words)

        n_iter = pars['numero_repeticiones_por_cruzada']

        init_total_exec = perf_counter()

        best_crossword_df = C.iterate()
        best_area, best_n_words = print_crossword(best_crossword_df)

        for i in range(n_iter - 1):
            own_words = C.iterate()
            area, n_words = print_crossword(own_words)
            if n_words > best_n_words:
                if area < best_area:
                    best_crossword_df = own_words.copy()

        print('Total time: ' + str(perf_counter() - init_total_exec))

        crosswords, coords_word = prepare_character_matrices(best_crossword_df, words_original,
                                                             pars['numero_inicial_palabras'])
        draw_images(crosswords, coords_word, group)
        group += 1

        if f.tell() == end_location:
            break