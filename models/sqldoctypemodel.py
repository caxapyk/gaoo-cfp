from PyQt5.QtCore import QAbstractItemModel, QModelIndex


class SQLDoctypeModel(QAbstractItemModel):
    def __init__(self, data):
        super(SQLDoctypeModel, self).__init__()

        self.__data = data
        self.__root = QStandardItem(1,1)

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.__root.columnCount()

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.__root
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()
