from PyQt5 import QtCore
from PyQt5.QtCore import QModelIndex, QItemSelection, QItemSelectionModel
from PyQt5.QtWidgets import QMainWindow, QMenu, QMessageBox
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

        self.index = 0

        self.table_view_cfp()
        self.tree_view_geo()

        self.show()

        self.ui.treeView_geo.customContextMenuRequested.connect(self.show_context_menu)

        self.menu = QMenu(self)
        insert_action = self.menu.addAction("Добавить")
        del_action = self.menu.addAction("Удалить")
        insert_action.triggered.connect(self.insertRow)
        del_action.triggered.connect(self.removeRow)



    def show_context_menu(self, point):

        #action = self.menu.exec_(self.mapToGlobal(point.pos()))
        #if action == quitAct:
            #self.close()
        self.menu.exec(self.mapToGlobal(point))

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
        i = self.ui.treeView_geo.selectedIndexes()
        self.tm.insertRow(i[0].internalPointer().childCount() - 1, i[0])
        index = i[0].child(i[0].internalPointer().childCount() - 1, 0)
        if not self.ui.treeView_geo.isExpanded(i[0]):
            self.ui.treeView_geo.setExpanded(i[0], True)

        selection = QItemSelection()
        selection.select(index, index)
        self.ui.treeView_geo.selectionModel().select(
            selection, QItemSelectionModel.Rows | QItemSelectionModel.Select | QItemSelectionModel.Clear
        )

    def removeRow(self):
        confirm = QMessageBox()
        confirm.setText("Вы уверены что хотите удалить этот объект?")
        confirm.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
        confirm.setDefaultButton(QMessageBox.No)
        r = confirm.exec()
        if r == QMessageBox.Yes:
            i = self.ui.treeView_geo.selectedIndexes()
            item = i[0].internalPointer()
            print(item.itemID())
            print("index")
            print(i[0].row())
            self.tm.removeRow(i[0].row(), i[0].parent())
