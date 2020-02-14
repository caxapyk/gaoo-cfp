from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractListModel


class CheckListProxyModel(QAbstractListModel):
    def __init__(self, parent):
        super(CheckListProxyModel, self).__init__(parent)

        self.parent = parent
        self.column = 0

        self.__idx__ = []

        self.refresh()

    def refresh(self):
        if "select" in dir(self.parent):
            return self.parent.select()
        else:
            return self.parent.refresh()

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsUserCheckable

    def rowCount(self, parent):
        return self.parent.rowCount()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.CheckStateRole:
            if index in self.__idx__:
                return Qt.Checked

            return Qt.Unchecked

        index = self.parent.index(index.row(), self.column)

        return self.parent.data(index, role)

    def data_(self):
        data = []
        for index in self.__idx__:

            id_idx = self.parent.index(index.row(), 0)
            data.append(id_idx.data())

        data.sort()

        return ",".join(str(x) for x in data)

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole:
            if value == Qt.Checked:
                self.__idx__.append(index)
                return True
            else:
                del self.__idx__[self.__idx__.index(index)]
                return True
        return False

    def setModelColumn(self, column):
        self.column = column

    def reset(self):
        self.__idx__.clear()
        self.modelReset.emit()
