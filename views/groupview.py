from PyQt5.Qt import Qt
from PyQt5.QtCore import (QSortFilterProxyModel, QSize)
from PyQt5.QtWidgets import (QSizePolicy, QFrame, QTreeView, QVBoxLayout)
from models import (SqlTreeModel, GroupModel)
from widgets import TreeSortFilter
from views import (View, TreeItemDelegate)
from .treebaseview import TreeBaseView


class GroupView(View):
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

        self.tree_view = TreeBaseView()
        # set model to tree_view
        self.tree_view.setModel(self.model)

        self.tree_view.treeView().doubleClicked.connect(self.loadDocs)

        # tree filter
        self.tree_filter = TreeSortFilter(self)
        self.tree_filter.setWidget(self.tree_view)
        self.tree_filter.setFilterPlaceHolder("Фильтр по справочнику...")
        self.tree_filter.setMode(TreeSortFilter.SortFilterMode)

        v_layout.addWidget(self.tree_filter)
        v_layout.addWidget(self.tree_view.mainWidget())

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(15)

        self.main_widget.setSizePolicy(sizePolicy)
        self.main_widget.setMinimumSize(QSize(250, 0))

        # set main ad default widget
        self.setMainWidget(self.main_widget)

    def loadDocs(self, index):
        index = self.model.mapToSource(index)
        sql_model = index.internalPointer()

        self.docview.loadData(sql_model.uid())

    def showContextMenu(self, point):
        # do not work

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
