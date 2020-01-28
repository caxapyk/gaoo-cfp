from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from .docmodel import DocModel


class DocModelPlain(DocModel):
    def __init__(self, church_id=None):
        super(DocModelPlain, self).__init__()

    def select(self):
        super().select()
        self.insertColumn(2, QModelIndex())

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:
            item = index.internalPointer()

            if index.column() == 2:
                rec = self.record(index.row())

                storage_unit = "Ф. %s Оп. %s Д. %s" % (
                    item.data(rec.indexOf("cfp_doc.fund")),
                    item.data(rec.indexOf("cfp_doc.inventory")),
                    item.data(rec.indexOf("cfp_doc.unit")))

                return storage_unit

        return super().data(index, role)
