from PyQt5.Qt import Qt
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QModelIndex, QAbstractListModel
from models import DocflagModel


class DocFlagsModel(DocflagModel):
    def __init__(self, flag_list=""):
        super(DocFlagsModel, self).__init__()

        if len(flag_list) > 0:
            flags = flag_list.split(",")
        else:
            flags = []

        super().select()

        self.__data = flags
        self.__flags = []

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsUserCheckable

    def data_(self):
        return self.__flags

    def data(self, index, role):
        if not index.isValid():
            return None

        if role == Qt.CheckStateRole:
            # index for DocflagModel column `id`
            id_index = self.createIndex(index.row(), 0, QModelIndex())
            if super().data(index) in self.__data:
                if super().data(id_index) not in self.__flags:
                    self.__flags.append(super().data(id_index))
                return Qt.Checked

            return Qt.Unchecked


        return super().data(index, role)

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole:
    #        # index for DocflagModel column `id`
    #        id_index = self.__model.createIndex(index.row(), 0, QModelIndex())

            if(value == Qt.Checked):
                 self.__data.append(super().data(index))
    #            record = self.__model.record()
    #            record.remove(record.indexOf("id"))
    #            record.setValue("doc_id", self.doc_id)
    #            record.setValue("docflag_id", self.data(id_index))

    #            if self.__model.insertRecord(-1, record):
    #                self.__flags[self.data(
    #                    id_index)] = self.__model.rowCount() - 1
            else:
                # index for DocflagModel column `id`
                id_index = self.createIndex(index.row(), 0, QModelIndex())

                del self.__flags[self.__flags.index(super().data(id_index))]
                del self.__data[self.__data.index(super().data(index))]
    #            if self.__model.removeRows(self.__flags[self.data(id_index)], 1):
    #                del self.__flags[self.data(id_index)]
    #    return True
        return True

    #def submitAll(self):
    #    self.__model.submitAll()
