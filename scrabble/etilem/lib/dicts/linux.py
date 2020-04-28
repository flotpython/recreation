

class Dict():

    words = {}

    def __init__(self, locale="french"):

        intab = u"âàéêèîôû"
        outtab = u"aaeeeiou"
        transtab = dict((ord(a), b) for a, b in zip(intab, outtab))
        with open("/usr/share/dict/" + locale, "r") as fh:
            for line in fh.readlines():
                word = line.strip().translate(transtab).upper()
                if '-' in word or len(word) > 15:
                    continue
                key = ''.join(sorted(word))
                if key in self.words:
                    self.words[key].append(word)
                else:
                    self.words[key] = [word]
