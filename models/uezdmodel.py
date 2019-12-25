from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel

"""
Uezd
"""


class UezdModel(QSqlQueryModel):

    m_parent_id = None

    def __init__(self):
        super(UezdModel, self).__init__()

        self.setHeaderData(0, Qt.Horizontal, "ID")
        self.setHeaderData(1, Qt.Horizontal, "Название губернии")
        self.setHeaderData(2, Qt.Horizontal, "Название уезда")

    def refresh(self):
        print("i am here")
        query = "SELECT * FROM cfp_uezd"

        if self.m_parent_id:
            query += " WHERE gub_id = ?"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.m_parent_id:
            sql_query.addBindValue(self.m_parent_id)

        sql_query.exec_()

        self.setQuery(sql_query)

