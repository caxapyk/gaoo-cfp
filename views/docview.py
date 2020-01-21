from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QFrame, QSizePolicy, QHBoxLayout, QVBoxLayout,
                             QLineEdit, QToolButton, QTreeView, QMenu, QAction, QMessageBox)
from PyQt5.QtSql import QSqlRelationalTableModel
from views import View
from models import DocModel


class DocView(View):
    def __init__(self, parent):
        super(DocView, self).__init__()
        self.parent = parent

        self.initUi()

        self.model = DocModel()

        self.tree_view.setModel(self.model)

        #proxy_model = QSortFilterProxyModel()
        #proxy_model.setSourceModel(geo_model)

    def load(self, index):
        church_id = index.internalPointer().uid()

        self.model.setChurchId(church_id)
        self.model.refresh()

        self.model.setHeaderData(2, Qt.Horizontal, "Фонд")
        self.model.setHeaderData(3, Qt.Horizontal, "Опись")
        self.model.setHeaderData(4, Qt.Horizontal, "Дело")
        self.model.setHeaderData(5, Qt.Horizontal, "Кол. листов")

        self.tree_view.hideColumn(0)
        self.tree_view.hideColumn(1)

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
