from PyQt5.Qt import Qt
from PyQt5.QtCore import QIdentityProxyModel


class DefaultItemProxyModel(QIdentityProxyModel):
    def __init__(self, default_column):
        super(DefaultItemProxyModel, self).__init__()
        self.default_column = default_column

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled

        rec = self.sourceModel().record(index.row())
        if (rec.value(self.default_column) == 1):
            return Qt.NoItemFlags

        return super().flags(index)
