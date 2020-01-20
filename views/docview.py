from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QFrame, QSizePolicy, QHBoxLayout, QVBoxLayout,
                             QLineEdit, QToolButton, QTreeView, QMenu, QAction, QMessageBox)
from PyQt5.QtSql import QSqlRelationalTableModel
from views import View


class DocView(View):
    def __init__(self, parent):
        super(DocView, self).__init__()
        self.parent = parent

        self.initUi()

        docs = QSqlRelationalTableModel()
        docs.setTable("cfp_church")
        docs.select()

        #proxy_model = QSortFilterProxyModel()
        #proxy_model.setSourceModel(geo_model)

        self.tree_view.setModel(docs)

        #self.model = proxy_model

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
