from PyQt5.Qt import Qt, QCursor, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QModelIndex, QSortFilterProxyModel, QSize)
from PyQt5.QtWidgets import (QWidget, QAbstractItemView, QFrame, QSizePolicy,
                             QHBoxLayout, QVBoxLayout, QLineEdit, QButtonGroup,
                             QPushButton, QTreeView, QMenu, QAction,
                             QMessageBox)
from models import (GuberniaModel, UezdModel,
                    LocalityModel, ChurchModel, SqlTreeModel, GroupModel)
from views import (View, GeoItemDelegate)
from widgets import TreeSortFilter


class GroupView(View):
    def __init__(self, parent):
        super(GroupView, self).__init__(parent)

        self.parent = parent
        self.docview = self.parent.doc_view

        # Build UI
        main = QFrame()
        v_layout = QVBoxLayout(main)
        v_layout.setContentsMargins(2, 0, 0, 0)
        v_layout.setSpacing(0)

        tree_view = QTreeView(main)
        tree_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        tree_view.customContextMenuRequested.connect(
            self.showContextMenu)
        tree_view.doubleClicked.connect(self.loadDocs)

        tree_view_delegate = GeoItemDelegate()
        tree_view_delegate.closeEditor.connect(self.onEditorClosed)

        tree_view.setItemDelegateForColumn(0, tree_view_delegate)

        # tree filter
        tree_filter = TreeSortFilter()
        tree_filter.setMode(TreeSortFilter.SortFilterMode)
        tree_filter.setWidget(tree_view)
        tree_filter.setFilterPlaceHolder("Фильтр по справочнику...")

        v_layout.addWidget(tree_filter)
        v_layout.addWidget(tree_view)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(15)
        main.setSizePolicy(sizePolicy)
        main.setMinimumSize(QSize(250, 0))

        c_menu = QMenu(tree_view)

        # set model
        groupfolder_model = GroupModel()

        group_model = SqlTreeModel(
            (groupfolder_model,),
            ("Группировки",))

        group_model.setModelColumn(0, 2)

        group_model.select()

        proxy_model = QSortFilterProxyModel()
        proxy_model.setFilterKeyColumn(0)
        proxy_model.setSourceModel(group_model)
        # disable auto filtering
        proxy_model.setDynamicSortFilter(False)
        # set model to tree_view
        tree_view.setModel(proxy_model)

        self.tree_view = tree_view
        self.tree_filter = tree_filter
        self.c_menu = c_menu

        self.model = proxy_model
        self.group_model = group_model

        # set main ad default widget
        self.setMainWidget(main)

    def loadDocs(self, index):
        index = self.model.mapToSource(index)
        sql_model = index.internalPointer()

        if isinstance(sql_model.model(), ChurchModel):
            self.docview.loadData(sql_model.uid())

    def showContextMenu(self, point):
        index = self.tree_view.indexAt(point)

        self.c_menu.clear()

        if index.isValid():
            source_index = self.model.mapToSource(index)
            sql_model = source_index.internalPointer()

            child_name = ""
            if isinstance(sql_model.model(), GuberniaModel):
                child_name = "уезд"
            elif isinstance(sql_model.model(), UezdModel):
                child_name = "населенный пункт"
            elif isinstance(sql_model.model(), LocalityModel):
                child_name = "церковь"

            default_actions = (
                (":/icons/folder-new-16.png", "Добавить раздел%s" % child_name,
                    lambda: self.insertItem()),
                (":/icons/delete-16.png", "Добавить группировку%s" % child_name,
                    lambda: self.insertItem()),
                (":/icons/rename-16.png", "Переименовать", self.editItem),
                (":/icons/delete-16.png", "Удалить", self.removeItem),
            )

            group_actions = (
                (":/icons/docs-folder-16.png", "Открыть документы",
                 lambda: self.loadDocs(index)),
                (":/icons/rename-16.png", "Переименовать", self.editItem),
                (":/icons/delete-16.png", "Удалить", self.removeItem),
            )

            if isinstance(sql_model.model(), GuberniaModel):
                actions_list = group_actions
            else:
                actions_list = default_actions

            for icon, text, func in actions_list:
                action = self.c_menu.addAction(text)
                action.setIcon(QIcon(icon))
                action.triggered.connect(func)

            self.c_menu.exec_(
                self.tree_view.viewport().mapToGlobal(point))

        else:
            ins_action = self.c_menu.addAction("Добавить губернию")
            ins_action.setIcon(QIcon(":/icons/folder-new-16.png"))
            ins_action.triggered.connect(self.insertTopItem)

            self.c_menu.exec(QCursor.pos())

    def onEditorClosed(self):
        if self.tree_filter.isSorted():
            self.tree_filter.sort(self.model.sortOrder())

    def insertTopItem(self):
        if self.model.insertRows(0, 1, QModelIndex()):
            self.openItemEditor(QModelIndex())
        else:
            QMessageBox().critical(
                    self.tree_view, "Создание объекта",
                    "Не удалось добавить губернию!\nВозможно у Вас недостаточно привилегий.", QMessageBox.Ok)

    def insertItem(self):
        index = self.tree_view.currentIndex()
        if index:
            if self.tree_filter.isFiltered():
                # store source model index to reload after clearFilter()
                # because index of proxy model will be changed
                m_index = self.model.mapToSource(index)
                self.tree_filter.clearAllFilters()
                # restore index
                index = self.model.mapFromSource(m_index)
                self.tree_view.setCurrentIndex(index)

            # !important: branch must be expanded before new row inserted
            self.tree_view.setExpanded(index, True)

            if self.model.insertRows(0, 1, index):
                self.openItemEditor(index)
            else:
                QMessageBox().critical(
                    self.tree_view, "Создание объекта",
                    "Не удалось добавить новый объект!\nВозможно у Вас недостаточно привилегий.", QMessageBox.Ok)

    def editItem(self):
        index = self.tree_view.currentIndex()
        if index:
            self.tree_view.edit(index)

    def removeItem(self):
        index = self.tree_view.currentIndex()
        if index:
            result = QMessageBox().critical(
                self.parent, "Удаление объекта справочника",
                "Вы уверены что хотите удалить \"%s\"?" % index.data(),
                QMessageBox.No | QMessageBox.Yes)

            if result == QMessageBox.Yes:
                if not self.model.removeRows(index.row(), 1, index.parent()):
                    QMessageBox().critical(self.tree_view, "Удаление объекта",
                                           "Не удалось удалить объект!\n\nПроверьте нет ли связей с другими объектами или возможно у Вас недостаточно привилегий.",
                                           QMessageBox.Ok)

    def openItemEditor(self, parent):
        # map underlying model index
        geo_parent = self.model.mapToSource(parent)
        geo_index = self.group_model.index(self.group_model.rowCount(
            geo_parent) - 1, 0, geo_parent)

        # map back to proxy model
        index = self.model.mapFromSource(geo_index)

        self.tree_view.setCurrentIndex(index)

        # edit new item
        self.tree_view.edit(index)
