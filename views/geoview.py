from PyQt5.Qt import Qt, QCursor, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QModelIndex, QItemSelection,
                          QItemSelectionModel, QSortFilterProxyModel)
from PyQt5.QtWidgets import (QFrame, QHBoxLayout, QVBoxLayout, QLineEdit,
                             QToolButton, QTreeView, QMenu, QAction, QMessageBox)
from models import (GuberniaModel, UezdModel,
                    LocalityModel, ChurchModel, SqlTreeModel)
from views import View


class GEOView(View):
    def __init__(self, parent):
        super(GEOView, self).__init__()

        self.parent = parent
        self.sorted = False

        self.setUi()
        self.setModels()
        self.setTriggers()

        self.tree_view.setModel(self.model)

    def setUi(self):
        filter_panel = QFrame()
        f_layout = QHBoxLayout(filter_panel)
        f_layout.setContentsMargins(2, 5, 2, 5)
        f_layout.setSpacing(5)

        geo_filter = QLineEdit(filter_panel)
        geo_filter.setObjectName("geo_filter")
        geo_filter.setPlaceholderText("Фильтр по справочнику...")

        clearfilter_btn = QToolButton(filter_panel)
        clearfilter_btn.setObjectName("clearfilter_btn")
        clearfilter_btn.setIcon(QIcon(":/icons/clear-filter-16.png"))
        clearfilter_btn.setToolTip("Сбросить фильтр")
        clearfilter_btn.setDisabled(True)

        sort_btn = QToolButton(filter_panel)
        sort_btn.setObjectName("sort_btn")
        sort_btn.setIcon(QIcon(":/icons/sort-az-16.png"))
        sort_btn.setToolTip("<html><head/><body><p>Сортировка справочника:</p><p><img src=\":/icons/sort19-16.png\"/><span style=\" color:#555753;\">&nbsp;сортировка по алфавиту</span></p><p><img src=\":/icons/sort-az-16.png\"/><span style=\" color:#555753;\">&nbsp;сортировка по списку заполнения</span></p></body></html>")

        f_layout.addWidget(geo_filter)
        f_layout.addWidget(clearfilter_btn)
        f_layout.addWidget(sort_btn)

        main = QFrame()
        v_layout = QVBoxLayout(main)
        v_layout.setContentsMargins(2, 0, 0, 0)
        v_layout.setSpacing(0)

        tree_view = QTreeView(main)
        tree_view.setObjectName("tree_view")
        tree_view.setContextMenuPolicy(Qt.CustomContextMenu)

        v_layout.addWidget(filter_panel)
        v_layout.addWidget(tree_view)

        self.sort_btn = sort_btn
        self.geo_filter = geo_filter
        self.clearfilter_btn = clearfilter_btn
        self.tree_view = tree_view

        self.c_menu = QMenu(tree_view)

        # set main ad default widget
        self.setMainWidget(main)

    def setModels(self):
        gubernia = GuberniaModel()
        uezd = UezdModel()
        locality = LocalityModel()
        church = ChurchModel()

        geo_model = SqlTreeModel(
            (gubernia, uezd, locality, church),
            ("Территория",))

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(geo_model)

        self.model = proxy_model

    def setTriggers(self):
        self.sort_btn.clicked.connect(self.sort)
        self.geo_filter.textChanged.connect(self.filter)
        self.clearfilter_btn.clicked.connect(self.clearFilter)
        self.tree_view.customContextMenuRequested.connect(
            self.showContextMenu)

    def showContextMenu(self, point):
        print("contex")
        proxy_index = self.tree_view.indexAt(point)
        index = self.model.mapToSource(proxy_index)

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

                # open_action.triggered.connect(self.openDocs)

            # prevent delete if node has children
            if index.model().hasChildren(index):
                del_action.setEnabled(False)

            self.c_menu.exec(
                self.tree_view.viewport().mapToGlobal(point))

        else:
            ins_action = self.c_menu.addAction("Новая губерния")
            ins_action.setIcon(QIcon(":/icons/folder-new-16.png"))
            ins_action.triggered.connect(self.insertTopItem)

            self.c_menu.exec(QCursor.pos())

    def filter(self, text):
        self.clearfilter_btn.setDisabled(False)
        self.tree_view.expandAll()
        self.model.setRecursiveFilteringEnabled(True)
        self.model.setFilterRegExp(
            QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))
        self.model.setFilterKeyColumn(0)

    def clearFilter(self):
        if len(self.geo_filter.text()) > 0:
            self.geo_filter.setText("")
            self.clearfilter_btn.setDisabled(True)

    def sort(self):
        if not self.sorted:
            self.sort_btn.setIcon(QIcon(":/icons/sort19-16.png"))
            self.model.sort(0, Qt.AscendingOrder)
            self.sorted = True
        else:
            self.sort_btn.setIcon(QIcon(":/icons/sort-az-16.png"))
            self.model.sort(-1, Qt.AscendingOrder)
            self.sorted = False

    def insertTopItem(self):
        self.model.insertRows(1, 1, QModelIndex())

    def insertItem(self):
        index = self.tree_view.currentIndex()
        if index:
            self.clearFilter()
            # set branch expanded before insert !important
            if not self.tree_view.isExpanded(index):
                self.tree_view.setExpanded(index, True)

            self.model.insertRows(0, 1, index)

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
                self.parent, "Удаление объекта",
                "Вы уверены что хотите удалить \"%s\"?" % index.data(),
                QMessageBox.No | QMessageBox.Yes)

            if result == QMessageBox.Yes:
                self.model.removeRows(index.row(), 1, index.parent())

    def selectAndEditNewItem(self, parent):
        # map underlying model index
        m_parent = self.model.mapToSource(parent)
        m_child_count = m_parent.internalPointer().childCount() - 1
        m_new_item = m_parent.model().index(m_child_count, 0, m_parent)

        proxy_child = self.model.mapFromSource(m_new_item)

        selection = QItemSelection()
        selection.select(proxy_child, proxy_child)
        self.tree_view.selectionModel().select(
            selection, QItemSelectionModel.Rows | QItemSelectionModel.Select | QItemSelectionModel.Clear)

        # edit new item
        self.tree_view.edit(proxy_child)
