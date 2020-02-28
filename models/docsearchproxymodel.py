from PyQt5.Qt import Qt
from PyQt5.QtCore import QSortFilterProxyModel


class DocSearchProxyModel(QSortFilterProxyModel):
    def __init__(self, ):
        super(DocSearchProxyModel, self).__init__()

    def data(self, item, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if item.column() == 0:
                return item.row() + 1

        return super().data(item, role)
