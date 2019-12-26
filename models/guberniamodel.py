from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlQueryModel


"""
Gubernia
"""


class GuberniaModel(QSqlQueryModel):

    __m_parent_id = None

    def __init__(self):
        super(GuberniaModel, self).__init__()

        self.setHeaderData(0, Qt.Horizontal, "ID")
        self.setHeaderData(1, Qt.Horizontal, "Название губернии")

    def refresh(self):
        query = "SELECT * FROM cfp_gubernia"
        self.setQuery(query)

    def getParentId(self):
        return self.__m_parent_id

    def setParentId(self, parent_id):
        self.__m_parent_id = parent_id