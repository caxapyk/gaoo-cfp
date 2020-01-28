from PyQt5.QtWidgets import QAbstractItemView


class DocItem(QAbstractItemView):
    def __init__(self, data=None, years=None, flags=None):
        super(DocItem, self).__init__()

        self.__data = data
        self.__years = years
        self.__flags = flags

    def columnCount(self):
        return len(self.__data)

    def setData(self, data, column):
        self.__data[column] = data

    def data(self, section):
        return self.__data[section]

    def years(self):
        return self.__years

    def flags(self):
        return self.__flags

    def insertColumn(self, column):
        self.__data.insert(column, "")