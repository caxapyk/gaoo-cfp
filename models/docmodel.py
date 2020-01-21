from PyQt5.QtSql import QSqlQueryModel, QSqlQuery


class DocModel(QSqlQueryModel):
    def __init__(self):
        super(DocModel, self).__init__()

        self.church_id = None

    def setChurchId(self, church_id):
        self.church_id = church_id

    def refresh(self):
        query = "SELECT * FROM cfp_doc"

        if self.church_id:
            query += " WHERE church_id = ?"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.church_id:
            sql_query.addBindValue(self.church_id)

        if sql_query.exec_():
            self.setQuery(sql_query)
        else:
            self.printError(sql_query)

    def printError(self, sql_query):
        print("%s: %s" %
              (self.__class__.__name__, sql_query.lastError().text()))
