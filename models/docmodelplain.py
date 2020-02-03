from PyQt5.Qt import Qt
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from utils import AbbrMaker


class DocModelPlain(QSqlQueryModel):
    def __init__(self):
        super(DocModelPlain, self).__init__()

        self.__church_id__ = None
        self.__last_insert_id__ = None

    def setChurch(self, id):
        self.__church_id__ = id

    def getChurchId(self):
        return self.__church_id__

    def lastInsertId(self):
        return self.__last_insert_id__

    def data(self, item, role):
        if role == Qt.DisplayRole:
            if item.column() == 0:
                return item.row() + 1

            elif item.column() == 1:
                rec = self.record(item.row())
                doctype_abbr = AbbrMaker().make(
                    rec.value("cfp_doctype.name"))

                return doctype_abbr

            elif item.column() == 5:
                rec = self.record(item.row())

                storage_unit = "Ф. %s Оп. %s Д. %s" % (
                    rec.value("cfp_doc.fund"),
                    rec.value("cfp_doc.inventory"),
                    rec.value("cfp_doc.unit"))

                return storage_unit
        return super().data(item, role)

    def refresh(self):
        query = "SELECT \
        cfp_doc.id AS `cfp_doc.id`, \
        cfp_doc.church_id AS `cfp_doc.church_id`, \
        cfp_doc.doctype_id AS `cfp_doc.doctype_id`, \
        cfp_doctype.name AS `cfp_doctype.name`, \
        cfp_doc.fund AS `cfp_doc.fund`, \
        cfp_doc.inventory AS `cfp_doc.inventory`, \
        cfp_doc.unit AS `cfp_doc.unit`, \
        cfp_doc.sheets AS `cfp_doc.sheets`, \
        cfp_doc.comment AS `cfp_doc.comment`, \
        (SELECT GROUP_CONCAT(year) FROM cfp_docyears WHERE cfp_docyears.doc_id = cfp_doc.id) AS years, \
        (SELECT GROUP_CONCAT(cfp_docflag.name) FROM cfp_docflags LEFT JOIN cfp_docflag ON cfp_docflags.docflag_id=cfp_docflag.id WHERE cfp_docflags.doc_id = cfp_doc.id) AS flags \
        FROM cfp_doc \
        LEFT JOIN cfp_doctype ON cfp_doc.doctype_id=cfp_doctype.id"

        if self.__church_id__:
            query += " WHERE cfp_doc.church_id = ?"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.__church_id__:
            sql_query.addBindValue(self.__church_id__)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return None

        self.setQuery(sql_query)

        # insert columns for counter and type abbr fields
        self.insertColumns(0, 2)
        # insert column for storage_unit field
        self.insertColumns(5, 1)
        # insert column for years and flags fields
        self.insertColumns(10, 2)

    def insert(self, data):
        query = "INSERT INTO cfp_doc \
            (church_id, doctype_id, fund, inventory, unit, sheets, comment) \
            VALUES(?,?,?,?,?,?,?)"
        
        sql_query = QSqlQuery()
        sql_query.prepare(query)

        sql_query.addBindValue(data["cfp_doc.church_id"])
        sql_query.addBindValue(data["cfp_doc.doctype_id"])
        sql_query.addBindValue(data["cfp_doc.fund"])
        sql_query.addBindValue(data["cfp_doc.inventory"])
        sql_query.addBindValue(data["cfp_doc.unit"])
        sql_query.addBindValue(data["cfp_doc.sheets"])
        sql_query.addBindValue(data["cfp_doc.comment"])

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return False

        if sql_query.lastInsertId():
            self.__last_insert_id__ = sql_query.lastInsertId()
            data["cfp_doc.id"] = self.__last_insert_id__

            if not self.update_years(data) or not self.update_flags(data):
                return False
        else:
            return False

        return True


    def update(self, data):
        if not self.update_years(data) or not self.update_flags(data):
            return False

        query = "UPDATE cfp_doc SET church_id=?, doctype_id=?, fund=?, inventory=?, unit=?, sheets=?, comment=? WHERE id=?"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        sql_query.addBindValue(data["cfp_doc.church_id"])
        sql_query.addBindValue(data["cfp_doc.doctype_id"])
        sql_query.addBindValue(data["cfp_doc.fund"])
        sql_query.addBindValue(data["cfp_doc.inventory"])
        sql_query.addBindValue(data["cfp_doc.unit"])
        sql_query.addBindValue(data["cfp_doc.sheets"])
        sql_query.addBindValue(data["cfp_doc.comment"])
        sql_query.addBindValue(data["cfp_doc.id"])

        print(sql_query.lastQuery())

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return False

        return True

    def update_years(self, data):
        sql_query = QSqlQuery()
        
        query = "DELETE FROM cfp_docyears \
        WHERE doc_id=%s" % data["cfp_doc.id"]

        sql_query.prepare(query)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return False
        
        if len(data["years"]) > 0:
            years = []
            for y in data["years"]:
                row = "(%s, %s)" % (data["cfp_doc.id"], y)
                years.append(row)

            query = "INSERT INTO cfp_docyears \
                (doc_id, year) VALUES %s" % ",".join(years)

            sql_query.prepare(query)

            if not sql_query.exec_():
                print(sql_query.lastError().text())
                return False

        return True

    def update_flags(self, data):
        sql_query = QSqlQuery()
        
        query = "DELETE FROM cfp_docflags \
        WHERE doc_id=%s" % data["cfp_doc.id"]

        sql_query.prepare(query)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return False
        
        if len(data["flags"]) > 0:
            flags = []
            for f in data["flags"]:
                row = "(%s, %s)" % (data["cfp_doc.id"], f)
                flags.append(row)

            query = "INSERT INTO cfp_docflags \
                (doc_id, docflag_id) VALUES %s" % ",".join(flags)

            sql_query.prepare(query)

            if not sql_query.exec_():
                print(sql_query.lastError().text())
                return False

        return True

    def remove(self, doc_id):
        # docyears and docflags removes by ON CASCADE MYSQL feature
        query = "DELETE FROM cfp_doc WHERE id=%s" % doc_id

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        print(sql_query.lastQuery())

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return False

        return True

