from PyQt5.Qt import Qt, QCursor, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QModelIndex, QItemSelection,
                          QItemSelectionModel, QSortFilterProxyModel)
from PyQt5.QtWidgets import (QWidget, QMenu, QAction, QMessageBox)
from models import (GuberniaModel, UezdModel,
                    LocalityModel, ChurchModel, SqlTreeModel)


class GEOView(QWidget):

    def __init__(self, main_window):
        super(GEOView, self).__init__()

        self.main_window = main_window

        self.tree_view = main_window.ui.treeView_geo
        self.sort_btn = main_window.ui.toolButton_sort
        self.filter_l_edit = main_window.ui.lineEdit_geo_filter
        self.clearfilter_btn = main_window.ui.toolButton_clearFilter

        model1 = GuberniaModel()
        model2 = UezdModel()
        model3 = LocalityModel()
        model4 = ChurchModel()

        geo_model = SqlTreeModel(
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
        self.clearfilter_btn.clicked.connect(self.clearFilter)

    def setupContextMenu(self):
        self.tree_view.customContextMenuRequested.connect(
            self.showContextMenu)

    def showContextMenu(self, point):
        proxy_index = self.tree_view.indexAt(point)
        index = self.proxy_model.mapToSource(proxy_index)

        self.c_menu.clear()

        if index.isValid():
            # selected model
            sel_model = index.internalPointer().model()

            ins_action = self.c_menu.addAction("Новый элемент")
            upd_action = self.c_menu.addAction("Переименовать")
            del_action = self.c_menu.addAction("Удалить")

            # add icons
            ins_action.setIcon(QIcon(":/icons/folder-new-16.png"))
            upd_action.setIcon(QIcon(":/icons/rename-16.png"))
            del_action.setIcon(QIcon(":/icons/folder-delete-16.png"))

            if isinstance(sel_model, GuberniaModel):
                ins_action.setText("Новый узед")

            elif isinstance(sel_model, UezdModel):
                ins_action.setText("Новый населенный пункт")

            elif isinstance(sel_model, LocalityModel):
                ins_action.setText("Новая церковь")
                ins_action.setIcon(QIcon(":/icons/church-16.png"))

            # set triggers
            ins_action.triggered.connect(self.insertItem)
            upd_action.triggered.connect(self.editItem)
            del_action.triggered.connect(self.removeItem)

            if isinstance(sel_model, ChurchModel):
                ins_action.setEnabled(False)
                ins_action.setVisible(False)

                del_action.setIcon(QIcon(":/icons/delete-16.png"))

                # sep_acton = self.c_menu.addSeparator()

                open_action = QAction(
                    QIcon(":/icons/docs-folder-16.png"), "Открыть документы")

                self.c_menu.insertAction(ins_action, open_action)

                #open_action.triggered.connect(self.openDocs)

            # prevent delete if node has children
            if index.model().hasChildren(index):
                del_action.setEnabled(False)

                # self.setDoctypeMenu()

            self.c_menu.exec(
                self.tree_view.viewport().mapToGlobal(point))

        else:
            ins_action = self.c_menu.addAction("Новая губерния")
            ins_action.setIcon(QIcon(":/icons/folder-new-16.png"))
            ins_action.triggered.connect(self.insertTopItem)

            self.c_menu.exec(QCursor.pos())

    def selectDocType(self):
        index = self.tree_view.currentIndex()
        s_index = self.proxy_model.mapToSource(index)

        doctype_dialog = SetDTDialog(s_index)

    def setDoctypeMenu(self):
        self.doctype_menu = self.c_menu.addMenu("Типы документов")
        self.doctype_menu.addAction("Тип 1").setCheckable(True)

    def filter(self, text):
        self.tree_view.expandAll()
        self.proxy_model.setRecursiveFilteringEnabled(True)
        self.proxy_model.setFilterRegExp(
            QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))
        self.proxy_model.setFilterKeyColumn(0)

    def clearFilter(self):
        if len(self.filter_l_edit.text()) > 0:
            self.filter_l_edit.setText("")

    def sort(self):
        if not self.sorted:
            self.sort_btn.setIcon(QIcon(":/icons/sort19-16.png"))
            self.proxy_model.sort(0, Qt.AscendingOrder)
            self.sorted = True
        else:
            self.sort_btn.setIcon(QIcon(":/icons/sort-az-16.png"))
            self.proxy_model.sort(-1, Qt.AscendingOrder)
            self.sorted = False

    def insertTopItem(self):
        self.proxy_model.insertRows(1, 1, QModelIndex())

    def insertItem(self):
        index = self.tree_view.currentIndex()
        if index:
            self.clearFilter()
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
            result = QMessageBox().critical(
                self.main_window, "Удаление объекта",
                "Вы уверены что хотите удалить \"%s\"?" % index.data(),
                QMessageBox.No | QMessageBox.Yes)

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
