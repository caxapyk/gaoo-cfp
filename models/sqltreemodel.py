from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractItemModel, QModelIndex
from .sqltreeitem import SQLTreeItem


class SQLTreeModel(QAbstractItemModel):
    """
    Note theat we assumed that the first column is always the primary key,
    and the second column is the foreign key related to the parent table
    (except for the first, root level), third is name displayed in a TreeView.
    So these columns constitute the structure of the tree.
    This class inherit QAbstractItemModel and therefore implement the
    five pure virtual methods: columnCount, rowCount, index, parent and data.
    """

    def __init__(self, data, columns):
        super(SQLTreeModel, self).__init__()
        self._data = data
        self._columns = columns

        self.root = SQLTreeItem(columns, 0)

        self.setupModelData()

    """
    Compose QSqlQueryModels into TreeView hierarchy.
    Each next model is child of previous.
    pos is current recursion position
    row is current row of parent model query, needed to set
    foreign key to current model
    """

    def setupModelData(self, parent=None, pos=0):
        model = self._data[pos]

        if not parent:
            parent = self.root
            name_col_id = 1

        if pos != 0:
            # set foreign key to current model
            model.m_parent_id = parent.itemID()
            name_col_id = 2

        model.refresh()

        i = 0
        while i < model.rowCount():
            # tuple of columns with data
            item_data = (model.data(model.index(i, name_col_id)),)
            item_id = model.data(model.index(i, 0))
            item = SQLTreeItem(item_data, pos, item_id, parent, model)

            if pos < len(self._data) - 1:
                self.setupModelData(item, pos + 1)

            parent.childAppend(item)
            i += 1
    """
    Set flags (enabled, selectable, editable)
    """

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.root.columnCount()

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.root
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
            parentItem = self.root
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

        if parentItem == self.root:
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

    """
    Reimplement setData function (calls on edit)
    """

    def setData(self, index, value, role):
        if role != Qt.EditRole:
            return None

        item = index.internalPointer()

        item_model = item.model()
        item_id = item_model.getId(item.row())

        item_model.update(item_id, value)

        item.setData((value,))

        return True

    def insertRow(self, row, parent):
        self.beginInsertRows(parent, row, row)

        parent_item = parent.internalPointer()
        child_item = parent_item.child(row)

        parent_model = parent_item.model()
        parent_id  = parent_model.getId(parent_item.row())

        child_model = child_item.model()
        el_name = child_model.new_el_name()

        result_id = child_model.insert(parent_id, el_name)

        if result_id:
            new_item = SQLTreeItem((el_name, ""), 0, result_id , parent_item, child_model)
            parent_item.childAppend(new_item)

        self.endInsertRows()

    def removeRow(self, row, parent):
        self.beginRemoveRows(parent, row, row)

        parent_item = parent.internalPointer()
        child_item = parent_item.child(row)

        level = child_item.level()

        self._data[level].remove(child_item.itemID())
        parent_item.childRemove(child_item)

        self.endRemoveRows()
