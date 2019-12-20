from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractItemModel, QModelIndex


class GEOItem(object):
    def __init__(self, model):
        self._model = model
        self._children = []

    def rowCount(self):
        return self._model.rowCount()

    def childCount(self):
            return len(self._children)
           #return self._model.rowCount()

    def columnCount(self):
        if self._model:
            return self._model.columnCount()

        return 3

    def child(self, row):
        return self._children[row]

    def childAppend(self, child):
        i = 0
        while i < child.rowCount():
            self._children.append(child)
            i = i+1


    def data(self, section):
        print("here data")
        return self._model.data(self._model.index(0, section))


class GEOModel(QAbstractItemModel):

    def __init__(self, model):
        super(GEOModel, self).__init__()
        self.model = model

        self.gub = GEOItem(self.model)

        self._root = GEOItem(self.model)
        self._root.childAppend(self.gub)




    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self._root.columnCount()


    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self._root
        else:
            parentItem = parent.internalPointer()

        print(parentItem.childCount())


        return parentItem.childCount()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():

            parentItem = self._root
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)
        print(childItem)
        if childItem:
            index = self.createIndex(row, column, childItem)
            print("hehe")
            return index
        else:
            return QModelIndex()


    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def headerData(self, section, orientation, role):
        print("here")
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.model.headerData(section, orientation, role)

        return None

