from PyQt5.Qt import Qt
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from utils import AbbrMaker


class DocModelPlain(QSqlQueryModel):
    def __init__(self, church_id=None):
        super(DocModelPlain, self).__init__()

        self.__church_id = church_id

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

        if self.__church_id:
            query += " WHERE cfp_doc.church_id = ?"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.__church_id:
            sql_query.addBindValue(self.__church_id)

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
