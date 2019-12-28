from PyQt5.Qt import Qt, QCursor, QRegExp
from PyQt5.QtCore import (QModelIndex, QItemSelection,
                          QItemSelectionModel, QSortFilterProxyModel)
from PyQt5.QtWidgets import (QWidget, QMenu, QMessageBox)
from PyQt5.uic import loadUi
from models import (CFPModel, GuberniaModel, UezdModel,
                    LocalityModel, ChurchModel, SQLTreeModel)


class GEOView(QWidget):

    def __init__(self, main_window):
        super(GEOView, self).__init__()

        self.tree_view = main_window.ui.treeView_geo
        self.sort_btn = main_window.ui.pushButton_sort
        self.filter_l_edit = main_window.ui.lineEdit_geo_filter

        model1 = GuberniaModel()
        model2 = UezdModel()
        model3 = LocalityModel()
        model4 = ChurchModel()

        geo_model = SQLTreeModel(
            (model1, model2, model3, model4),
            ("Территория",))

        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(geo_model)

        self.model = self.proxy_model
        self.sorted = False

        self.c_menu = QMenu(self)

        self.setupTriggers()
        self.setupContextMenu()

    def setupTriggers(self):
        self.tree_view.setModel(self.model)
        self.sort_btn.clicked.connect(self.sort)
        self.filter_l_edit.textChanged.connect(self.filter)

    def setupContextMenu(self):
        self.tree_view.customContextMenuRequested.connect(
            self.showContextMenu)

    def showContextMenu(self, point):
        proxy_index = self.tree_view.indexAt(point)
        index = self.proxy_model.mapToSource(proxy_index)
        if (index.isValid()):

            self.c_menu.clear()

            ins_action = self.c_menu.addAction("Добавить")
            upd_action = self.c_menu.addAction("Переименовать")
            del_action = self.c_menu.addAction("Удалить")

            ins_action.triggered.connect(self.insertItem)
            upd_action.triggered.connect(self.editItem)
            del_action.triggered.connect(self.removeItem)

            # selected model
            sel_model = index.internalPointer().model()
            if isinstance(sel_model, ChurchModel):
                ins_action.setEnabled(False)

            self.c_menu.exec(
                self.tree_view.viewport().mapToGlobal(point))

    def filter(self, text):
        self.tree_view.expandAll()
        #self.proxy_model.setRecursiveFilteringEnabled(True)
        self.proxy_model.setFilterRegExp(QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))
        self.proxy_model.setFilterKeyColumn(0)

    def sort(self):
        if not self.sorted:
            self.proxy_model.sort(0, Qt.AscendingOrder)
            self.sorted = True
        else:
            self.proxy_model.sort(-1, Qt.AscendingOrder)
            self.sorted = False

    def insertItem(self):
        index = self.tree_view.currentIndex()
        if index:
            # set branch expanded before insert !important
            if not self.tree_view.isExpanded(index):
                self.tree_view.setExpanded(index, True)

            # map underlying model index
            m_index = self.proxy_model.mapToSource(index)
            m_rows = m_index.internalPointer().childCount()

            self.proxy_model.insertRows(m_rows, 1, index)

            # select new item
            m_child = m_index.model().index(m_rows, 0, m_index)
            proxy_child = self.proxy_model.mapFromSource(m_child)

            selection = QItemSelection()
            selection.select(proxy_child, proxy_child)
            self.tree_view.selectionModel().select(
                selection, QItemSelectionModel.Rows | QItemSelectionModel.Select | QItemSelectionModel.Clear)

            # edit new item
            self.tree_view.edit(proxy_child)

    def editItem(self):
        index = self.tree_view.currentIndex()
        if index:
            self.tree_view.edit(index)

    def removeItem(self):
        index = self.tree_view.currentIndex()
        if index:
            confirm = QMessageBox()
            confirm.setWindowTitle("Удаление объекта")
            confirm.setText("Вы уверены что хотите удалить этот объект?")
            confirm.setStandardButtons(QMessageBox.No | QMessageBox.Yes)
            confirm.setDefaultButton(QMessageBox.No)
            result = confirm.exec()

            if result == QMessageBox.Yes:
                self.model.removeRows(index.row(), 1, index.parent())
