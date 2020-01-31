from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlRelation, QSqlRecord
from models import DocflagModel


class DocFlagsModel(QSqlRelationalTableModel):
    def __init__(self, doc_id):
        super(DocFlagsModel, self).__init__()

        self.setTable("cfp_docflags")
        #self.setRelation(2, QSqlRelation(
        #    "cfp_docflag", "id", "name AS `cfp_docflag.name`"))
        self.setFilter("doc_id=%s" % doc_id)

        self.setEditStrategy(QSqlRelationalTableModel.OnManualSubmit)

        self.doc_id = doc_id
        self.__flags = []
        self.__model = DocflagModel()
        self.__model.select()

    def select(self):
        if super().select():
            while self.query().next():
                self.__flags.append(self.query().value("docflag_id"))
            return True
        print(self.__flags)
        return False

    def rowCount(self, parent):
        return self.__model.rowCount()

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsUserCheckable

    def data(self, index, role):
        if not index.isValid():
            return None

        # index for DocflagModel column `id`
        id_index = self.__model.createIndex(index.row(), 0, QModelIndex())
        # index for DocflagModel column `name`
        m_index = self.__model.createIndex(index.row(), 1, QModelIndex())

        if role == Qt.CheckStateRole:
            if self.__model.data(id_index) in self.__flags:
                return Qt.Checked

            return Qt.Unchecked

        if role == Qt.DisplayRole:
            return self.__model.data(m_index)

        return None

    def setData(self, index, value, role):
        print(index.data())
        if role == Qt.CheckStateRole:
            # index for DocflagModel column `id`
            id_index = self.__model.createIndex(index.row(), 0, QModelIndex())
            # index for DocflagModel column `name`
            #m_index = self.__model.createIndex(index.row(), 1, QModelIndex())

            if(value == Qt.Checked):
                print("insert")

                record = self.record()
                record.remove(record.indexOf("id"))
                record.setValue("doc_id", self.doc_id)
                record.setValue("docflag_id", self.__model.data(id_index))
                print(self.doc_id, "/", self.__model.data(id_index))

                if self.insertRowIntoTable(record):
                    self.__flags.append(self.__model.data(id_index))
            else:
                print("remove")
                #print(self.__flags)
                print(self.__flags.index(self.__model.data(id_index)))
                if self.deleteRowFromTable(0):
                    self.__flags.remove(self.__model.data(id_index))
        return True
