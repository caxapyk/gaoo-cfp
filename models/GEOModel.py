from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractItemModel, QModelIndex


class GEOItem(object):
    def __init__(self, data, level, parent=None):
        self._parent = parent
        self._data = data
        self._children = []
        self._level = level

    def level(self):
        return self._level

    def childCount(self):
        return len(self._children)

    def columnCount(self):
        return len(self._data)

    def child(self, row):
        return self._children[row]

    def parent(self):
        return self._parent

    def childAppend(self, child):
        self._children.append(child)

    def row(self):
        if self._parent:
            return self._parent._children.index(self)

        return 0

    def data(self, section):
        try:
            return self._data[section]
        except IndexError:
            return None


class GEOModel(QAbstractItemModel):

    def __init__(self, model, model2, data):
        super(GEOModel, self).__init__()

        self._data = data

        self._root = GEOItem(("Территория", "Церковь"), 0)

        self.composeData(self._data)

    def composeData(self, data, parent=None, pos=0, row=0):
        if not parent:
            parent = self._root
        i = 0
        if len(data) > pos:
            while i < data[pos].rowCount():
                if (pos == 0):
                    item = GEOItem(
                        (data[pos].data(data[pos].index(i, 1)), ""), 1, parent)
                    self.composeData(data, item, 1, i)
                    parent.childAppend(item)

                else:
                    if data[pos].data(data[pos].index(i, 1)) == data[pos - 1].data(data[pos - 1].index(row, 0)):
                        item = GEOItem(
                            (data[pos].data(data[pos].index(i, 2)), ""), 1, parent)
                        self.composeData(data, item, pos + 1, i)
                        parent.childAppend(item)
                i += 1

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            #print("columnCount: ")
            # print(self._root.columnCount())
            return self._root.columnCount()

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self._root
        else:
            parentItem = parent.internalPointer()

        #print("child count",parentItem.childCount())

        return parentItem.childCount()

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self._root
        else:
            parentItem = parent.internalPointer()
            # print("------------")
            # print(parentItem.level())
            # print("------------")

        childItem = parentItem.child(row)
        #print("childItem: ", childItem)
        if childItem:
            index = self.createIndex(row, column, childItem)
            # print("hehe")
            return index
        else:
            return QModelIndex()

    def level(self, index):
        item = index.internalPointer()
        return item.level()

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self._root:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._root.data(section)

        return None
