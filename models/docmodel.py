from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractItemModel, QModelIndex
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery, QSqlField
from .docitem import DocItem


class DocModel(QAbstractItemModel):
    def __init__(self, fk=None):
        super(DocModel, self).__init__()

        self.__fk = fk
        self.__items = []
        self.__m_model = QSqlQueryModel()

    def select(self):
        # query = "SELECT cfp_doctype.id, cfp_doctype.name, cfp_doc.id, cfp_doc.fund, cfp_doc.inventory, cfp_doc.unit, cfp_doc.sheets, cfp_doc.comment, \
        #CONCAT('Ф.', cfp_doc.fund,  ', Оп.', cfp_doc.inventory, ', Д.', cfp_doc.unit) AS storageUnit, \
        #(SELECT GROUP_CONCAT(year) FROM cfp_docyears WHERE cfp_docyears.doc_id = cfp_doc.id) AS years, \
        #(SELECT GROUP_CONCAT(cfp_docflag.name) FROM cfp_docflags LEFT JOIN cfp_docflag ON cfp_docflags.docflag_id=cfp_docflag.id WHERE cfp_docflags.doc_id = cfp_doc.id) AS flags, \
        #(SELECT GROUP_CONCAT(cfp_docflag.id) FROM cfp_docflags LEFT JOIN cfp_docflag ON cfp_docflags.docflag_id=cfp_docflag.id WHERE cfp_docflags.doc_id = cfp_doc.id) AS flag_ids \
        #FROM cfp_doc \
        #LEFT JOIN cfp_doctype ON cfp_doc.doctype_id=cfp_doctype.id"
        # self.setupModelData()

        query = "SELECT cfp_doc.id, cfp_doctype.name, cfp_doc.fund, cfp_doc.inventory, cfp_doc.unit, cfp_doc.sheets, cfp_doc.comment, \
        (SELECT GROUP_CONCAT(year) FROM cfp_docyears WHERE cfp_docyears.doc_id = cfp_doc.id) AS years, \
        (SELECT GROUP_CONCAT(cfp_docflag.name) FROM cfp_docflags LEFT JOIN cfp_docflag ON cfp_docflags.docflag_id=cfp_docflag.id WHERE cfp_docflags.doc_id = cfp_doc.id) AS flags \
        FROM cfp_doc \
        LEFT JOIN cfp_doctype ON cfp_doc.doctype_id=cfp_doctype.id"

        if self.__fk:
            query += " WHERE cfp_doc.church_id = ?"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if self.__fk:
            sql_query.addBindValue(self.__fk)

        if sql_query.exec_():
            self.__m_model.setQuery(sql_query)
        print(sql_query.lastError().text())

        while sql_query.next():
            data = []
            years = []
            flags = []

            # fill data
            i = 0
            while i < sql_query.record().count():
                data.append(sql_query.record().value(i))
                i += 1
            # fill years
            for year in sql_query.record().value("years").split(","):
                years.append(year)
            # fill flags
            for flag in sql_query.record().value("flags").split(","):
                flags.append(flag)

            item = DocItem(data, years, flags)

            self.__items.append(item)

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def columnCount(self, parent):
        rec = self.__m_model.record()
        if rec.isEmpty():
            return 0

        return rec.count()

    def rowCount(self, parent):
        if not parent.isValid():
            return len(self.__items)
        else:
            return 0

    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
           return QModelIndex()

        item = self.__items[row]
        index = self.createIndex(row, column, item)

        return index

    def parent(self, index):
        return QModelIndex()

    def data(self, index, role):
        if not index.isValid():
            return None

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        item = index.internalPointer()

        return item.data(index.column())

    def setData(self, index, value, role):
        if role != Qt.EditRole:
            return None

        print(value)

        item = index.internalPointer()
        item.setData(value, index.column())
        # if item.model().update(item.uid(), value):
        #    item.setData((value,))

        return True

        return False

    def insertColumn(self, column, parent):
        self.__m_model.insertColumn(column, parent)

        for item in self.__items:
            item.insertColumn(column)

    def record(self, row):
        return self.__m_model.record(row)
