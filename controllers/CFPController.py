from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from models.CFPModel import CFPModel
from models.SQLTreeModel import SQLTreeModel


from PyQt5.QtSql import QSqlQueryModel
from PyQt5.Qt import Qt


class CFPController(QMainWindow):

    def __init__(self):
        super(CFPController, self).__init__()
        self.ui = loadUi("ui/main_window.ui", self)


        self._model = QSqlQueryModel()
        self._model.setQuery("SELECT * FROM cfp_gubernia")

        self._model2 = QSqlQueryModel()
        self._model2.setQuery("SELECT * FROM cfp_uezd")

        self._model3 = QSqlQueryModel()
        self._model3.setQuery("SELECT * FROM cfp_locality")

        self._model4 = QSqlQueryModel()
        self._model4.setQuery("SELECT * FROM cfp_church")

        self.table_view_cfp()
        self.tree_view_geo()

        self.show()

    def table_view_cfp(self):
        model = CFPModel()
        self.ui.tableView_cfp.setModel(model.select())

    def tree_view_geo(self):
        #_model.setHeaderData(0, Qt.Horizontal, "Name

        self.ui.treeView_geo.setModel(SQLTreeModel(("Территория",),(self._model, self._model2, self._model3, self._model4)))
        self.ui.treeView_geo.clicked.connect(self.test) # Note that the the signal is now a attribute of the widget.

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def test(self, index):
        print("clicked")
        indexItem = self._model.data(index)
        print(index.row())
        print(index.column())
        parent = index.parent()
        print(index.model().level(index))
