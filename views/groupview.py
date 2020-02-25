from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QModelIndex, QSortFilterProxyModel, QSize)
from PyQt5.QtWidgets import (QSizePolicy, QMenu, QFrame,QTreeView, QVBoxLayout)
from models import (SqlTreeModel, GroupModel)
from widgets import TreeSortFilter
from views import (View, TreeItemDelegate)
from .treebaseview import TreeBaseView


class GroupView(TreeBaseView):
    def __init__(self, parent):
        super(GroupView, self).__init__(parent)

        self.parent = parent
        self.docview = self.parent.doc_view

        # Models
        groupfolder_model = GroupModel()

        group_model = SqlTreeModel(
            (groupfolder_model,),
            ("Группировки",))

        group_model.setModelColumn(0, 2)
        group_model.select()

        self.model = QSortFilterProxyModel()
        self.model.setFilterKeyColumn(0)
        self.model.setSourceModel(group_model)
        # disable auto filtering
        self.model.setDynamicSortFilter(False)

        self.main_widget = QFrame()
        v_layout = QVBoxLayout(self.main_widget)
        v_layout.setContentsMargins(2, 0, 0, 0)
        v_layout.setSpacing(0)

        # Build UI
        self.tree_view = QTreeView(self.main_widget)
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)

        tree_view_delegate = TreeItemDelegate()
        tree_view_delegate.closeEditor.connect(self.onEditorClosed)

        self.tree_view.setItemDelegateForColumn(0, tree_view_delegate)

        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(
            self.showContextMenu)
        self.tree_view.doubleClicked.connect(self.loadDocs)

        # tree filter
        self.tree_filter = TreeSortFilter()
        self.tree_filter.setWidget(self.tree_view)
        self.tree_filter.setFilterPlaceHolder("Фильтр по справочнику...")
        self.tree_filter.setMode(TreeSortFilter.SortFilterMode)

        v_layout.addWidget(self.tree_filter)
        v_layout.addWidget(self.tree_view)

        # set model to tree_view
        self.tree_view.setModel(self.model)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(15)

        self.main_widget.setSizePolicy(sizePolicy)
        self.main_widget.setMinimumSize(QSize(250, 0))

        self.setTreeView(self.tree_view)
        self.setTreeFilter(self.tree_filter)

        # set main ad default widget
        self.setMainWidget(self.main_widget)

    def loadDocs(self, index):
        index = self.model.mapToSource(index)
        sql_model = index.internalPointer()

        self.docview.loadData(sql_model.uid())

    def showContextMenu(self, point):
        index = self.tree_view.indexAt(point)

        if index.isValid():
            context_menu = self.contextMenu()
            action_doc_open = self.context_menu.addAction("Открыть документы")
            action_doc_open.triggered.connect(self.loadDocs)

            context_menu.addSeparator()

            # disable open documents if index has childen
            if self.model.hasChildren(index):
                action_doc_open.setDisabled(True)

        super().showContextMenu(point)
