from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractItemModel, QModelIndex
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery, QSqlField
from .docitem import DocItem


class DocModel(QAbstractItemModel):
    def __init__(self, church_id=None):
        super(DocModel, self).__init__()

        self.__church_id = church_id
        self.__items = []

        self.__columns = 0

    def select(self):
        query = "SELECT \
        cfp_doc.id, \
        cfp_doctype.name, \
        cfp_doc.fund, \
        cfp_doc.inventory, \
        cfp_doc.unit, \
        cfp_doc.sheets, \
        cfp_doc.comment, \
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

        while sql_query.next():
            rec = sql_query.record()

            data = []
            years = []
            flags = []

            # fill data
            i = 0
            while i < rec.count() - 2:
                data.append(sql_query.record().value(i))
                i += 1

            # fill years
            for year in rec.value("years").split(","):
                years.append(year)
            # fill flags
            for flag in rec.value("flags").split(","):
                flags.append(flag)

            item = DocItem(data, years, flags)

            self.__items.append(item)
            self.__columns = i

        return True

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def columnCount(self, parent):
        return self.__columns

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

        if role == Qt.DisplayRole or role == Qt.EditRole:
            item = index.internalPointer()

            return item.data(index.column())

        return None

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

    def insertColumns(self, column, count, parent):
        for item in self.__items:
            i = 0
            while i < count:
                item.insertColumn(column)
                i += 1

        self.__columns += count
