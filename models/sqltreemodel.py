from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractItemModel, QModelIndex
from .sqltreeitem import SqlTreeItem


class SqlTreeModel(QAbstractItemModel):
    """
    Note theat we assumed that the first column is always the primary key,
    and the second column is the foreign key related to the parent table
    (except for the first, root level), third is name displayed in a TreeView.
    So these columns constitute the structure of the tree.
    This class inherit QAbstractItemModel and therefore implement the
    virtual methods.
    """

    def __init__(self, data, columns):
        super(SqlTreeModel, self).__init__()
        self.data = data
        self.columns = columns
        self.model_columns = {}

        self.root = SqlTreeItem(columns, -1)
        self.root.map()

    def select(self):
        self.setupModelData()

    def setModelColumn(self, level, column):
        self.model_columns[level] = column

    """
    Compose QSqlQueryModels into TreeView hierarchy.
    Each next model is child of previous.
    pos is current recursion position
    row is current row of parent model query, needed to set
    foreign key to current model
    """

    def setupModelData(self, parent=None, pos=0):
        # create instance of model
        model = self.data[pos]

        if not parent:
            parent = self.root

        # set parent for top level nodes
        if pos != 0:
            # set foreign key to current model
            model.setParentId(parent.uid())

        # map parent
        parent.map()

        name_col_id = 0

        if self.model_columns.get(pos):
            name_col_id = self.model_columns[pos]

        model.refresh()

        i = 0
        while i < model.rowCount():
            # tuple of columns with data
            item_data = (model.data(model.index(i, name_col_id)),)

            item_id = model.data(model.index(i, 0))
            item = SqlTreeItem(item_data, pos, item_id, parent, model)

            parent.childAppend(item)
            i += 1

    def hasChildren(self, index):
        if not index.isValid():
            return True

        item = index.internalPointer()
        child_level = item.level()

        # change level for multilevel model
        if len(self.data) > 1:
            child_level += 1

        if child_level < len(self.data):
            model = self.data[child_level]
            model.setParentId(item.uid())

            if model.count() > 0:
                return True

        return False

    def canFetchMore(self, index):
        if not index.isValid():
            return False
        item = index.internalPointer()
        return not item.isMapped()

    def fetchMore(self, index):
        item = index.internalPointer()
        child_level = item.level()
        # change level for multilevel model
        if len(self.data) > 1:
            child_level += 1

        self.setupModelData(item, child_level)

    """
    (Implement) Set flags (enabled, selectable, editable)
    """

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsEditable

    """
    Implement
    """

    def columnCount(self, parent):
        if parent.isValid():
            return parent.internalPointer().columnCount()
        else:
            return self.root.columnCount()

    """
    Implement
    """

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.root
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    """
    (Implement) Returns QModelIndex to current TreeView item
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
    (Implement) Returns parent QModelIndex
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
    (Implement) Returns data from internalPointer(to SQLItemModel) column
    """

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DecorationRole:
            item_model = index.internalPointer().model()
            return item_model.getIcon()

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    """
    (Implement) Set column header to root node (passed to model class)
    """

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.columns[section]

        return None

    """
    (Implement) calls on item edit
    """

    def setData(self, index, value, role):
        if role != Qt.EditRole:
            return None

        item = index.internalPointer()

        if len(value) > 0:
            if item.model().update(item.uid(), value):
                item.setData((value,))

            return True

        return False

    """
    Implement insertRow function (calls on insert)
    """

    def insertRows(self, row, count, parent):
        if parent.isValid():
            parent_item = parent.internalPointer()
        else:
            parent_item = self.root

        new_item = None

        child_level = parent_item.level()

        # change level for multilevel model
        if len(self.data) > 1:
            child_level += 1

        # create instance of model
        model = self.data[child_level]

        if child_level != 0:
            # set foreign key (parent id) to the current model
            model.setParentId(parent_item.uid())

        # refresh model for an empty branch
        # if parent_item.childCount() == 0:
            # model.refresh()

        # set default name for a new item
        el_name = model.newItemName()

        result_id = model.insert(model.newItemName())
        child_count = parent_item.childCount()

        if result_id:
            # map parent if it has no children
            # it needed to refresh proxy model of qtreevew before expand
            if parent_item.childCount() == 0:
                parent_item.map()

            # use child_count to insert to top of branch, its needed for sort
            self.beginInsertRows(parent, child_count, child_count)

            new_item = SqlTreeItem(
                (el_name,), child_level, result_id, parent_item, model)

            parent_item.childAppend(new_item)

            self.endInsertRows()

            return True

        return False

    """
    Implement removeRow function (calls on remove)
    """

    def removeRows(self, row, count, parent):
        if parent.isValid():
            parent_item = parent.internalPointer()
        else:
            parent_item = self.root

        child_item = parent_item.child(row)

        if child_item.model().remove(child_item.uid()):
            self.beginRemoveRows(parent, row, row)

            parent_item.childRemove(child_item)

            self.endRemoveRows()

            return True

        return False
