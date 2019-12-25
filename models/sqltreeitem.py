from PyQt5.QtWidgets import QAbstractItemView


class SQLTreeItem(QAbstractItemView):
    def __init__(self, data, level, model_item_id=None, parent=None, model=None):
        super(SQLTreeItem, self).__init__()
        self.parent_item = parent
        self.child_items = []
        self._data = data
        self._level = level
        self._id = model_item_id
        self._model = model

    def model(self):
        return self._model

    def level(self):
        return self._level

    def itemID(self):
        return self._id

    def setData(self, data):
        self._data = data

    def columnCount(self):
        return len(self._data)

    def parent(self):
        return self.parent_item

    def child(self, row):
        return self.child_items[row]

    def childCount(self):
        return len(self.child_items)

    def childAppend(self, child):
        self.child_items.append(child)

    def childRemove(self, child):
        self.child_items.remove(child)

    def row(self):
        # root has no parent
        if self.parent_item:
            return self.parent_item.child_items.index(self)

        return 0

    def data(self, section):
        return self._data[section]
