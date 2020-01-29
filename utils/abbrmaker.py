

class AbbrMaker():
    def make(self, string):
        abbr = ""
        for i, w in enumerate(string.upper().split()):
            if i > 2:
                break
            abbr += w[0]

        return abbr
