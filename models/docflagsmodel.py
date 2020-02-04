from PyQt5.Qt import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.QtCore import QModelIndex, QAbstractListModel
from models import DocflagModel


class DocFlagsModel(DocflagModel):
    def __init__(self, doc_id, flag_list=""):
        super(DocFlagsModel, self).__init__()

        if len(flag_list) > 0:
            flags = flag_list.split(",")
        else:
            flags = []

        super().select()

        self.__data = flags
        self.__ids = []

        while self.query().next():
            if self.query().value("name") in self.__data:
                self.__ids.append(self.query().value("id"))

        self.doc_id = doc_id

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsUserCheckable

    def data_(self):
        return ",".join(self.__data)

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.CheckStateRole:
            if super().data(index) in self.__data:
                return Qt.Checked

            return Qt.Unchecked


        return super().data(index, role)

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole:
            # index for DocflagModel column `id`
            id_index = super().index(index.row(), 0)

            if(value == Qt.Checked):
                self.__data.append(super().data(index))
                self.__ids.append(super().data(id_index))
            else:
                del self.__ids[self.__ids.index(super().data(id_index))]
                del self.__data[self.__data.index(super().data(index))]

        return True

    def submit(self):
        sql_query = QSqlQuery()

        query = "DELETE FROM cfp_docflags \
        WHERE doc_id=%s" % self.doc_id

        sql_query.prepare(query)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return False

        print(self.__ids)

        if len(self.__ids) > 0:
            flags = []
            for f_id in self.__ids:
                row = "(%s, %s)" % (self.doc_id, f_id)
                flags.append(row)

            query = "INSERT INTO cfp_docflags \
                (doc_id, docflag_id) VALUES %s" % ",".join(flags)

            sql_query.prepare(query)
            print(sql_query.lastQuery())

            if not sql_query.exec_():
                print(sql_query.lastError().text())
                return False

        return True
