from PyQt5.Qt import Qt
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtGui import QBrush


class SqlListModel(QSqlTableModel):
    def __init__(self):
        super(SqlListModel, self).__init__()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.ForegroundRole:
            # check if field is default
            rec = self.record(index.row())
            if (rec.value("dfield") == 1):
                return QBrush(Qt.gray)

        return super().data(index, role)
