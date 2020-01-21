from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from PyQt5.QtGui import QIcon


class GEOBaseModel(QSqlQueryModel):
    def __init__(self):
        super(GEOBaseModel, self).__init__()
        self.m_table = None
        self.m_parent_id = None
        self.m_fk = None

        self.diplay_name = "Новый элемент"
        self.icon_resource = ":/icons/folder-16.png"

    def setTable(self, table_name):
        self.m_table = table_name

    def getTable(self):
        return self.m_table

    def getParentId(self):
        return self.m_parent_id

    def setParentId(self, parent_id):
        self.m_parent_id = parent_id

    def getNewItemName(self):
        return self.diplay_name

    def setNewItemName(self, name):
        self.diplay_name = name

    def setForeignKey(self, fk):
        self.m_fk = fk

    def setIconResource(self, resource):
        self.icon_resource = resource

    def getIcon(self):
        return QIcon(self.icon_resource)

    def refresh(self):
        query = "SELECT * FROM %s" % self.m_table

        if self.getParentId():
            query += " WHERE %s = ?" % self.m_fk

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.getParentId():
            sql_query.addBindValue(self.m_parent_id)

        if sql_query.exec_():
            self.setQuery(sql_query)
        else:
            self.printError(sql_query)

    def insert(self, name):
        if self.m_parent_id and self.m_fk:
            query = "INSERT INTO %s (name, %s) \
                VALUES (?, ?)" % (self.m_table, self.m_fk)
        else:
            query = "INSERT INTO %s (name) VALUES (?)" % self.m_table

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        sql_query.addBindValue(name)

        if self.m_parent_id:
            sql_query.addBindValue(self.m_parent_id)

        if sql_query.exec_() and sql_query.lastInsertId():
            return sql_query.lastInsertId()

        self.printError(sql_query)

        return False

    def update(self, item_id, name):
        query = "UPDATE %s SET name = ? WHERE id = ?" % self.m_table
        sql_query = QSqlQuery()
        sql_query.prepare(query)
        sql_query.addBindValue(name)
        sql_query.addBindValue(item_id)

        if sql_query.exec_():
            return True

        self.printError(sql_query)

        return False

    def remove(self, item_id):
        query = "DELETE FROM %s WHERE id = ?" % self.m_table
        sql_query = QSqlQuery()
        sql_query.prepare(query)
        sql_query.addBindValue(item_id)

        if sql_query.exec_():
            return True

        self.printError(sql_query)

        return False

    def count(self):
        query = "SELECT COUNT(id) FROM %s" % self.m_table

        if self.m_parent_id:
            query += " WHERE %s = ?" % self.m_fk

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.m_parent_id:
            sql_query.addBindValue(self.getParentId())

        if sql_query.exec_():
            self.setQuery(sql_query)
            return int(self.data(self.index(0, 0)))

        self.printError(sql_query)

        return 0

    def printError(self, sql_query):
        print("%s: %s" %
              (self.__class__.__name__, sql_query.lastError().text()))
