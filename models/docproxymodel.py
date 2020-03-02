from PyQt5.Qt import Qt
from PyQt5.QtCore import QSortFilterProxyModel


class DocProxyModel(QSortFilterProxyModel):
    def __init__(self, ):
        super(DocProxyModel, self).__init__()

    def data(self, item, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if item.column() == 9:
                return item.row() + 1

        return super().data(item, role)
