from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractListModel


class CheckListProxyModel(QAbstractListModel):
    def __init__(self, parent):
        super(CheckListProxyModel, self).__init__(parent)

        self.parent = parent
        self.column = 0

        self.__data = []

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
            if index in self.__data:
                return Qt.Checked

            return Qt.Unchecked

        index = self.parent.index(index.row(), self.column)

        return self.parent.data(index, role)

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole:
            if value == Qt.Checked:
                self.__data.append(index)
                return True
            else:
                del self.__data[self.__data.index(index)]
                return True
        return False

    def setModelColumn(self, column):
        self.column = column

    def reset(self):
        self.__data.clear()
        self.modelReset.emit()
