from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QMainWindow, QMenu
from PyQt5.uic import loadUi
from models import (CFPModel, GuberniaModel, UezdModel, LocalityModel, ChurchModel)
from models.SQLTreeModel import SQLTreeModel


from PyQt5.QtSql import QSqlQueryModel
from PyQt5.Qt import Qt


class CFPController(QMainWindow):

    def __init__(self):
        super(CFPController, self).__init__()
        self.ui = loadUi("ui/main_window.ui", self)

        self.m_gubernia = GuberniaModel()
        self.m_uezd = UezdModel()
        self.m_locality = LocalityModel()
        self.m_church = ChurchModel()

        self.tm = SQLTreeModel(("Территория",), (
            self.m_gubernia,
            self.m_uezd,
            self.m_locality,
            self.m_church
        ))

        self.index = 0;


        self.table_view_cfp()
        self.tree_view_geo()

        self.show()

    def table_view_cfp(self):
        model = CFPModel()
        self.ui.tableView_cfp.setModel(model.select())

    def tree_view_geo(self):
        self.ui.treeView_geo.setModel(self.tm)

        self.ui.treeView_geo.clicked.connect(self.test)
        self.ui.pushButton_add_ch.clicked.connect(self.insertRow)

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def test(self, index):
        print("clicked")
        #indexItem = self._model.data(index)
        print(index.row())
        print(index.column())
        parent = index.parent()
        print(index.model().level(index))
        self.index = index

    def insertRow(self):
        self.tm.insertRow( 0, self.index)
