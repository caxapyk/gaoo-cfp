from PyQt5.QtSql import QSqlTableModel


class FundModel(QSqlTableModel):
    def __init__(self):
        super(FundModel, self).__init__()

        self.setTable("cfp_fund")
