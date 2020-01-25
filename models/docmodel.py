from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from utils import AbbrString


class DocModel(QSqlQueryModel):
    def __init__(self):
        super(DocModel, self).__init__()

        self.church_id = None

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            data = "#"
            if section == 1:
                data = "Тип документа"
            elif section == 2:
                data = "ID"
            elif section == 3:
                data = "Тип документа"
            elif section == 4:
                data = "ID (тип документа)"
            elif section == 5:
                data = "Ед. хранения"
            elif section == 6:
                data = "Фонд"
            elif section == 7:
                data = "Опись"
            elif section == 8:
                data = "Дело"
            elif section == 9:
                data = "Листов"
            elif section == 10:
                data = "Годы документов"
            elif section == 11:
                data = "Другие сведения"
            elif section == 12:
                data = "Комментарий"

            return data
        return super().headerData(section, orientation, role)

    def data(self, item, role):
        if role == Qt.DisplayRole:
            if item.column() == 0:
                return item.row() + 1

            elif item.column() == 1:
                rec = self.record(item.row())
                doctype_abbr = AbbrString().make(
                    rec.value("cfp_doctype.name"))

                return doctype_abbr

            elif item.column() == 5:
                rec = self.record(item.row())

                storage_unit = "Ф. %s Оп. %s Д. %s" % (
                    rec.value("cfp_doc.fund"),
                    rec.value("cfp_doc.inventory"),
                    rec.value("cfp_doc.unit"))

                return storage_unit

            #elif item.column() == 10:
            #    rec = self.record(item.row())
            #    year_rel = self.yearRelation(rec.value("cfp_doc.id"))

            #    years_list = ""
            #    if year_rel:
            #        while year_rel.next():
            #            years_list += "%s, " % str(year_rel.value("year"))

            #        return years_list[:-2]

            #elif item.column() == 11:
            #    rec = self.record(item.row())
            #    flag_rel = self.flagRelation(rec.value("cfp_doc.id"))

            #    flags_list = ""
            #    if flag_rel:
            #        while flag_rel.next():
            #            flags_list += "%s/" % AbbrString().make(
            #                flag_rel.value("name"))

            #        return flags_list[:-1]

        return super().data(item, role)

    def setChurchId(self, church_id):
        self.church_id = church_id

    def select(self):
        query = "SELECT \
        cfp_doctype.id, \
        cfp_doctype.name, \
        cfp_doc.id, \
        cfp_doc.fund, \
        cfp_doc.inventory, \
        cfp_doc.unit, \
        cfp_doc.sheets, \
        cfp_doc.comment \
        FROM cfp_doc \
        LEFT JOIN cfp_doctype \
        ON cfp_doc.doctype_id=cfp_doctype.id"

        if self.church_id:
            query += " WHERE cfp_doc.church_id = ?"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.church_id:
            sql_query.addBindValue(self.church_id)

        if sql_query.exec_():
            self.setQuery(sql_query)
            # insert columns for counter and type abbr fields
            self.insertColumns(0, 2, QModelIndex())
            # insert column for storage_unit field
            self.insertColumns(5, 1, QModelIndex())
            # insert column for years and flags fields
            self.insertColumns(10, 2, QModelIndex())
        else:
            self.printError(sql_query)

    def yearRelation(self, doc_id):
        y_model = QSqlQueryModel()
        query = "SELECT cfp_docYears.year \
        FROM cfp_doc \
        RIGHT JOIN cfp_docYears \
        ON cfp_docYears.doc_id=cfp_doc.id \
        WHERE cfp_doc.id=?"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        sql_query.addBindValue(doc_id)

        if sql_query.exec_():
            y_model.setQuery(sql_query)
            return y_model
        else:
            self.printError(sql_query)

    def flagRelation(self, doc_id):
        f_model = QSqlQueryModel()
        query = "SELECT cfp_docflag.name \
        FROM cfp_doc \
        RIGHT JOIN cfp_docFlags \
        ON cfp_docFlags.doc_id=cfp_doc.id \
        LEFT JOIN cfp_docflag \
        ON cfp_docFlags.docflag_id=cfp_docflag.id \
        WHERE cfp_doc.id=?"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        sql_query.addBindValue(doc_id)

        if sql_query.exec_():
            f_model.setQuery(sql_query)
            return f_model
        else:
            self.printError(sql_query)

    def printError(self, sql_query):
        print("%s: %s" %
              (self.__class__.__name__, sql_query.lastError().text()))
