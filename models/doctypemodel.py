from PyQt5.QtSql import QSqlTableModel


class DoctypeModel(QSqlTableModel):
    def __init__(self):
        super(DoctypeModel, self).__init__()

        self.setTable("cfp_doctype")

    def getItemId(self, row):
        if row is not None and row <= self.rowCount():
            return self.record(row).value("id")
        else:
            return None
