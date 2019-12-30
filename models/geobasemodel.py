from PyQt5.QtSql import QSqlQueryModel, QSqlQuery


class GEOBaseModel(object):

    __model = None
    __m_table = None
    __m_parent_id = None
    __m_diplay_name = "Элемент"

    __m_fk = None

    def __init__(self):
        super(GEOBaseModel, self).__init__()
        self.__model = QSqlQueryModel()

    def rowCount(self):
        return self.__model.rowCount()

    def data(self, index):
        return self.__model.data(index)

    def index(self, row, col):
        return self.__model.index(row, col)

    def setTable(self, table_name):
        self.__m_table = table_name

    def getTable(self):
        return self.__m_table

    def getParentId(self):
        return self.__m_parent_id

    def setParentId(self, parent_id):
        self.__m_parent_id = parent_id

    def getNewItemName(self):
        return self.__m_diplay_name

    def setNewItemName(self, name):
        self.__m_diplay_name = name

    def setForeignKey(self, fk):
        self.__m_fk = fk

    def refresh(self):
        query = "SELECT * FROM %s" % self.__m_table

        if self.getParentId():
            query += " WHERE %s = ?" % self.__m_fk

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.getParentId():
            sql_query.addBindValue(self.__m_parent_id)

        if sql_query.exec_():
            self.__model.setQuery(sql_query)

    def insert(self, name):
        if self.__m_parent_id and self.__m_fk:
            query = "INSERT INTO %s (name, %s) \
                VALUES (?, ?)" % (self.__m_table, self.__m_fk)
        else:
            query = "INSERT INTO %s (name) VALUES (?)" % self.__m_table

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        sql_query.addBindValue(name)

        if self.__m_parent_id:
            sql_query.addBindValue(self.__m_parent_id)

        if sql_query.exec_() and sql_query.lastInsertId():
            return sql_query.lastInsertId()

        print(sql_query.lastError().text())

        return False

    def update(self, item_id, name):
        query = "UPDATE %s SET name = ? WHERE id = ?" % self.__m_table
        sql_query = QSqlQuery()
        sql_query.prepare(query)
        sql_query.addBindValue(name)
        sql_query.addBindValue(item_id)

        if sql_query.exec_():
            return True

        print(sql_query.lastError().text())

        return False

    def remove(self, item_id):
        query = "DELETE FROM %s WHERE id = ?" % self.__m_table
        sql_query = QSqlQuery()
        sql_query.prepare(query)
        sql_query.addBindValue(item_id)

        if sql_query.exec_():
            return True

        print(sql_query.lastError().text())

        return False

    def count(self):
        query = "SELECT COUNT(id) FROM %s" % self.__m_table

        if self.__m_parent_id:
            query += " WHERE %s = ?" % self.__m_fk

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.__m_parent_id:
            sql_query.addBindValue(self.getParentId())

        if sql_query.exec_():
            self.__model.setQuery(sql_query)
            return int(self.data(self.index(0, 0)))

        print(sql_query.lastError().text())

        return 0
