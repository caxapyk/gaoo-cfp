from PyQt5.QtSql import QSqlQueryModel


class GEOBaseModel(QSqlQueryModel):

    __m_parent_id = None
    __m_diplay_name = "Элемент"

    def __init__(self):
        super(GEOBaseModel, self).__init__()

    def getParentId(self):
        return self.__m_parent_id

    def setParentId(self, parent_id):
        self.__m_parent_id = parent_id

    def getDisplayName(self):
        return self.__m_diplay_name

    def setDisplayName(self, name):
        self.__m_diplay_name = name

    def refresh(self):
        return False

    def insert(self, name):
        return False

    def update(self, item_id, name):
        return False

    def remove(self, item_id):
        return False
