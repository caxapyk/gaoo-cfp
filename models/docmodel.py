from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlRelation, QSqlQuery
from utils import AbbrMaker, YearRangeList


class DocModel(QSqlRelationalTableModel):
    def __init__(self):
        super(DocModel, self).__init__()

        self.setTable("cfp_doc")
        self.setRelation(2, QSqlRelation(
            "cfp_doctype", "id", "name AS `cfp_doctype.name`"))
        self.setRelation(3, QSqlRelation(
            "cfp_fund", "id", "name AS `cfp_fund.name`"))

        self.setSort(0, Qt.AscendingOrder)

        self.__church_id__ = None
        self.__cache_years__ = {}
        self.__cache_flags__ = {}

    def data(self, item, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if item.column() == 9:
                return item.row() + 1

            elif item.column() == 10:
                rec = self.record(item.row())
                return rec.value("cfp_doctype.name")

            if item.column() == 11:
                return self.__years__(item.row())

            elif item.column() == 12:
                rec = self.record(item.row())

                storage_unit = "Ф.%s Оп.%s Д.%s " % (
                    rec.value("cfp_fund.name"),
                    rec.value("cfp_doc.inventory"),
                    rec.value("cfp_doc.unit"))

                return storage_unit

            if item.column() == 13:
                rec = self.record(item.row())
                return rec.value("cfp_doc.sheets")

            elif item.column() == 14:
                val = self.__flags__(item.row())
                return val

            if item.column() == 15:
                rec = self.record(item.row())
                return rec.value("cfp_doc.comment")

        return super().data(item, role)

    def select(self):
        if super().select():
            self.insertColumns(9, 7, QModelIndex())

            self.setHeaderData(9, Qt.Horizontal, "#")
            self.setHeaderData(10, Qt.Horizontal, "Вид документа")
            self.setHeaderData(11, Qt.Horizontal, "Годы документов")
            self.setHeaderData(12, Qt.Horizontal, "Шифр")
            self.setHeaderData(13, Qt.Horizontal, "Кол.-во листов")
            self.setHeaderData(14, Qt.Horizontal, "Примечание")
            self.setHeaderData(15, Qt.Horizontal, "Комментарий")

            self.__cache_years__.clear()
            self.__cache_flags__.clear()

            return True
        else:
            return False

    def __years__(self, row):
        # set years list to the local varible __cache_years__
        if self.__cache_years__.get(row) is None:
            y_list = self.docYears(row).split(",")

            self.__cache_years__[row] = YearRangeList().make(y_list)

        return self.__cache_years__[row]

    def __flags__(self, row):
        # set flag list to the local varible _cache_flags__
        if self.__cache_flags__.get(row) is None:
            val = self.docFlags(row)
            if isinstance(val, str):
                self.__cache_flags__[row] = AbbrMaker().make(val)
            else:
                self.__cache_flags__[row] = ""

        return self.__cache_flags__[row]

    def docYears(self, row):
        if row is None:
            return None

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

        return y_rec

    def docFlags(self, row):
        if row is None:
            return None

        doc_id = self.getItemId(row)

        query = "SELECT \
        (SELECT GROUP_CONCAT(cfp_docflag.name ORDER BY cfp_docflag.name SEPARATOR '/') \
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

        return y_rec

    def locality(self):
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
        WHERE cfp_church.id=%s" % self.churchId()

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

    def setChurch(self, church_id):
        self.__church_id__ = church_id

    def churchId(self):
        return self.__church_id__

    def clearCache(self, row):
        # clear cached years
        if self.__cache_years__.get(row) is not None:
            del self.__cache_years__[row]

        # clear cached flags
        if self.__cache_flags__.get(row) is not None:
            del self.__cache_flags__[row]

    def getItemId(self, row):
        if row is not None and row <= self.rowCount():
            return self.record(row).value("id")
        else:
            return None
