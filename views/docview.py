from PyQt5.Qt import Qt
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

        self.model = None

        #proxy_model = QSortFilterProxyModel()
        #proxy_model.setSourceModel(geo_model)

    def load(self, index):
        church_id = index.internalPointer().uid()

        self.model = DocModel()

        self.model.setChurchId(church_id)
        #self.model.setFilter("church_id=\"%s\"" % church_id)
        self.model.select()

        #storageunit_delegate = StorageUnitDelegate(self)

        self.tree_view.setModel(self.model)
        #self.tree_view.setItemDelegateForColumn(1, storageunit_delegate)


        self.tree_view.setColumnWidth(0, 50)
        self.tree_view.hideColumn(1)
        self.tree_view.setColumnWidth(2, 150)
        self.tree_view.hideColumn(3)
        self.tree_view.setColumnWidth(4, 200)
        self.tree_view.hideColumn(5)
        self.tree_view.hideColumn(6)
        self.tree_view.hideColumn(7)

        #self.model.setHeaderData(1, Qt.Horizontal, "Ед. хранения")
        #self.tree_view.setColumnWidth(1, 200)

        #self.model.setHeaderData(2, Qt.Horizontal, "Тип док-та")
        #self.tree_view.setColumnWidth(2, 100)
        #self.model.setHeaderData(3, Qt.Horizontal, "Кол. листов")
        #self.tree_view.setColumnWidth(2, 50)

        #self.tree_view.hideColumn(1)
        #self.tree_view.hideColumn(5)
        #self.tree_view.hideColumn(6)

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

        v_layout.addWidget(actions_panel)
        v_layout.addWidget(tree_view)

        self.tree_view = tree_view

        self.setMainWidget(main)
