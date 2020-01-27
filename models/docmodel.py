from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlRelation
from models import DoctypeModel, DocflagModel, YearsModel
from utils import AbbrString


class DocModel(QSqlRelationalTableModel):
    def __init__(self):
        super(DocModel, self).__init__()

        self.setTable("cfp_doc")
        self.setRelation(1, QSqlRelation("cfp_church", "id", "name"))
        self.setRelation(2, QSqlRelation("cfp_doctype", "id", "name"))

        self.church_id = None

    def data(self, item, role):
        if role == Qt.DisplayRole:
            if item.column() == 0:
                return item.row() + 1

            elif item.column() == 1:
                rec = self.record(item.row())
                doctype_abbr = AbbrString().make(
                    rec.value("name"))

                return doctype_abbr

            elif item.column() == 5:
                rec = self.record(item.row())

                storage_unit = "Ф. %s Оп. %s Д. %s" % (
                    rec.value("cfp_doc.fund"),
                    rec.value("cfp_doc.inventory"),
                    rec.value("cfp_doc.unit"))

                return storage_unit

            elif item.column() == 10:
                year_rel = self.yearsModel(item.row())

                years_list = ""
                if year_rel:
                    while year_rel.query().next():
                        years_list += "%s, " % str(
                            year_rel.query().value("year"))

                    return years_list[:-2]

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

    def yearsModel(self, row):
        rec = self.record(row)
        years_model = YearsModel()

        years_model.setFilter("doc_id=%s" % rec.value("id"))
        years_model.select()

        return years_model

    def select(self):
        super().select()
        # insert columns for counter and type abbr fields
        self.insertColumns(0, 2, QModelIndex())
        # insert column for storage_unit field
        self.insertColumns(5, 1, QModelIndex())
        # insert column for years and flags fields
        self.insertColumns(10, 2, QModelIndex())

        self.setHeaderData(0, Qt.Horizontal, "#")
        self.setHeaderData(1, Qt.Horizontal, "Тип документа")
        self.setHeaderData(2, Qt.Horizontal, "ID")
        self.setHeaderData(3, Qt.Horizontal, "Название церкви")
        self.setHeaderData(4, Qt.Horizontal, "Тип документа (полностью)")
        self.setHeaderData(5, Qt.Horizontal, "Ед. хранения")
        self.setHeaderData(6, Qt.Horizontal, "Фонд")
        self.setHeaderData(7, Qt.Horizontal, "Опись")
        self.setHeaderData(8, Qt.Horizontal, "Дело")
        self.setHeaderData(9, Qt.Horizontal, "Листов")
        self.setHeaderData(10, Qt.Horizontal, "Годы документов")
        self.setHeaderData(11, Qt.Horizontal, "Другие сведения")
        self.setHeaderData(12, Qt.Horizontal, "Комментарий")
