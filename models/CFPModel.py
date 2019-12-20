from PyQt5.QtCore import Qt
from PyQt5.QtSql import (QSqlQuery, QSqlRelation, QSqlRelationalDelegate, QSqlRelationalTableModel, QSqlTableModel)


class CFPModel:

    def __init__(self):
        self.model = QSqlRelationalTableModel()
        self.model.setTable('cfp_cfp')
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)
        self.model.setRelation(1, QSqlRelation('cfp_church', 'id', 'name'))
        self.model.setHeaderData(0, Qt.Horizontal, "ID")
        self.model.setHeaderData(1, Qt.Horizontal, "Название церкви")
        self.model.setHeaderData(2, Qt.Horizontal, "Другие сведения")

    def select(self):
        self.model.select()
        return self.model
