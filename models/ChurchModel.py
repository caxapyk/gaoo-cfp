from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel

"""
Locality
"""


class ChurchModel(QSqlQueryModel):

    m_parent_id = None
    modelDisplayName = "Церковь"

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

    def update(self, ch_id, name):
        if ch_id and name:
            query = "UPDATE cfp_church set name = ? WHERE id = ?"
            sql_query = QSqlQuery()
            sql_query.prepare(query)
            sql_query.addBindValue(name)
            sql_query.addBindValue(ch_id)
            sql_query.exec_()

    def remove(self, ch_id):
        if ch_id:
            query = "DELETE FROM cfp_church WHERE id = ?"
            sql_query = QSqlQuery()
            sql_query.prepare(query)
            sql_query.addBindValue(ch_id)
            sql_query.exec_()

    def insert(self, locality_id, name):
        if locality_id and locality_id:
            query = "INSERT INTO cfp_church (name, locality_id) VALUES (?, ?)"
            sql_query = QSqlQuery()
            sql_query.prepare(query)
            sql_query.addBindValue(name)
            sql_query.addBindValue(locality_id)
            sql_query.exec_()

            print(sql_query.lastError().text())
        if sql_query.lastInsertId():
            return sql_query.lastInsertId()
        return False

    def new_el_name(self):
        query = "SELECT name FROM cfp_church WHERE cfp_church.name LIKE ? ORDER BY cfp_church.id DESC LIMIT 1"

        search_name = self.modelDisplayName + "_%"
        el_name = self.modelDisplayName + " 1"

        sql_query = QSqlQuery()
        sql_query.prepare(query)
        sql_query.addBindValue(search_name)
        sql_query.exec_()

        if sql_query.last():
            ch_arr = str.split(sql_query.value(0), " ", 1)
            next_num = int(ch_arr[1]) + 1
            el_name = self.modelDisplayName + " " + str(next_num)

        return el_name


