import re


class ItemDefaultName():
    def __init__(self, parent, prefix):
        self.parent_item = parent
        self.prefix = prefix

        self.regex = r'\w+ \d+'
        self.splitter = " "

    def process(self):
        i = 0
        el_num = 1
        while i < self.parent_item.childCount():

            el_text = self.parent_item.child(i).data(0)

            if re.fullmatch(self.regex, el_text):
                split_arr = str.split(el_text, self.splitter, 1)
                cur_num = int(split_arr[1])
                if cur_num >= el_num:
                    el_num = cur_num + 1
            i += 1

        el_name = self.prefix + self.splitter + str(el_num)

        return el_name
