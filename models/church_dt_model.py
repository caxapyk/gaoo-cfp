from PyQt5.Qt import Qt
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery


class ChurchDTModel(QSqlQueryModel):
    __uid = None

    def __init__(self, uid):
        super(ChurchDTModel, self).__init__()
        self.__uid = uid

    def refresh(self):
        query = "SELECT * FROM cfp_doctype"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if sql_query.exec_():
            self.setQuery(sql_query)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.CheckStateRole:
            # some function for checkstate
            return Qt.Checked

        return super().data(index, role)
