from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractItemModel, QModelIndex


class SQLTreeItem(object):
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
        # root has not parent
        if self._parent:
            return self._parent._children.index(self)

        return 0

    def data(self, section):
        return self._data[section]



class SQLTreeModel(QAbstractItemModel):
    """
    Note theat we assumed that the first column is always the primary key,
    and the second column is the foreign key related to the parent table
    (except for the first, root level).
    So these columns constitute the structure of the tree.
    This class inherit QAbstractItemModel and therefore implement the
    five pure virtual methods: columnCount, rowCount, index, parent and data.
    """

    def __init__(self, columns, data):
        super(SQLTreeModel, self).__init__()

        self._data = data

        self._columns = columns

        self._root = SQLTreeItem(columns, 0)

        self.composeData(self._data)

    """
    Compose QSqlQueryModels into TreeView hierarchy.
    Each next model is child of previous
    """
    def composeData(self, model, parent=None, pos=0, row=0):
        if not parent:
            parent = self._root
        i = 0
        if pos < len(model):
            while i < model[pos].rowCount():
                if (pos == 0):
                    item = SQLTreeItem(
                        (model[pos].data(model[pos].index(i, 1)), ""), pos, parent)
                    self.composeData(model, item, 1, i)
                    parent.childAppend(item)

                elif model[pos].data(model[pos].index(i, 1)) == model[pos - 1].data(model[pos - 1].index(row, 0)):
                    item = SQLTreeItem(
                        (model[pos].data(model[pos].index(i, 2)), ""), pos, parent)
                    self.composeData(model, item, pos + 1, i)
                    parent.childAppend(item)
                i += 1

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

        return parentItem.childCount()

    """
    Returns QModelIndex to current TreeView item
    """
    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self._root
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem.child(row)

        if childItem:
            index = self.createIndex(row, column, childItem)
            return index
        else:
            return QModelIndex()

    """
    Returns level of hierarchy from internalPointer(to SqlTreeItem) level
    """
    def level(self, index):
        item = index.internalPointer()
        return item.level()

    """
    Returns data from internalPointer(to SqlTreeItem) column
    """
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()

        childItem = index.internalPointer()
        parentItem = childItem.parent()

        if parentItem == self._root:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    """
    Returns data from internalPointer(to Item model) column
    """
    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    """
    Set column header to root node (passed to model class)
    """
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._columns[section]

        return None
