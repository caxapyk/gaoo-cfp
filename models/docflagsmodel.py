from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex, QAbstractListModel
from PyQt5.QtSql import QSqlQueryModel, QSqlQuery, QSqlTableModel, QSqlRelation
from models import DocflagModel


class DocFlagsModel(QAbstractListModel):
    def __init__(self, index):
        super(DocFlagsModel, self).__init__()

        flags = index.internalPointer().docflags()

        model = DocflagModel()
        model.select()

        self.__data = flags
        self.__model = model

    def rowCount(self, parent):
        return self.__model.rowCount()

    def flags(self, index):
        return super().flags(index) | Qt.ItemIsUserCheckable

    def data(self, index, role):
        if not index.isValid():
            return None

        m_index = self.createIndex(index.row(), 1, QModelIndex())

        if role == Qt.CheckStateRole:
            if self.__model.data(m_index) in self.__data:
                return Qt.Checked
            return Qt.Unchecked

        if role == Qt.DisplayRole:
            return self.__model.data(m_index)

        return None

    def setData(self, index, value, role):
        if role == Qt.CheckStateRole:
            m_index = self.createIndex(index.row(), 1, QModelIndex())

            if(value == Qt.Checked):
                self.__data.append(self.__model.data(m_index))
            else:
                self.__data.remove(self.__model.data(m_index))
        return True
