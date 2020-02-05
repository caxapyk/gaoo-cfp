from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlRelation, QSqlQuery
from models import DoctypeModel
from utils import AbbrMaker


class DocModel(QSqlRelationalTableModel):
    def __init__(self):
        super(DocModel, self).__init__()

        self.setTable("cfp_doc")
        self.setRelation(2, QSqlRelation(
            "cfp_doctype", "id", "name AS `cfp_doctype.name`"))

        self.__church_id__ = None

    def setChurch(self, id):
        self.__church_id__ = id

    def churchId(self):
        return self.__church_id__

    def data(self, item, role):
        # if role == Qt.DisplayRole:
            # if item.column() == 0:
            #    return item.row() + 1

            # elif item.column() == 1:
            #    rec = self.record(item.row())
            #    doctype_abbr = AbbrMaker().make(
            #        rec.value("name"))

            #    return doctype_abbr

            # elif item.column() == 5:
            #    rec = self.record(item.row())

            #    storage_unit = "Ф. %s Оп. %s Д. %s" % (
            #        rec.value("cfp_doc.fund"),
            #        rec.value("cfp_doc.inventory"),
            #        rec.value("cfp_doc.unit"))

            #    return storage_unit

            # elif item.column() == 10:
            #    year_rel = self.yearsModel(item.row())

            #    years_list = ""
            #    if year_rel:
            #        while year_rel.query().next():
            #            years_list += "%s, " % str(
            #                year_rel.query().value("year"))

            #        return years_list[:-2]

            # elif item.column() == 11:
            #    rec = self.record(item.row())
            #    flag_rel = self.flagRelation(rec.value("cfp_doc.id"))

            #    flags_list = ""
            #    if flag_rel:
            #        while flag_rel.next():
            #            flags_list += "%s/" % AbbrString().make(
            #                flag_rel.value("name"))

            #        return flags_list[:-1]

        return super().data(item, role)

    def yearsList(self, row):
        if row is None:
            return None

        doc_id = self.getItemId(row)

        query = "SELECT \
        (SELECT GROUP_CONCAT(cfp_docyears.year ORDER BY cfp_docyears.year) \
        FROM cfp_docyears WHERE cfp_docyears.doc_id=%s) AS years\
        FROM cfp_docyears WHERE cfp_docyears.doc_id=%s" % (doc_id, doc_id)

        print(query)

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return None

        sql_query.last()
        y_rec = sql_query.record().value("years")

        print(y_rec)

        return y_rec

    def flagsList(self, row):
        if row is None:
            return None

        doc_id = self.getItemId(row)

        query = "SELECT \
        (SELECT GROUP_CONCAT(cfp_docflag.name ORDER BY cfp_docflag.name) FROM cfp_docflags LEFT JOIN cfp_docflag ON cfp_docflags.docflag_id=cfp_docflag.id WHERE cfp_docflags.doc_id=%s) AS flags \
        FROM cfp_docflags WHERE cfp_docflags.doc_id=%s" % (doc_id, doc_id)

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return None

        sql_query.last()
        y_rec = sql_query.record().value("flags")

        print(y_rec)

        return y_rec

    def select(self):
        if super().select():
            # insert columns for counter and type abbr fields
            #self.insertColumns(0, 2, QModelIndex())
            # insert column for storage_unit field
            #self.insertColumns(5, 1, QModelIndex())
            # insert column for years and flags fields
            #self.insertColumns(10, 2, QModelIndex())

            # self.setHeaderData(0, Qt.Horizontal, "#")
            #self.setHeaderData(1, Qt.Horizontal, "Тип документа")
            #self.setHeaderData(2, Qt.Horizontal, "ID")
            #self.setHeaderData(3, Qt.Horizontal, "Название церкви")
            #self.setHeaderData(4, Qt.Horizontal, "Тип документа (полностью)")
            #self.setHeaderData(5, Qt.Horizontal, "Ед. хранения")
            #self.setHeaderData(6, Qt.Horizontal, "Фонд")
            #self.setHeaderData(7, Qt.Horizontal, "Опись")
            #self.setHeaderData(8, Qt.Horizontal, "Дело")
            #self.setHeaderData(9, Qt.Horizontal, "Листов")
            #self.setHeaderData(10, Qt.Horizontal, "Годы документов")
            #self.setHeaderData(11, Qt.Horizontal, "Другие сведения")
            #self.setHeaderData(12, Qt.Horizontal, "Комментарий")

            return True
        else:
            return False

    def getItemId(self, row):
        if row <= self.rowCount():
            return self.record(row).value("id")
        else:
            return None
