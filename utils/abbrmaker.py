

class AbbrMaker():
    def make(self, string):
        abbr = ""
        for item in string.split(","):
            for i, w in enumerate(item.upper().split()):
                if i > 2:
                    break
                abbr += w[0]
            abbr += "/"

        return abbr[:-1]
