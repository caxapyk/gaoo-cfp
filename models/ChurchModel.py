from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel

"""
Locality
"""


class ChurchModel(QSqlQueryModel):

    m_parent_id = None

    def __init__(self):
        super(ChurchModel, self).__init__()

        self.setHeaderData(0, Qt.Horizontal, "ID")
        self.setHeaderData(1, Qt.Horizontal, "Населенный пункт")
        self.setHeaderData(2, Qt.Horizontal, "Название церкви")

    def refresh(self):
        query = "SELECT * FROM cfp_church"

        if self.m_parent_id:
            query += " WHERE locality_id = ?"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.m_parent_id:
            sql_query.addBindValue(self.m_parent_id)

        sql_query.exec_()

        self.setQuery(sql_query)

    def update(self, id, name):
        if id and name:
            query = "UPDATE cfp_church set name = ? WHERE id = ?"
            sql_query = QSqlQuery()
            sql_query.prepare(query)
            sql_query.addBindValue(name)
            sql_query.addBindValue(id)
            sql_query.exec_()

        return True

    def insert(self, locality_id, name ):
        if id and locality_id:
            query = "INSERT INTO cfp_church VALUES name = ? locality_id = ?"
            sql_query = QSqlQuery()
            sql_query.prepare(query)
            sql_query.addBindValue(locality_id)
            sql_query.addBindValue(name)
            sql_query.exec_()

        return True
