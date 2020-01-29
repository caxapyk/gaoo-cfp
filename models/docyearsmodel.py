from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex, QAbstractListModel
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery, QSqlTableModel, QSqlRelation


class DocYearsModel(QAbstractListModel):
    def __init__(self, index):
        super(DocYearsModel, self).__init__()

        years = index.internalPointer().docyears()
        self.__data = years

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsEditable

    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.__data)
        else:
            return 0

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.row() > len(self.__data):
                return None

            item = self.__data[index.row()]

            return item

        return None

    def setData(self, index, value, role):
        if role != Qt.EditRole:
            return None

        self.__data[index.row()] = value
        # if item.model().update(item.uid(), value):
        #    item.setData((value,))

        return True

    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, row)

        self.__data.append("")

        self.endInsertRows()

        return True

    def removeRows(self, row, count, parent):
        self.beginRemoveRows(parent, row, row)

        i = 0
        while i < count:
            del self.__data[row]
            i += 1

        self.endRemoveRows()

        return True
