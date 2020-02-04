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
        self.__data = data
        self.__columns = columns

        self.__root = SqlTreeItem(columns, -1)
        self.__root.map()

    def select(self):
        self.setupModelData()

    """
    Compose QSqlQueryModels into TreeView hierarchy.
    Each next model is child of previous.
    pos is current recursion position
    row is current row of parent model query, needed to set
    foreign key to current model
    """

    def setupModelData(self, parent=None, pos=0):
        # create instance of model
        model = self.__data[pos]

        if not parent:
            parent = self.__root
            name_col_id = 1

        if pos != 0:
            # set foreign key to current model
            model.setParentId(parent.uid())
            name_col_id = 2
            print("start fetch more: map")
            parent.map()

        model.refresh()

        i = 0
        while i < model.rowCount():
            # tuple of columns with data
            item_data = (model.data(model.index(i, name_col_id)),)

            item_id = model.data(model.index(i, 0))
            item = SqlTreeItem(item_data, pos, item_id, parent, model)

            parent.childAppend(item)
            i += 1

        print ("end setup model data")

    def hasChildren(self, index):
        print("start has children")
        if not index.isValid():
            return True

        item = index.internalPointer()
        child_level = item.level() + 1

        if child_level < len(self.__data):
            model = self.__data[child_level]
            model.setParentId(item.uid())

            if model.count() > 0:
                print("start has children: return True")
                return True
            print("start has children: return False")
        return False

    def canFetchMore(self, index):
        print("start canFetchMore")
        if not index.isValid():
            return False
        item = index.internalPointer()
        print("end canFetchMore")
        return not item.isMapped()

    def fetchMore(self, index):
        print("start fetch more")
        item = index.internalPointer()
        child_level = item.level() + 1
        print("start fetch more: setup model data")
        self.setupModelData(item, child_level)

        print("and fetch more")

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
            return self.__root.columnCount()

    """
    Implement
    """

    def rowCount(self, parent):
        if parent.column() > 0:
            return 0

        if not parent.isValid():
            parentItem = self.__root
        else:
            parentItem = parent.internalPointer()

        return parentItem.childCount()

    """
    (Implement) Returns QModelIndex to current TreeView item
    """

    def index(self, row, column, parent):
        #print("start get index")
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        if not parent.isValid():
            parentItem = self.__root
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

        if parentItem == self.__root:
            return QModelIndex()

        return self.createIndex(parentItem.row(), 0, parentItem)

    """
    (Implement) Returns data from internalPointer(to SQLItemModel) column
    """

    def data(self, index, role):
        #print("start show data")
        if not index.isValid():
            return None

        if role == Qt.DecorationRole:
        #    print("start show data: decorate")
            item_model = index.internalPointer().model()
            return item_model.getIcon()
        #print("start show data: end decorate")

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        #print("start show data: internalPointer")

        item = index.internalPointer()
        #print("end show data:")

        return item.data(index.column())

    """
    (Implement) Set column header to root node (passed to model class)
    """

    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.__columns[section]

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
            parent_item = self.__root

        new_item = None

        level = parent_item.level() + 1

        # create instance of model
        model = self.__data[level]

        if level != 0:
            # set foreign key (parent id) to the current model
            model.setParentId(parent_item.uid())

        # refresh model for an empty branch
        # if parent_item.childCount() == 0:
            # model.refresh()

        # set default name for a new item
        el_name = model.getNewItemName()

        result_id = model.insert(model.getNewItemName())
        child_count = parent_item.childCount()

        if result_id:
            # map parent if it has no children
            # it needed to refresh proxy model of qtreevew before expand
            if parent_item.childCount() == 0:
                parent_item.map()

            # use child_count to insert to top of branch, its needed for sort
            self.beginInsertRows(parent, child_count, child_count)

            new_item = SqlTreeItem(
                (el_name,), level, result_id, parent_item, model)

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
            parent_item = self.__root

        child_item = parent_item.child(row)

        if child_item.model().remove(child_item.uid()):
            self.beginRemoveRows(parent, row, row)

            parent_item.childRemove(child_item)

            self.endRemoveRows()

            return True

        return False
