from PyQt5.Qt import Qt, QCursor
from PyQt5.QtCore import (QModelIndex, QItemSelection, QItemSelectionModel)
from PyQt5.QtWidgets import (QWidget, QMenu, QMessageBox)
from PyQt5.uic import loadUi
from models import (CFPModel, GuberniaModel, UezdModel,
                    LocalityModel, ChurchModel, SQLTreeModel)


class GEOView(QWidget):

    def __init__(self, main_window):
        super(GEOView, self).__init__()

        self.tree_view = main_window.ui.treeView_geo
        self.church_btn = main_window.ui.pushButton_add_ch

        self.model = SQLTreeModel(
            (GuberniaModel(), UezdModel(), LocalityModel(), ChurchModel()),
            ("Территория",))

        self.menu = QMenu(self)

        self.setupTriggers()
        self.setupContextMenu()

    def setupTriggers(self):
        self.tree_view.setModel(self.model)
        self.tree_view.clicked.connect(self.item_clicked)

        self.church_btn.clicked.connect(self.insertItem)

    def setupContextMenu(self):
        self.tree_view.customContextMenuRequested.connect(
            self.showContextMenu)

    def showContextMenu(self, point):

        if self.currentIndex():

            self.menu.clear()

            ins_action = self.menu.addAction("Добавить")
            upd_action = self.menu.addAction("Изменить")
            del_action = self.menu.addAction("Удалить")

            ins_action.triggered.connect(self.insertItem)
            upd_action.triggered.connect(self.editItem)
            del_action.triggered.connect(self.removeItem)

            self.menu.exec(QCursor.pos())

    def insertItem(self):
        index = self.currentIndex()
        if index:
            child_count = index.internalPointer().childCount() - 1

            self.model.insertRow(child_count, index)

            item = index.child(child_count + 1, 0)
            if not self.tree_view.isExpanded(index):
                self.tree_view.setExpanded(index, True)

            selection = QItemSelection()
            selection.select(item, item)
            self.tree_view.selectionModel().select(
                selection, QItemSelectionModel.Rows | QItemSelectionModel.Select | QItemSelectionModel.Clear
            )

            self.tree_view.edit(item)

    def editItem(self):
        index = self.currentIndex()
        if index:
            self.tree_view.edit(index)

    def removeItem(self):
        index = self.currentIndex()
        if index:
            confirm = QMessageBox()
            confirm.setWindowTitle("Удаление объекта")
            confirm.setText("Вы уверены что хотите удалить этот объект?")
            confirm.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            confirm.setDefaultButton(QMessageBox.No)
            result = confirm.exec()

            if result == QMessageBox.Yes:
                self.model.removeRow(index.row(), index.parent())

    def currentIndex(self):
        idx = self.tree_view.selectedIndexes()
        if len(idx) > 0:
            return idx[0]

        return None

    def item_clicked(self, index):
        print("clicked")
