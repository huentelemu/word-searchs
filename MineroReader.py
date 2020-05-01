

class MineroReader:

    def __init__(self, file_path='Palabras minadas.txt'):
        with open(file_path, "r", encoding="ISO-8859-1") as f:
            f.seek(0, 2)  # Jumps to the end
            end_location = f.tell()  # Give you the end location (characters from start)
            f.seek(0)  # Jump to the beginning of the file again
            # Skip Header
            while True:
                line = f.readline().strip().upper()
                if line[:11] == '* * * GRUPO':
                    break

            self.groups_of_words = []
            words = []
            while True:
                line = f.readline().strip().upper()
                if f.tell() == end_location:
                    self.groups_of_words.append(sorted(words))
                    break
                if line[:11] == '* * * GRUPO':
                    self.groups_of_words.append(sorted(words))
                    words = []
                    continue
                if line == '':
                    continue
                words.append(line)
