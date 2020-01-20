from PyQt5.QtSql import QSqlTableModel

class DocflagModel(QSqlTableModel):
    def __init__(self):
        super(DocflagModel, self).__init__()

        self.setTable("cfp_docflag")
