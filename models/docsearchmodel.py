from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex, QAbstractItemModel
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery, QSqlRecord, QSqlField
from utils import AbbrMaker


class DocSearchModel(QSqlQueryModel):
    def __init__(self):
        super(DocSearchModel, self).__init__()

        self.__filter_str__ = ""

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:

            if index.column() == 0:
                return index.row() + 1

            elif index.column() == 11:
                rec = self.record(index.row())

                storage_unit = "Ф. %s Оп. %s Д. %s" % (
                    rec.value("cfp_doc.fund"),
                    rec.value("cfp_doc.inventory"),
                    rec.value("cfp_doc.unit"))

                return storage_unit

        return super().data(index, role)

    def refresh(self):
        query = "SELECT \
        cfp_doc.id AS `cfp_doc.id`, \
        cfp_gubernia.name AS `cfp_gubernia.name`, \
        cfp_uezd.name AS `cfp_uezd.name`, \
        cfp_locality.name AS `cfp_locality.name`, \
        cfp_church.name AS `cfp_church.name`, \
        cfp_doctype.name AS `cfp_doctype.name`, \
        (SELECT GROUP_CONCAT(cfp_docyears.year ORDER BY cfp_docyears.year SEPARATOR '/') FROM cfp_docyears WHERE cfp_docyears.doc_id = cfp_doc.id) AS years, \
        cfp_doc.fund AS `cfp_doc.fund`, \
        cfp_doc.inventory AS `cfp_doc.inventory`, \
        cfp_doc.unit AS `cfp_doc.unit`, \
        cfp_doc.sheets AS `cfp_doc.sheets`, \
        (SELECT GROUP_CONCAT(cfp_docflag.name ORDER BY cfp_docflag.name SEPARATOR '/') FROM cfp_docflags LEFT JOIN cfp_docflag ON cfp_docflags.docflag_id=cfp_docflag.id WHERE cfp_docflags.doc_id = cfp_doc.id) AS flags, \
        cfp_doc.comment AS `cfp_doc.comment` \
        FROM cfp_doc \
        LEFT JOIN cfp_church ON cfp_doc.church_id = cfp_church.id \
        LEFT JOIN cfp_locality ON cfp_church.locality_id = cfp_locality.id \
        LEFT JOIN cfp_uezd ON cfp_locality.uezd_id = cfp_uezd.id \
        LEFT JOIN cfp_gubernia ON cfp_uezd.gub_id = cfp_gubernia.id \
        LEFT JOIN cfp_doctype ON cfp_doc.doctype_id=cfp_doctype.id"

        if len(self.filter()) > 0:
            query += " WHERE " + self.filter()

        query += " LIMIT 500"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return None

        self.setQuery(sql_query)

        # insert columns for counter field
        self.insertColumns(0, 1)
        # insert columns for storage unit field
        self.insertColumns(11, 1)

        self.setHeaderData(0, Qt.Horizontal, "#")  # inserted
        self.setHeaderData(1, Qt.Horizontal, "Идентификатор документа")
        self.setHeaderData(2, Qt.Horizontal, "Губерния")
        self.setHeaderData(3, Qt.Horizontal, "Уезд")
        self.setHeaderData(4, Qt.Horizontal, "Населенный пункт")
        self.setHeaderData(5, Qt.Horizontal, "Наименование церкви")
        self.setHeaderData(6, Qt.Horizontal, "Тип документа")
        self.setHeaderData(7, Qt.Horizontal, "Годы документов")
        self.setHeaderData(8, Qt.Horizontal, "Фонд")
        self.setHeaderData(9, Qt.Horizontal, "Опись")
        self.setHeaderData(10, Qt.Horizontal, "Дело")
        self.setHeaderData(11, Qt.Horizontal, "Шифр (основание)")  # inserted
        self.setHeaderData(12, Qt.Horizontal, "Кол.-во листов")
        self.setHeaderData(13, Qt.Horizontal, "Примечание")
        self.setHeaderData(14, Qt.Horizontal, "Комментарий")

    def andFilterWhere(self, op, field, value, value2=""):
        a_filter = ""
        if op == "=":
            if len(value) > 0:
                a_filter += "%s=\"%s\"" % (field, value)
        elif op == "LIKE":
            if len(value) > 0:
                a_filter += "%s LIKE \"%%%s%%\"" % (field, value)
        elif op == "BETWEEN":
            if len(value) > 0 or len(value2) > 0:
                if field == "cfp_docyears.year":
                    if len(value) > 0 and len(value2) > 0:
                        cond = "BETWEEN %s AND %s" % (value, value2)
                    elif len(value) > 0 and len(value2) == 0:
                        cond = ">= %s" % value
                    elif len(value) == 0 and len(value2) > 0:
                        cond = "<= %s" % value2
                    a_filter += "EXISTS \
                    (SELECT cfp_docyears.year \
                    FROM cfp_docyears \
                    WHERE cfp_doc.id = cfp_docyears.doc_id \
                    AND cfp_docyears.year %s)" % cond
        elif op == "EXISTS":
            if field == "cfp_docflag.id":
                if len(value) > 0:
                    if value2 == "STRICT":
                        a_filter += "EXISTS \
                        (SELECT GROUP_CONCAT(cfp_docflag.id ORDER BY cfp_docflag.id) AS flags \
                        FROM cfp_docflag LEFT JOIN cfp_docflags \
                        ON cfp_docflag.id = cfp_docflags.docflag_id \
                        WHERE cfp_doc.id = cfp_docflags.doc_id \
                        GROUP BY cfp_doc.id \
                        HAVING flags = '%s')" % value
                    elif value2 == "NONSTRICT":
                        v_count = len(value.split(","))
                        a_filter += "EXISTS \
                        (SELECT cfp_docflag.id FROM cfp_docflag \
                        LEFT JOIN cfp_docflags \
                        ON cfp_docflag.id = cfp_docflags.docflag_id \
                        WHERE cfp_doc.id = cfp_docflags.doc_id \
                        AND cfp_docflags.docflag_id IN (%s) \
                        GROUP BY cfp_doc.id \
                        HAVING \
                        (SELECT COUNT(*) FROM cfp_docflags \
                        WHERE cfp_docflags.doc_id=cfp_doc.id \
                        AND cfp_docflags.docflag_id IN (%s)\
                        ) >= %s)" % (value, value, v_count)
                elif len(value) == 0 and value2 == "STRICT":
                    a_filter += "(SELECT \
                    GROUP_CONCAT(cfp_docflag.id ORDER BY cfp_docflag.id) AS flags \
                    FROM cfp_docflag \
                    LEFT JOIN cfp_docflags ON cfp_docflag.id = cfp_docflags.docflag_id \
                    WHERE cfp_doc.id = cfp_docflags.doc_id) IS NULL"

        if len(a_filter) > 0 and len(self.filter()) > 0:
            a_filter = " AND " + a_filter

        self.appendFilter(a_filter)

    def filter(self):
        return self.__filter_str__

    def appendFilter(self, filter_str):
        self.__filter_str__ += filter_str