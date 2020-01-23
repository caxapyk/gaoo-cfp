from PyQt5.Qt import Qt
from PyQt5.QtCore import (QModelIndex, QItemSelection,
                          QItemSelectionModel, QSortFilterProxyModel, QSize)
from PyQt5.QtWidgets import (QFrame, QSizePolicy, QHBoxLayout, QVBoxLayout,
                             QLineEdit, QToolButton, QTreeView, QMenu, QAction, QMessageBox)
from PyQt5.QtSql import QSqlRelationalTableModel
from PyQt5.QtCore import QModelIndex
from views import (View, StorageUnitDelegate)
from models import DocModel


class DocView(View):
    def __init__(self, parent):
        super(DocView, self).__init__()
        self.parent = parent

        self.initUi()

        self.doc_model = DocModel()
        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(self.doc_model)

        self.tree_view.setModel(proxy_model)

        #self.proxy_model = proxy_model

    def load(self, index):
        #church_id = index.internalPointer().uid()

        #self.doc_model.setChurchId(church_id)
        #self.doc_model.refresh()

        #self.tree_view.setColumnWidth(0, 50)
        #self.tree_view.hideColumn(not self.tree_view.isColumnHidden(1))
        #self.tree_view.setColumnWidth(2, 50)
        #self.tree_view.hideColumn(not self.tree_view.isColumnHidden(3))
        #self.tree_view.setColumnWidth(4, 200)
        #self.tree_view.hideColumn(not self.tree_view.isColumnHidden(5))
        #self.tree_view.hideColumn(not self.tree_view.isColumnHidden(6))
        #self.tree_view.hideColumn(not self.tree_view.isColumnHidden(7))
        #self.tree_view.setColumnWidth(8, 55)
        #self.tree_view.setColumnWidth(9, 150)
        #self.tree_view.setColumnWidth(10, 200)

        #print(self.proxy_model.sortColumn())
        pass

    def initUi(self):
        actions_panel = QFrame()
        f_layout = QHBoxLayout(actions_panel)
        f_layout.setContentsMargins(2, 5, 2, 5)
        f_layout.setSpacing(5)

        main = QFrame()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(85)
        main.setSizePolicy(sizePolicy)

        v_layout = QVBoxLayout(main)
        v_layout.setContentsMargins(2, 0, 0, 0)
        v_layout.setSpacing(0)

        tree_view = QTreeView(main)
        tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        tree_view.setSortingEnabled(True)

        v_layout.addWidget(actions_panel)
        v_layout.addWidget(tree_view)

        self.tree_view = tree_view

        self.setMainWidget(main)
