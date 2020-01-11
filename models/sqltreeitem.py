from PyQt5.QtWidgets import QAbstractItemView


class SqlTreeItem(QAbstractItemView):
    def __init__(self, data, level, uid=None, parent=None, model=None):
        super(SqlTreeItem, self).__init__()

        self.__parent = parent
        self.__children = []
        self.__data = data
        self.__level = level
        self.__uid = uid
        self.__model = model
        self.__mapped = False

    def map(self):
        self.__mapped = True

    def isMapped(self):
        return self.__mapped

    def model(self):
        return self.__model

    def level(self):
        return self.__level

    def uid(self):
        return self.__uid

    def parent(self):
        return self.__parent

    def child(self, row):
        if row >= 0:
            return self.__children[row]
        return None

    def childCount(self):
        return len(self.__children)

    def childAppend(self, child):
        self.__children.append(child)

    def childRemove(self, child):
        self.__children.remove(child)

    def columnCount(self):
        return len(self.__data)

    def row(self):
        # root has no parent
        if self.__parent:
            return self.__parent.__children.index(self)

        return 0

    def setData(self, data):
        self.__data = data

    def data(self, section):
        return self.__data[section]
