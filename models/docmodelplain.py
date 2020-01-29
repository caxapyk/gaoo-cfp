from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from .docmodel import DocModel
from utils import AbbrMaker


class DocModelPlain(DocModel):
    def __init__(self, church_id=None):
        super(DocModelPlain, self).__init__()

    def select(self):
        super().select()
        self.insertColumns(2, 1, QModelIndex())
        self.insertColumns(8, 2, QModelIndex())

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            item = index.internalPointer()

            if index.column() == 2:
                storage_unit = "Ф. %s Оп. %s Д. %s" % (
                    item.data(3),
                    item.data(4),
                    item.data(5))

                return storage_unit

            if index.column() == 8:
                return ','.join(index.internalPointer().docyears())

            if index.column() == 9:
                flag_list = [AbbrMaker().make(flag)
                             for flag in index.internalPointer().docflags()]

                return '/'.join(flag_list)

        return super().data(index, role)
