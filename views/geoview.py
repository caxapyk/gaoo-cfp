from PyQt5.Qt import Qt, QCursor, QRegExp
from PyQt5.QtCore import (QModelIndex, QItemSelection,
                          QItemSelectionModel, QSortFilterProxyModel)
from PyQt5.QtWidgets import (QWidget, QMenu, QMessageBox)
from models import (CFPModel, GuberniaModel, UezdModel,
                    LocalityModel, ChurchModel, SQLGeoModel)
from dialogs import DocTypeDialog


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

        geo_model = SQLGeoModel(
            (model1, model2, model3, model4),
            ("Территория",))

        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(geo_model)

        self.model = self.proxy_model
        self.sorted = False

        self.c_menu = QMenu(self)
        self.doctype_menu = QMenu(self)

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
        if index.isValid():

            self.c_menu.clear()

            ins_action = self.c_menu.addAction("Новая запись")
            upd_action = self.c_menu.addAction("Переименовать")
            del_action = self.c_menu.addAction("Удалить")

            ins_action.triggered.connect(self.insertItem)
            upd_action.triggered.connect(self.editItem)
            del_action.triggered.connect(self.removeItem)

            if index.model().hasChildren(index):
                del_action.setEnabled(False)

            # selected model
            sel_model = index.internalPointer().model()

            if isinstance(sel_model, ChurchModel):
                ins_action.setEnabled(False)
                ins_action.setVisible(False)

                sep_acton = self.c_menu.addSeparator()

                dtype_action = self.c_menu.addAction("Виды документов")
                dtype_action.triggered.connect(self.selectDocType)

                #self.setDoctypeMenu()


            self.c_menu.exec(
                self.tree_view.viewport().mapToGlobal(point))

        else:
            self.c_menu.clear()
            ins_action = self.c_menu.addAction("Добавить губернию")
            ins_action.triggered.connect(self.insertTopItem)
            self.c_menu.exec(QCursor.pos())

    def selectDocType(self):
        doctype_dialog = DocTypeDialog()

    def setDoctypeMenu(self):
        self.doctype_menu = self.c_menu.addMenu("Типы документов")
        self.doctype_menu.addAction("Тип 1").setCheckable(True)

    def filter(self, text):
        self.tree_view.expandAll()
        self.proxy_model.setRecursiveFilteringEnabled(True)
        self.proxy_model.setFilterRegExp(
            QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))
        self.proxy_model.setFilterKeyColumn(0)

    def resetFilter(self):
        if len(self.filter_l_edit.text()) > 0:
            self.filter_l_edit.setText("")

    def sort(self):
        if not self.sorted:
            self.proxy_model.sort(0, Qt.AscendingOrder)
            self.sorted = True
        else:
            self.proxy_model.sort(-1, Qt.AscendingOrder)
            self.sorted = False

    def insertTopItem(self):
        self.proxy_model.insertRows(1, 1, QModelIndex())

    def insertItem(self):
        index = self.tree_view.currentIndex()
        if index:
            self.resetFilter()
            # set branch expanded before insert !important
            if not self.tree_view.isExpanded(index):
                self.tree_view.setExpanded(index, True)

            self.proxy_model.insertRows(0, 1, index)

            # select new item
            self.selectAndEditNewItem(index)

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

    def selectAndEditNewItem(self, parent):
        # map underlying model index
        m_parent = self.proxy_model.mapToSource(parent)
        m_child_count = m_parent.internalPointer().childCount() - 1
        m_new_item = m_parent.model().index(m_child_count, 0, m_parent)

        proxy_child = self.proxy_model.mapFromSource(m_new_item)

        selection = QItemSelection()
        selection.select(proxy_child, proxy_child)
        self.tree_view.selectionModel().select(
            selection, QItemSelectionModel.Rows | QItemSelectionModel.Select | QItemSelectionModel.Clear)

        # edit new item
        self.tree_view.edit(proxy_child)
