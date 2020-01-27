from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery, QSqlTableModel, QSqlRelation


class YearsModel(QSqlTableModel):
    def __init__(self):
        super(YearsModel, self).__init__()

        self.setTable("cfp_docyears")
