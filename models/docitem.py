from PyQt5.QtWidgets import QAbstractItemView


class DocItem(QAbstractItemView):
    def __init__(self, data):
        super(DocItem, self).__init__()

        self.__data = data

    def setData(self, data, column):
        self.__data[column] = data

    def indexOf(self, field):
        return self.__column.index(field)

    def data(self, section):
        return self.__data[section]

    #def insertColumn(self, column):
    #    self.__data.insert(column, "")