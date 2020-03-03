from PyQt5.Qt import Qt
from PyQt5.QtCore import QSortFilterProxyModel
import re


class DocProxyModel(QSortFilterProxyModel):
    def __init__(self, ):
        super(DocProxyModel, self).__init__()

    def data(self, item, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if item.column() == 9:
                return item.row() + 1

        return super().data(item, role)

    def lessThan(self, left, right):
        # custom sort for storage unit column
        if left.column() == 12 and right.column() == 12:
            left_vals = re.findall(r'(\d+)', left.data())
            right_vals = re.findall(r'(\d+)', right.data())

            if len(left_vals) != len(right_vals):
                return super().lessThan(left, right)

            for i in range(0, len(left_vals)):
                if left_vals[i] != right_vals[i]:
                    return int(left_vals[i]) > int(right_vals[i])

            return True

        else:
            return super().lessThan(left, right)
