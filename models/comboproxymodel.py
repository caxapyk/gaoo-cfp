from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractListModel


class ComboProxyModel(QAbstractListModel):
    def __init__(self, parent, column=0):
        super(ComboProxyModel, self).__init__(parent)

        self.parent = parent
        self.column = 0

        self.refresh()

    def refresh(self):
        if "select" in dir(self.parent):
            return self.parent.select()
        else:
            return self.parent.refresh()

    def rowCount(self, parent):
        return self.parent.rowCount() + 1

    def data(self, index, role):
        if not index.isValid():
            return None

        if index.row() == 0:
            if role == Qt.DisplayRole:
                return "(Выберите из списка)"

        index = self.parent.index(index.row() - 1, self.column)

        return self.parent.data(index, role)

    def setModelColumn(self, column):
        self.column = column
