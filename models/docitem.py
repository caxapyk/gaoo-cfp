from PyQt5.QtWidgets import QAbstractItemView


class DocItem(QAbstractItemView):
    def __init__(self, data, years=None, flags=None):
        super(DocItem, self).__init__()

        self.__data = data

        self.__years = years
        self.__flags = flags

    def setData(self, data, column):
        self.__data[column] = data

    def indexOf(self, field):
        return self.__column.index(field)

    def data(self, section):
        return self.__data[section]

    def docyears(self):
        return self.__years

    def docflags(self):
        return self.__flags

    #def insertColumn(self, column):
    #    self.__data.insert(column, "")
