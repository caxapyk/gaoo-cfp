from PyQt5.Qt import Qt
from PyQt5.QtCore import QAbstractItemModel, QModelIndex
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery, QSqlField, QSqlRecord
from .docitem import DocItem


class DocModel(QAbstractItemModel):
    def __init__(self, church_id=None):
        super(DocModel, self).__init__()

        self.__church_id = church_id
        self.__items = []
        
        self.__db_col_list = []
        self.__columns = 0

        self.__cache = {}
        self.__doc_id = None

        self.__current_index = QModelIndex()

    def setCurrentIndex(self, index):
        self.__current_index = index


    def select(self):
        query = "SELECT \
        cfp_doc.id AS `cfp_doc.id`, \
        cfp_doc.doctype_id AS `cfp_doc.doctype_id`, \
        cfp_doc.fund AS `cfp_doc.fund`, \
        cfp_doc.inventory AS `cfp_doc.inventory`, \
        cfp_doc.unit AS `cfp_doc.unit`, \
        cfp_doc.sheets AS `cfp_doc.sheets`, \
        cfp_doc.comment AS `cfp_doc.comment`, \
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

        #self.__model.setQuery(sql_query)

        while sql_query.next():
            rec = sql_query.record()

            data = []
            cols = []
            #years = []
            #flags = []

            # fill data
            i = 0
            while i < rec.count():
                #data = {rec.field(i).name() : sql_query.record().value(i)}
                cols.append(rec.field(i).name())
                data.append(rec.value(i))
                #self.__db_col_list.append(rec.field(i).name())
                i += 1

            # fill years
            #for year in rec.value("years").split(","):
            #    years.append(year)
            # fill flags
            #for flag in rec.value("flags").split(","):
            #    flags.append(flag)

            #item = DocItem(data, years, flags)
            item = DocItem(cols, data)

            self.__items.append(item)
            self.__columns = i

        print(self.__db_col_list)

        return True

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def columnCount(self, parent=QModelIndex()):
        return self.__columns

    def rowCount(self, parent=QModelIndex()):
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

        item = index.internalPointer()

        #rec = self.__model.record(index.row())
        rec = self.record(index.row())
        field = rec.fieldName(index.column())

        #self.__cache[field] = value

        if index.row() < self.rowCount():
            self.__doc_id = rec.value("cfp_doc.id")

        item.setData(value, index.column())

        return True

    def submitAll(self):
        q_str = ""
        query = ""

        rec = self.record(self.__current_index.row())

        i = 0
        while i < rec.count():
            print(rec.field(i).name(), "=", rec.value(i))
            i += 1

        #for key, value in self.__cache.items():
        #    print(key, "=", value)

        #return None

        i = 0
        while i < rec.count() -2:
            if self.__doc_id is not None:
                q_str += "%s=?," % rec.field(i).name()
            else:
                q_str += "?,"
            i += 1

        #for key in self.__cache.keys():
        #    if self.__doc_id is not None:
        #        q_str += "%s=?," % key
        #    else:
        #        q_str += "?,"

        if self.__doc_id is None:
            query = "INSERT INTO cfp_doc \
            (church_id, doctype_id, fund, inventory, unit, sheets, comment) \
            VALUES(%s,%s)" % (self.__church_id, q_str[:-1])
        else:
            query = "UPDATE cfp_doc SET %s WHERE id=?" % q_str[:-1]

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        #for value in self.__cache.values():
        i= 0
        while i < rec.count() - 2:
            sql_query.addBindValue(rec.value(i))
            i += 1

        if self.__doc_id is not None:
            sql_query.addBindValue(self.__doc_id)

        print(sql_query.lastQuery())

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return False

        return True

    def insertColumns(self, column, count, parent):
        self.__model.insertColumns(column, count)
        for item in self.__items:
            i = 0
            while i < count:
                item.insertColumn(column)
                i += 1

        self.__columns += count

    def insertRows(self, row, count, parent):
        self.beginInsertRows(parent, row, row)

        i = 0
        data = []
        while i < self.record(row - 1).count() - 2:
            data.append(QSqlRecord())
            i += 1

        item = DocItem(0,data)
        self.__items.append(item)

        self.endInsertRows()

        return True

    def indexOf(self, field):
        #index = self.index(self.__current_index.row, 0, QModelIndex())

        return self.__current_index.internalPointer().indexOf(field)

