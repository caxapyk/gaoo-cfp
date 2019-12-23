from PyQt5 import QtCore
from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractItemModel, QModelIndex, pyqtSignal


class SQLTreeItem(object):
    def __init__(self, data, level, itemId = None, parent=None):
        self._parent = parent
        self._data = data
        self._children = []
        self._level = level
        self._id = itemId

    def level(self):
        return self._level

    def setData(self, data):
        self._data = data

    def itemID(self):
        return self._id

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
    (except for the first, root level), third is name displayed in a TreeView.
    So these columns constitute the structure of the tree.
    This class inherit QAbstractItemModel and therefore implement the
    five pure virtual methods: columnCount, rowCount, index, parent and data.
    """

    def __init__(self, columns, data):
        super(SQLTreeModel, self).__init__()

        self.data_changed = pyqtSignal(QModelIndex, QModelIndex)

        self._data = data

        self._columns = columns

        self._root = SQLTreeItem(columns, 0)

        self.composeData()


    """
    Compose QSqlQueryModels into TreeView hierarchy.
    Each next model is child of previous.
    pos is current recursion position
    row is current row of parent model query, needed to set
    foreign key to current model
    """
    def composeData(self, parent=None, pos=0, row=0):
        _m = self._data
        # top level model has not foreign key column
        name_column_id = 1
        if not parent:
            parent = self._root
        i = 0
        if pos < len(_m):
            if pos == 0:
                _m[pos].m_parent_id = None
            else:
                # set foreign key to current model
                _m[pos].m_parent_id = _m[pos - 1].data(_m[pos - 1].index(row, 0))
                name_column_id = 2

            _m[pos].refresh()

            while i < _m[pos].rowCount():
                # display name
                item = SQLTreeItem((_m[pos].data(_m[pos].index(i, name_column_id)), ""), pos, _m[pos].data(_m[pos].index(i, 0)), parent)
                self.composeData(item, pos + 1, i)
                parent.childAppend(item)
                i += 1

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

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

        if role != Qt.DisplayRole and role != Qt.EditRole:
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

    def setData(self, index, value, role):
        if role != Qt.EditRole:
            return None

        item = index.internalPointer()
        level = index.internalPointer().level()

        self._data[level].update(item.itemID(), value)
        #self.dataChanged.emit(index, index)
        item.setData((value,)) # не нравится мне этот вариант, нужен reresh модели on dataChanged

        #self.resetInternalData()

        return True

    def insertRow(self, row, parent):
        self.beginInsertRows(parent, row, row)
        parentItem = parent.internalPointer()
        item = SQLTreeItem(("Тест", ""), 1, "100", parentItem)
        parentItem.childAppend(item)
        self.endInsertRows()
