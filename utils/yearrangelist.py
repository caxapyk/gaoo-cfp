

class YearRangeList():
    def make(self, y_list):
        i = 0
        count = 0
        print(y_list)

        if len(y_list) == 1 and y_list[0] == "":
            return "не указаны"

        y_str = ""

        while i <= len(y_list) - 1:
            j = i
            delimeter = ","
            while j < len(y_list) - 1:
                curr_y = int(y_list[j])
                next_y = int(y_list[j + 1])
                if (next_y - curr_y) == 1:
                    count += 1
                else:
                    break
                j += 1

            if count > 1:
                delimeter = "-"

            while count:
                if count > 1:
                    del y_list[i + 1]
                count -= 1

            y_str += "%s%s" % (y_list[i], delimeter)
            i += 1

        return y_str[:-1]
