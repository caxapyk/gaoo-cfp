from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel

"""
Uezd
"""


class UezdModel(QSqlQueryModel):

    __m_parent_id = None

    def __init__(self):
        super(UezdModel, self).__init__()

        self.setHeaderData(0, Qt.Horizontal, "ID")
        self.setHeaderData(1, Qt.Horizontal, "Название губернии")
        self.setHeaderData(2, Qt.Horizontal, "Название уезда")

    def refresh(self):
        print("i am here")
        query = "SELECT * FROM cfp_uezd"

        if self.getParentId():
            query += " WHERE gub_id = ?"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.getParentId():
            sql_query.addBindValue(self.getParentId())

        sql_query.exec_()

        self.setQuery(sql_query)

    def getParentId(self):
        return self.__m_parent_id

    def setParentId(self, parent_id):
        self.__m_parent_id = parent_id
