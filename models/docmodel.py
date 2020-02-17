from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlRelation, QSqlQuery
from utils import AbbrMaker


class DocModel(QSqlRelationalTableModel):
    def __init__(self):
        super(DocModel, self).__init__()

        self.setTable("cfp_doc")
        self.setRelation(2, QSqlRelation(
            "cfp_doctype", "id", "name AS `cfp_doctype.name`"))

        self.__church_id__ = None
        self.__cache_years__ = {}
        self.__cache_flags__ = {}

    def setChurch(self, church_id):
        self.__church_id__ = church_id

    def churchId(self):
        return self.__church_id__

    def data(self, item, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if item.column() == 8:
                return item.row() + 1

            elif item.column() == 9:
                rec = self.record(item.row())
                val = rec.value("cfp_doctype.name")
                if isinstance(val, str):
                    doctype_abbr = AbbrMaker().make(val)
                    return doctype_abbr

                return ""

            elif item.column() == 10:
                rec = self.record(item.row())

                storage_unit = "Ф. %s Оп. %s Д. %s" % (
                    rec.value("cfp_doc.fund"),
                    rec.value("cfp_doc.inventory"),
                    rec.value("cfp_doc.unit"))

                return storage_unit

            if item.column() == 11:
                rec = self.record(item.row())
                return rec.value("cfp_doc.sheets")

            if item.column() == 12:
                return self.docYears(item.row())

            elif item.column() == 13:
                val = self.docFlags(item.row())
                if isinstance(val, str):
                    return AbbrMaker().make(val)

            if item.column() == 14:
                rec = self.record(item.row())
                return rec.value("cfp_doc.comment")

        return super().data(item, role)

    def docYears(self, row):
        if row is None:
            return None

        # get years from local varible
        if self.__cache_years__.get(row) is not None:
            return self.__cache_years__[row]

        doc_id = self.getItemId(row)

        query = "SELECT \
        (SELECT GROUP_CONCAT(cfp_docyears.year ORDER BY cfp_docyears.year) \
        FROM cfp_docyears WHERE cfp_docyears.doc_id=%s) AS years\
        FROM cfp_docyears WHERE cfp_docyears.doc_id=%s" % (doc_id, doc_id)

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return None

        sql_query.last()
        y_rec = sql_query.record().value("years")

        # set flags to local varible
        self.__cache_years__[row] = y_rec

        return y_rec

    def docFlags(self, row):
        if row is None:
            return None

        # get flags from local varible
        if self.__cache_flags__.get(row) is not None:
            return self.__cache_flags__[row]

        doc_id = self.getItemId(row)

        query = "SELECT \
        (SELECT GROUP_CONCAT(cfp_docflag.name ORDER BY cfp_docflag.name) \
        FROM cfp_docflags LEFT JOIN cfp_docflag \
        ON cfp_docflags.docflag_id=cfp_docflag.id \
        WHERE cfp_docflags.doc_id=%s) AS flags \
        FROM cfp_docflags WHERE cfp_docflags.doc_id=%s" % (doc_id, doc_id)

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return None

        sql_query.last()
        y_rec = sql_query.record().value("flags")

        # set flags to local varible
        self.__cache_flags__[row] = y_rec

        return y_rec

    def clearCache(self, row):
        # clear cached years
        if self.__cache_years__.get(row) is not None:
            del self.__cache_years__[row]

        # clear cached flags
        if self.__cache_flags__.get(row) is not None:
            del self.__cache_flags__[row]

    def select(self):
        if super().select():
            self.insertColumns(8, 7, QModelIndex())

            self.setHeaderData(8, Qt.Horizontal, "#")
            self.setHeaderData(9, Qt.Horizontal, "Тип документа")
            self.setHeaderData(10, Qt.Horizontal, "Ед. хранения")
            self.setHeaderData(11, Qt.Horizontal, "Листов")
            self.setHeaderData(12, Qt.Horizontal, "Годы документов")
            self.setHeaderData(13, Qt.Horizontal, "Флаги")
            self.setHeaderData(14, Qt.Horizontal, "Комментарий")

            self.__cache_years__.clear()
            self.__cache_flags__.clear()

            return True
        else:
            return False

    def locality(self):
        if self.rowCount() > 0:
            # used in search model
            if self.churchId():
                churchId = self.churchId()
            else:
                churchId = self.record(0).value("cfp_doc.church_id")

            query = "SELECT \
            cfp_church.id AS `cfp_church.id`, \
            cfp_church.name AS `cfp_church.name`, \
            cfp_gubernia.name AS `cfp_gubernia.name`, \
            cfp_uezd.name AS `cfp_uezd.name`, \
            cfp_locality.name AS `cfp_locality.name` \
            FROM cfp_church \
            LEFT JOIN cfp_locality ON cfp_church.locality_id = cfp_locality.id \
            LEFT JOIN cfp_uezd ON cfp_locality.uezd_id = cfp_uezd.id \
            LEFT JOIN cfp_gubernia ON cfp_uezd.gub_id = cfp_gubernia.id \
            WHERE cfp_church.id=%s" % churchId

            sql_query = QSqlQuery()
            sql_query.prepare(query)

            if not sql_query.exec_():
                print(sql_query.lastError().text())
                return None

            sql_query.last()

            val = "%s, %s, %s, %s" % (
                sql_query.value("cfp_gubernia.name"),
                sql_query.value("cfp_uezd.name"),
                sql_query.value("cfp_locality.name"),
                sql_query.value("cfp_church.name"))

            return val
        return ""

    def getItemId(self, row):
        if row is not None and row <= self.rowCount():
            return self.record(row).value("id")
        else:
            return None
