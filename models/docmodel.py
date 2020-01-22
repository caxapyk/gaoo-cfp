from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery
from models import YearModel


class DocModel(QSqlQueryModel):
    def __init__(self):
        super(DocModel, self).__init__()

        self.church_id = None

        self.year_model = YearModel()

    def flags(self, index):
        return Qt.ItemIsSelectable | Qt.ItemIsEnabled

    def data(self, item, role):
        if role == Qt.DisplayRole:
            if item.column() == 0:
                return item.row() + 1

            elif item.column() == 4:
                rec = self.query().record()

                storage_unit = "Ф. %s Оп. %s Д. %s" % (
                    rec.value("cfp_doc.fund"),
                    rec.value("cfp_doc.inventory"),
                    rec.value("cfp_doc.unit"))

                return storage_unit

            elif item.column() == 9:
                rec = self.query().record()
                self.year_model.setFilter(
                    "doc_id=\"%s\"" % rec.value("cfp_doc.id"))

                self.year_model.select()

                years_list = ""
                query = self.year_model.query()
                while query.next():
                    years_list += "%s/" % str(query.value("year"))

                return years_list[:-1]

            # elif item.column() == 2:
            #    abbr = ""
            #    doctype = self.query().record().value("cfp_doctype.name")

            #    for i, w in enumerate(doctype.upper().split()):
            #       if i > 2:
            #            break
            #        abbr += w[0]

            #    return abbr

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
        cfp_doc.sheets \
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
            # insert columns for counter and storage_unit fields
            self.insertColumns(0, 1, QModelIndex())
            self.insertColumns(4, 1, QModelIndex())
            # insert columns for years fields
            self.insertColumns(9, 1, QModelIndex())

            self.setHeaderData(0, Qt.Horizontal, "№ п/п")
            self.setHeaderData(1, Qt.Horizontal, "ID")
            self.setHeaderData(2, Qt.Horizontal, "Тип документа")
            self.setHeaderData(3, Qt.Horizontal, "ID")
            self.setHeaderData(4, Qt.Horizontal, "Ед. хранения")
            self.setHeaderData(5, Qt.Horizontal, "Фонд")
            self.setHeaderData(6, Qt.Horizontal, "Опись")
            self.setHeaderData(7, Qt.Horizontal, "Дело")
            self.setHeaderData(8, Qt.Horizontal, "Листов")
            self.setHeaderData(9, Qt.Horizontal, "Годы документов")
        else:
            self.printError(sql_query)

    def printError(self, sql_query):
        print("%s: %s" %
              (self.__class__.__name__, sql_query.lastError().text()))
