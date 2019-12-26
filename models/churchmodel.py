from PyQt5.QtSql import QSqlQuery
from models import GEOBaseModel

"""
Church Model
"""


class ChurchModel(GEOBaseModel):

    def __init__(self):
        super(ChurchModel, self).__init__()
        self.setDisplayName("Церковь")

    def refresh(self):
        query = "SELECT * FROM cfp_church"

        if self.getParentId():
            query += " WHERE cfp_church.locality_id = ?"

        query += " ORDER BY cfp_church.id"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.getParentId():
            sql_query.addBindValue(self.getParentId())

        sql_query.exec_()

        self.setQuery(sql_query)

    def insert(self, name):
        query = "INSERT INTO cfp_church (cfp_church.name, cfp_church.locality_id) \
                VALUES (?, ?)"
        sql_query = QSqlQuery()
        sql_query.prepare(query)
        sql_query.addBindValue(name)
        sql_query.addBindValue(self.getParentId())

        if(sql_query.exec_() and sql_query.lastInsertId()):
            return sql_query.lastInsertId()

        return False

    def update(self, item_id, name):
        query = "UPDATE cfp_church SET cfp_church.name = ? \
            WHERE cfp_church.id = ?"
        sql_query = QSqlQuery()
        sql_query.prepare(query)
        sql_query.addBindValue(name)
        sql_query.addBindValue(item_id)

        if(sql_query.exec_()):
            return True

        print(sql_query.lastError())

        return False

    def remove(self, item_id):
        query = "DELETE FROM cfp_church WHERE cfp_church.id = ?"
        sql_query = QSqlQuery()
        sql_query.prepare(query)
        sql_query.addBindValue(item_id)
        if(sql_query.exec_()):
            return True

        print(sql_query.lastError())

        return False
