from PyQt5.QtWidgets import QAbstractItemView


class DocItem(QAbstractItemView):
    def __init__(self, data):
        super(DocItem, self).__init__()

        self.__data = data

    def setData(self, column, data):
        self.__data[column] = data

    def indexOf(self, field):
        return self.__column.index(field)

    def data(self, section):
        return self.__data[section]

    def insertColumns(self, column, count):
        i = 0
        while i < count:
            self.__data.insert(column, "")
            i += 1
