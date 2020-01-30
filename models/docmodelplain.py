from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from .docmodel import DocModel
from utils import AbbrMaker


class DocModelPlain(DocModel):
    def __init__(self, church_id=None):
        super(DocModelPlain, self).__init__(church_id)

    def select(self):
        super().select()
        self.insertColumns(2, 1, QModelIndex())
        self.insertColumns(8, 2, QModelIndex())

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            item = index.internalPointer()

            if index.column() == 20:
                rec = index.model().record(index.row())
                storage_unit = "Ф. %s Оп. %s Д. %s" % (
                    item.data(rec.indexOf("cfp_doc.fund")),
                    item.data(rec.indexOf("cfp_doc.inventory")),
                    item.data(rec.indexOf("cfp_doc.unit")))

                return storage_unit

            if index.column() == 80:
                return ','.join(index.internalPointer().docyears())

            if index.column() == 90:
                flag_list = [AbbrMaker().make(flag)
                             for flag in index.internalPointer().docflags()]

                return '/'.join(flag_list)

        return super().data(index, role)
