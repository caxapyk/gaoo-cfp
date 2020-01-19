from PyQt5.Qt import Qt, QCursor, QRegExp
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QModelIndex, QItemSelection,
                          QItemSelectionModel, QSortFilterProxyModel, QSize)
from PyQt5.QtWidgets import (QWidget, QFrame, QSizePolicy, QHBoxLayout, QVBoxLayout,
                             QLineEdit, QButtonGroup, QPushButton, QTreeView, QMenu, QAction, QMessageBox, QItemDelegate)
from models import (GuberniaModel, UezdModel,
                    LocalityModel, ChurchModel, SqlTreeModel)
from views import View


class GEOView(View):
    def __init__(self, parent):
        super(GEOView, self).__init__()

        self.parent = parent
        self.az_sorted = False
        self.filtered = False

        self.setUi()
        self.setModels()
        self.setTriggers()

    def setUi(self):
        filter_panel = QFrame()
        f_layout = QHBoxLayout(filter_panel)
        f_layout.setContentsMargins(2, 5, 2, 5)
        f_layout.setSpacing(5)

        geo_filter = QLineEdit(filter_panel)
        geo_filter.setPlaceholderText("Фильтр по справочнику...")

        clearfilter_btn = QPushButton(filter_panel)
        clearfilter_btn.setIcon(QIcon(":/icons/clear-filter-16.png"))
        clearfilter_btn.setToolTip("Сбросить фильтр")
        clearfilter_btn.setDisabled(True)

        f_layout.addWidget(geo_filter)
        f_layout.addWidget(clearfilter_btn)

        sort_group = QButtonGroup(filter_panel)
        sort_buttons = (
            (":/icons/sort19-16.png", "Cортировка по списку заполнения"),
            (":/icons/sort-az-16.png", "Cортировка по алфавиту (по возрастанию)"),
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

        main = QFrame()
        v_layout = QVBoxLayout(main)
        v_layout.setContentsMargins(2, 0, 0, 0)
        v_layout.setSpacing(0)

        tree_view = QTreeView(main)
        tree_view.setContextMenuPolicy(Qt.CustomContextMenu)

        v_layout.addWidget(filter_panel)
        v_layout.addWidget(tree_view)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(15)
        main.setSizePolicy(sizePolicy)
        main.setMinimumSize(QSize(250, 0))

        self.sort_group = sort_group
        #self.sort_inc_btn = sort_inc_btn
        #self.sort_az_btn = sort_az_btn
        #self.sort_za_btn = sort_za_btn
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

        self.tree_view.setModel(proxy_model)
        self.delegate = QItemDelegate()
        #self.tree_view.setItemDelegateForColumn(1, self.delegate)

        self.model = proxy_model
        self.base_model = geo_model

    def setTriggers(self):
        self.delegate.closeEditor.connect(self.sort)
        self.sort_group.buttonClicked[int].connect(self.sort)
        #self.sort_group.buttonClicked.connect(self.sort_az)
        #self.sort_group.buttonClicked.connect(self.sort_za)
        #self.sort_az_btn.clicked.connect(self.sort_az)
        #self.sort_inc_btn.clicked.connect(self.sort_inc)
        self.geo_filter.textChanged.connect(self.filter)
        self.clearfilter_btn.clicked.connect(self.clearFilter)
        self.tree_view.customContextMenuRequested.connect(
            self.showContextMenu)

    def showContextMenu(self, point):
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
        self.filtered = True

    def clearFilter(self):
        if len(self.geo_filter.text()) > 0:
            self.geo_filter.setText("")
            self.model.invalidateFilter()
            self.clearfilter_btn.setDisabled(True)

    def sort(self, typ):
        print(typ)
        print(self.sort_group.checkedId())
        print("sdfsdfsf")
        #self.sort_az(self)

    def sort_az(self):
        #self.sort_az_btn.setChecked(True)
        #self.sort_inc_btn.setChecked(False)

        #if not self.az_sorted:
        #    self.sort_az_btn.setIcon(QIcon(":/icons/sort-az-16.png"))
        self.model.sort(0, Qt.AscendingOrder)
        #    self.az_sorted = True
        #else:
        #    self.sort_az_btn.setIcon(QIcon(":/icons/sort-za-16.png"))
        #    self.model.sort(0, Qt.DescendingOrder)
        #    self.az_sorted = False

    def sort_za(self):
        #self.sort_az_btn.setChecked(True)
        #self.sort_inc_btn.setChecked(False)

        #if not self.az_sorted:
        #self.sort_az_btn.setIcon(QIcon(":/icons/sort-az-16.png"))
        #    self.model.sort(0, Qt.AscendingOrder)
        #self.az_sorted = True
        #else:
        #    self.sort_az_btn.setIcon(QIcon(":/icons/sort-za-16.png"))
        self.model.sort(0, Qt.DescendingOrder)
        #    self.az_sorted = False

    def sort_inc(self):
        #self.sort_inc_btn.setChecked(True)
        #self.sort_az_btn.setChecked(False)
        #self.sort_az_btn.setIcon(QIcon(":/icons/sort-az-16.png"))

        self.model.sort(-1, Qt.AscendingOrder)

    def insertTopItem(self):
        self.model.insertRows(1, 1, QModelIndex())

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
            
            # !important: branch must be expanded before insert
            self.tree_view.setExpanded(index, True)

            self.model.insertRows(0, 1, index)
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
