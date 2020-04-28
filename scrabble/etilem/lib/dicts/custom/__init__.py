
import os


class Dict():

    words = {}

    def __init__(self, locale="french"):
        filename = os.path.join(os.path.dirname(__file__), locale)
        with open(filename, "r") as fh:
            for line in fh.readlines():
                word = line.strip()
                key = ''.join(sorted(word))
                if key in self.words:
                    self.words[key].append(word)
                else:
                    self.words[key] = [word]
