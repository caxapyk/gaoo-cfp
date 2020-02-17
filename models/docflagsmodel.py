from PyQt5.Qt import Qt
from PyQt5.QtSql import QSqlQuery
from models import DocflagModel


class DocFlagsModel(DocflagModel):
    def __init__(self, flag_list):
        super(DocFlagsModel, self).__init__()

        if flag_list is not None and len(flag_list) > 0:
            flags = flag_list.split(",")
        else:
            flags = []

        super().select()

        self.__data = {}
        self.__readOnly__ = False

        while self.query().next():
            v_id = self.query().value("id")
            v_name = self.query().value("name")

            if v_name in flags:
                self.__data[v_id] = v_name

        self.doc_id = None
        self.current_changed = False

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsUserCheckable

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.CheckStateRole:
            if super().data(index) in self.__data.values():
                return Qt.Checked

            return Qt.Unchecked

        return super().data(index, role)

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole and not self.__readOnly__:
            v_name = super().record(index.row()).value("name")
            v_id = super().record(index.row()).value("id")

            if(value == Qt.Checked):
                self.__data[v_id] = v_name
            else:
                del self.__data[v_id]

            self.current_changed = True
            self.dataChanged.emit(index, index)

        return True

    def submitAll(self):
        if not self.current_changed:
            return True

        sql_query = QSqlQuery()

        query = "DELETE FROM cfp_docflags \
        WHERE doc_id=%s" % self.doc_id

        sql_query.prepare(query)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return False

        if len(self.__data) > 0:
            flags = []
            for f_id in self.__data.keys():
                row = "(%s, %s)" % (self.doc_id, f_id)
                flags.append(row)

            query = "INSERT INTO cfp_docflags \
                (doc_id, docflag_id) VALUES %s" % ",".join(flags)

            print(query)

            sql_query.prepare(query)

            if not sql_query.exec_():
                print(sql_query.lastError().text())
                return False

        return True

    def setDoc(self, doc_id):
        self.doc_id = doc_id

    def setReadOnly(self, value):
        self.__readOnly__ = value
