from PyQt5.Qt import Qt, QCursor
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import (QModelIndex, QSortFilterProxyModel, QSize)
from PyQt5.QtWidgets import (QSizePolicy, QMenu)
from models import (SqlTreeModel, GroupModel)
from widgets import TreeSortFilter
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

        self.treeView().setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView().customContextMenuRequested.connect(
            self.showContextMenu)
        self.treeView().doubleClicked.connect(self.loadDocs)

        # set model to tree_view
        self.treeView().setModel(self.model)

        self.treeFilter().setFilterPlaceHolder("Фильтр по справочнику...")
        self.treeFilter().setMode(TreeSortFilter.SortFilterMode)

        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(15)

        self.mainWidget().setSizePolicy(sizePolicy)
        self.mainWidget().setMinimumSize(QSize(250, 0))

        self.context_menu = QMenu(self.treeView())

    def loadDocs(self, index):
        index = self.model.mapToSource(index)
        sql_model = index.internalPointer()

        self.docview.loadData(sql_model.uid())

    def showContextMenu(self, point):
        index = self.treeView().indexAt(point)

        self.context_menu.clear()

        if index.isValid():
            source_index = self.model.mapToSource(index)
            sql_model = source_index.internalPointer()

            display_name = sql_model.model().displayName()

            actions = (
                (None, "Открыть документы",
                    lambda: self.loadDocs(index)),
                (":/icons/folder-new-16.png", "Создать %s" % display_name,
                    self.insertRow),
                (":/icons/rename-16.png", "Переименовать", self.editRow),
                (":/icons/delete-16.png", "Удалить", self.removeRow),
            )

            for i, action in enumerate(actions):
                _action = self.context_menu.addAction(action[1])
                _action.setIcon(QIcon(action[0]))
                _action.triggered.connect(action[2])
                if i == 0:
                    self.context_menu.addSeparator()
                if i == 0 and index.model().hasChildren(index):
                    # disable open documents if index has childen
                    _action.setDisabled(True)

            self.context_menu.exec_(
                self.treeView().viewport().mapToGlobal(point))

        else:
            ins_action = self.context_menu.addAction("Создать группировку")
            ins_action.setIcon(QIcon(":/icons/folder-new-16.png"))
            ins_action.triggered.connect(self.insertRow)

            self.treeView().setCurrentIndex(QModelIndex())
            self.context_menu.exec_(QCursor.pos())
