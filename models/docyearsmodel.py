from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex, QAbstractListModel
from PyQt5.QtSql import QSqlQuery


class DocYearsModel(QAbstractListModel):
    def __init__(self, year_list):
        super(DocYearsModel, self).__init__()

        if year_list is not None and len(year_list) > 0:
            years = year_list.split(",")
        else:
            years = []

        self.__data = years

        self.doc_id = None
        self.current_changed = False

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsEditable

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self.__data)
        else:
            return 0

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.DisplayRole or role == Qt.EditRole:
            if index.row() > len(self.__data):
                return None

            item = self.__data[index.row()]

            return item

        return None

    def setData(self, index, value, role=Qt.EditRole):
        if role != Qt.EditRole:
            return None

        if len(value) == 4:
            # remove row if current list contains value
            if value in self.__data:
                self.removeRows(index.row(), 1)
            else:
                self.__data[index.row()] = value
                self.__data.sort()

            self.current_changed = True
            self.dataChanged.emit(index, index)
            return True

        return False

    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row)

        self.__data.append("")

        self.endInsertRows()

        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row)

        i = 0
        while i < count:
            del self.__data[row]
            i += 1

        self.current_changed = True

        self.endRemoveRows()

        return True

    def submitAll(self):
        if not self.current_changed:
            return True

        sql_query = QSqlQuery()

        query = "DELETE FROM cfp_docyears \
        WHERE doc_id=%s" % self.doc_id

        sql_query.prepare(query)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return False

        if len(self.__data) > 0:
            years = []
            # use set() to make unique
            for y in set(self.__data):
                row = "(%s, %s)" % (self.doc_id, y)
                years.append(row)

            query = "INSERT INTO cfp_docyears \
                (doc_id, year) VALUES %s" % ",".join(years)

            sql_query.prepare(query)

            if not sql_query.exec_():
                print(sql_query.lastError().text())
                return False

        return True

    def setDoc(self, doc_id):
        self.doc_id = doc_id
