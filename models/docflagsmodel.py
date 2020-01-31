from PyQt5.Qt import Qt
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QModelIndex


class DocFlagsModel(QSqlTableModel):
    def __init__(self, doc_id):
        super(DocFlagsModel, self).__init__()

        self.setTable("cfp_docflag")

        self.__model = QSqlTableModel()
        self.__model.setTable("cfp_docflags")
        self.__model.setFilter("doc_id=%s" % doc_id)
        self.__model.select()

        self.__flags = {}
        self.doc_id = doc_id

        row = 0
        while self.__model.query().next():
        	# id:row dict
            self.__flags[self.__model.query().value("docflag_id")] = row
            row += 1

        print(self.__flags)

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsUserCheckable

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.CheckStateRole:
            # index for DocflagModel column `id`
            id_index = self.createIndex(index.row(), 0, QModelIndex())
            if super().data(id_index) in self.__flags.keys():
                return Qt.Checked

            return Qt.Unchecked

        return super().data(index, role)

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole:
            # index for DocflagModel column `id`
            id_index = self.__model.createIndex(index.row(), 0, QModelIndex())

            if(value == Qt.Checked):
                record = self.__model.record()
                record.remove(record.indexOf("id"))
                record.setValue("doc_id", self.doc_id)
                record.setValue("docflag_id", self.data(id_index))

                if self.__model.insertRecord(-1, record):
                    self.__flags[self.data(id_index)] = self.__model.rowCount() - 1
            else:
                if self.__model.removeRows(self.__flags[self.data(id_index)], 1):
                    del self.__flags[self.data(id_index)]
        return True

    def submitAll(self):
        self.__model.submitAll()
