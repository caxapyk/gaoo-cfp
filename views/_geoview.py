from PyQt5.Qt import Qt, QCursor, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QModelIndex, QSortFilterProxyModel, QSize)
from PyQt5.QtWidgets import (QWidget, QAbstractItemView, QFrame, QSizePolicy,
                             QHBoxLayout, QVBoxLayout, QLineEdit, QButtonGroup,
                             QPushButton, QTreeView, QMenu, QAction,
                             QMessageBox)
from models import (GuberniaModel, UezdModel,
                    LocalityModel, ChurchModel, SqlTreeModel)
from views import (View, TreeItemDelegate)


class GEOView(View):
    def __init__(self, parent):
        super(GEOView, self).__init__(parent)

        self.parent = parent
        self.docview = self.parent.doc_view

        # 0 - sort by ID asc, 1 - sort by name asc, 2 - sort by name desc
        self.currentSortType = 0
        self.filtered = False

        # Build UI
        filter_panel = QFrame()
        f_layout = QHBoxLayout(filter_panel)
        f_layout.setContentsMargins(0, 5, 0, 5)
        f_layout.setSpacing(5)

        geofilter_lineedit = QLineEdit(filter_panel)
        geofilter_lineedit.setPlaceholderText("Фильтр по справочнику...")
        geofilter_lineedit.textChanged.connect(self.filter)

        clearfilter_btn = QPushButton(filter_panel)
        clearfilter_btn.setIcon(QIcon(":/icons/clear-filter-16.png"))
        clearfilter_btn.setToolTip("Сбросить фильтр")
        clearfilter_btn.setDisabled(True)
        clearfilter_btn.clicked.connect(self.clearFilter)

        f_layout.addWidget(geofilter_lineedit)
        f_layout.addWidget(clearfilter_btn)

        sort_group = QButtonGroup(filter_panel)
        sort_buttons = (
            (":/icons/sort19-16.png", "Cортировка по списку заполнения"),
            (":/icons/sort-az-16.png", "Cортировка по алфавиту \
                (по возрастанию)"),
            (":/icons/sort-za-16.png", "Cортировка по алфавиту (по убыванию)"),
        )
        for i, button in enumerate(sort_buttons):
            sort_btn = QPushButton(filter_panel)
            sort_btn.setIcon(QIcon(button[0]))
            sort_btn.setToolTip(button[1])
            sort_btn.setCheckable(True)
            if i == 0:
                sort_btn.setChecked(True)

            sort_group.addButton(sort_btn, i)
            f_layout.addWidget(sort_btn)

        sort_group.buttonClicked[int].connect(self.sort)

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

        tree_view_delegate = TreeItemDelegate()
        tree_view_delegate.closeEditor.connect(self.onEditorClosed)

        tree_view.setItemDelegateForColumn(0, tree_view_delegate)

        v_layout.addWidget(filter_panel)
        v_layout.addWidget(tree_view)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(15)
        main.setSizePolicy(sizePolicy)
        main.setMinimumSize(QSize(250, 0))

        c_menu = QMenu(tree_view)

        # set models
        gubernia = GuberniaModel()
        uezd = UezdModel()
        locality = LocalityModel()
        church = ChurchModel()

        geo_model = SqlTreeModel(
            (gubernia, uezd, locality, church),
            ("Документы (по территор. признаку)",))
        geo_model.setModelColumn(0, 1)
        geo_model.setModelColumn(1, 2)
        geo_model.setModelColumn(2, 2)
        geo_model.setModelColumn(3, 2)

        geo_model.select()

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(geo_model)
        # disable auto filtering
        proxy_model.setDynamicSortFilter(False)
        # set model to tree_view
        tree_view.setModel(proxy_model)

        self.geofilter_lineedit = geofilter_lineedit
        self.clearfilter_btn = clearfilter_btn
        self.tree_view = tree_view
        self.c_menu = c_menu

        self.model = proxy_model
        self.geo_model = geo_model

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
                (":/icons/folder-new-16.png", "Добавить %s" % child_name,
                    self.insertItem),
                (":/icons/rename-16.png", "Переименовать", self.editItem),
                (":/icons/delete-16.png", "Удалить", self.removeItem),
            )

            church_actions = (
                (":/icons/docs-folder-16.png", "Открыть документы",
                 lambda: self.loadDocs(index)),
                (":/icons/rename-16.png", "Переименовать", self.editItem),
                (":/icons/delete-16.png", "Удалить", self.removeItem),
            )

            if isinstance(sql_model.model(), ChurchModel):
                actions_list = church_actions
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

    def filter(self, text):
        self.clearfilter_btn.setDisabled((len(text) == 0))

        self.tree_view.expandAll()

        self.model.setRecursiveFilteringEnabled(True)
        self.model.setFilterRegExp(
            QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))

        self.model.setFilterKeyColumn(0)

        self.filtered = True

    def clearFilter(self):
        if len(self.geofilter_lineedit.text()) > 0:
            self.geofilter_lineedit.setText("")
            self.clearfilter_btn.setDisabled(True)

            self.model.invalidateFilter()

            self.sort(self.currentSortType)

    def sort(self, sort_type):
        if sort_type == 0:
            self.model.sort(-1)
        elif sort_type == 1:
            self.model.sort(0, Qt.AscendingOrder)
        elif sort_type == 2:
            self.model.sort(0, Qt.DescendingOrder)
        else:
            self.sort(self.currentSortType)

        self.currentSortType = sort_type

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
            if self.filtered:
                # store source model index to reload after clearFilter()
                # because index of proxy model will be changed
                m_index = self.model.mapToSource(index)
                self.clearFilter()
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

    def onEditorClosed(self):
        self.sort(self.currentSortType)

    def openItemEditor(self, parent):
        # map underlying model index
        geo_parent = self.model.mapToSource(parent)
        geo_index = self.geo_model.index(self.geo_model.rowCount(
            geo_parent) - 1, 0, geo_parent)

        # map back to proxy model
        index = self.model.mapFromSource(geo_index)

        self.tree_view.setCurrentIndex(index)

        # edit new item
        self.tree_view.edit(index)
