from PyQt5.QtCore import (QSortFilterProxyModel, QSize)
from PyQt5.QtWidgets import (QSizePolicy, QFrame, QVBoxLayout)
from models import (SqlTreeModel, GroupModel, DocModel)
from widgets import TreeSortFilter
from views import View
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

        self.doc_model = DocModel()

        self.model = QSortFilterProxyModel()
        self.model.setFilterKeyColumn(0)
        self.model.setSourceModel(group_model)
        # disable auto filtering
        self.model.setDynamicSortFilter(False)

        self.main_widget = QFrame()
        v_layout = QVBoxLayout(self.main_widget)
        v_layout.setContentsMargins(2, 0, 0, 0)
        v_layout.setSpacing(0)

        #self.tree_view = TreeBaseView(parent)
        # set model to tree_view
        self.tree_view.setModel(self.model)

        self.tree_view.doubleClicked.connect(self.loadDocs)
        #self.tree_view.contextMenuBeforeOpen.connect(self.initContextMenu)

        # tree filter
        self.tree_filter = TreeSortFilter(self)
        self.tree_filter.setView(self)
        self.tree_filter.setMode(TreeSortFilter.SortFilterMode)

        v_layout.addWidget(self.tree_filter)
        v_layout.addWidget(self.tree_view)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(15)

        self.main_widget.setSizePolicy(sizePolicy)
        self.main_widget.setMinimumSize(QSize(250, 0))

        # set main ad default widget
        self.setMainWidget(self.main_widget)

    def loadDocs(self, index):
        if self.isEndPointReached(index):
            index = self.model.mapToSource(index)
            sql_model = index.internalPointer()

            self.docview.loadData(sql_model.uid())

    def showContextMenu(self, point):
        index = self.tree_view.indexAt(point)
        source_index = self.model.mapToSource(index)
        item_type = source_index.internalPointer().itemType()

        if item_type == GroupModel.TypeGroup:
            action_doc_open = self.context_menu.addAction("Связанные документы")
            action_doc_open.triggered.connect(lambda: self.loadDocs(index))

            self.context_menu.addSeparator()

            # disable open documents if index has childen
            if self.model.hasChildren(index):
                action_doc_open.setDisabled(True)

        super().showContextMenu(point)

    def isEndPointReached(self, index):
        if index.isValid():
            # reach endpoint if item type is TypeGroup
            source_index = self.model.mapToSource(index)
            item_type = source_index.internalPointer().itemType()

            if item_type == GroupModel.TypeGroup:
                return True
        return False

