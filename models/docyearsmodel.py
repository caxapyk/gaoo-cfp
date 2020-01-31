from PyQt5.QtSql import QSqlTableModel

class DocYearsModel(QSqlTableModel):
    def __init__(self):
        super(DocYearsModel, self).__init__()

        self.setTable("cfp_docyears")
        self.setEditStrategy(QSqlTableModel.OnManualSubmit)
