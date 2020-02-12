from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex, QAbstractItemModel
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery, QSqlRecord, QSqlField
from utils import AbbrMaker


class DocSearchModel(QSqlQueryModel):
    def __init__(self):
        super(DocSearchModel, self).__init__()

        self.__filter_str__ = None

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole:

            if index.column() == 11:
                return index.row() + 1

            elif index.column() == 12:
                rec = self.record(index.row())
                doctype_abbr = AbbrMaker().make(
                    rec.value("cfp_doctype.name"))

                return doctype_abbr

            elif index.column() == 13:
                rec = self.record(index.row())

                storage_unit = "Ф. %s Оп. %s Д. %s" % (
                    rec.value("cfp_doc.fund"),
                    rec.value("cfp_doc.inventory"),
                    rec.value("cfp_doc.unit"))

                return storage_unit

            elif index.column() == 16:
                rec = self.record(index.row())

                flags_list = ""
                for flag in rec.value("flags").split(","):
                    flags_list += "%s/" % AbbrMaker().make(flag)

                return flags_list[:-1]

        return super().data(index, role)

    def refresh(self):
        query = "SELECT \
        cfp_doc.id AS `cfp_doc.id`, \
        cfp_gubernia.name AS `cfp_gubernia.name`, \
        cfp_uezd.name AS `cfp_uezd.name`, \
        cfp_locality.name AS `cfp_locality.name`, \
        cfp_church.name AS `cfp_church.name`, \
        cfp_doc.church_id AS `cfp_doc.church_id`, \
        cfp_doctype.name AS `cfp_doctype.name`, \
        cfp_doc.doctype_id AS `cfp_doc.doctype_id`, \
        cfp_doc.fund AS `cfp_doc.fund`, \
        cfp_doc.inventory AS `cfp_doc.inventory`, \
        cfp_doc.unit AS `cfp_doc.unit`, \
        cfp_doc.sheets AS `cfp_doc.sheets`, \
        (SELECT GROUP_CONCAT(cfp_docyears.year ORDER BY cfp_docyears.year) FROM cfp_docyears WHERE cfp_docyears.doc_id = cfp_doc.id) AS years, \
        (SELECT GROUP_CONCAT(cfp_docflag.name ORDER BY cfp_docflag.name) FROM cfp_docflags LEFT JOIN cfp_docflag ON cfp_docflags.docflag_id=cfp_docflag.id WHERE cfp_docflags.doc_id = cfp_doc.id) AS flags, \
        cfp_doc.comment AS `cfp_doc.comment` \
        FROM cfp_doc \
        LEFT JOIN cfp_church ON cfp_doc.church_id = cfp_church.id \
        LEFT JOIN cfp_locality ON cfp_church.locality_id = cfp_locality.id \
        LEFT JOIN cfp_uezd ON cfp_locality.uezd_id = cfp_uezd.id \
        LEFT JOIN cfp_gubernia ON cfp_uezd.gub_id = cfp_gubernia.id \
        LEFT JOIN cfp_doctype ON cfp_doc.doctype_id=cfp_doctype.id"

        if self.filter():
            query += " WHERE " + self.filter()

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return None

        self.setQuery(sql_query)

        # insert columns for counter/type abbr/storage unit fields
        self.insertColumns(11, 3)
        # insert column for flags abbr
        self.insertColumns(16, 1)

        self.setHeaderData(0, Qt.Horizontal, "Идентификатор документа")
        self.setHeaderData(1, Qt.Horizontal, "Губерния")
        self.setHeaderData(2, Qt.Horizontal, "Уезд")
        self.setHeaderData(3, Qt.Horizontal, "Населенный пункт")
        self.setHeaderData(4, Qt.Horizontal, "Наименование церкви")
        self.setHeaderData(5, Qt.Horizontal, "Идентификатор церкви")
        self.setHeaderData(6, Qt.Horizontal, "Тип документа")
        self.setHeaderData(7, Qt.Horizontal, "Идентификатор типа документа")
        self.setHeaderData(8, Qt.Horizontal, "Фонд")
        self.setHeaderData(9, Qt.Horizontal, "Опись")
        self.setHeaderData(10, Qt.Horizontal, "Дело")
        self.setHeaderData(11, Qt.Horizontal, "#")  # inserted
        self.setHeaderData(12, Qt.Horizontal, "Тип документа")  # inserted
        self.setHeaderData(13, Qt.Horizontal, "Ед. хранения")  # inserted
        self.setHeaderData(14, Qt.Horizontal, "Листов")
        self.setHeaderData(15, Qt.Horizontal, "Годы документов")
        self.setHeaderData(16, Qt.Horizontal, "Флаги")  # inserted
        self.setHeaderData(17, Qt.Horizontal, "Флаги")
        self.setHeaderData(18, Qt.Horizontal, "Комментарий")

    def setFilter(self, f_str):
        self.__filter_str__ = f_str

    def filter(self):
        return self.__filter_str__
