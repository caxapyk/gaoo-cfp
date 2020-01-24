from PyQt5.Qt import Qt, QCursor, QRegExp
from PyQt5.QtCore import (QModelIndex, QItemSelection,
                          QItemSelectionModel, QSortFilterProxyModel, QSize)
from PyQt5.QtWidgets import (QWidget, QAbstractItemView, QFrame, QSizePolicy, QHBoxLayout, QVBoxLayout, QLineEdit,
                             QButtonGroup, QPushButton, QTreeView, QMenu, QAction, QMessageBox)
from PyQt5.QtGui import QIcon
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

    def initUi(self):
        topline = QFrame()
        topline_layout = QHBoxLayout(topline)
        topline_layout.setContentsMargins(0, 0, 0, 0)

        actions_panel = QFrame(topline)
        a_layout = QHBoxLayout(actions_panel)
        topline_layout.setSpacing(0)

        insert_btn = QPushButton(actions_panel)
        insert_btn.setIcon(QIcon(":/icons/doc-new-20.png"))
        insert_btn.setIconSize(QSize(20, 20))
        insert_btn.setFlat(True)
        insert_btn.setToolTip("Добавить новый документ")
        insert_btn.setDisabled(True)
        insert_btn.clicked.connect(self.insertRow)

        edit_btn = QPushButton(actions_panel)
        edit_btn.setIcon(QIcon(":/icons/doc-edit-20.png"))
        edit_btn.setIconSize(QSize(20, 20))
        edit_btn.setFlat(True)
        edit_btn.setToolTip("Редактировать документ")
        edit_btn.setDisabled(True)
        edit_btn.clicked.connect(self.editRow)

        delete_btn = QPushButton(actions_panel)
        delete_btn.setIcon(QIcon(":/icons/delete-20.png"))
        delete_btn.setIconSize(QSize(20, 20))
        delete_btn.setFlat(True)
        delete_btn.setToolTip("Удалить документ")
        delete_btn.setDisabled(True)
        delete_btn.clicked.connect(self.deleteRow)

        a_layout.addWidget(insert_btn)
        a_layout.addWidget(edit_btn)
        a_layout.addWidget(delete_btn)

        filter_panel = QFrame(topline)
        f_layout = QHBoxLayout(filter_panel)
        f_layout.setAlignment(Qt.AlignRight)

        docfilter_lineedit = QLineEdit(filter_panel)
        docfilter_lineedit.setPlaceholderText("Фильтр по единице хранения...")
        docfilter_lineedit.setMaximumWidth(300)
        docfilter_lineedit.setDisabled(True)
        docfilter_lineedit.textChanged.connect(self.filter)

        clearfilter_btn = QPushButton(filter_panel)
        clearfilter_btn.setIcon(QIcon(":/icons/clear-filter-16.png"))
        clearfilter_btn.setToolTip("Сбросить фильтр")
        clearfilter_btn.setMaximumWidth(30)
        clearfilter_btn.setDisabled(True)
        clearfilter_btn.clicked.connect(self.clearFilter)

        f_layout.addWidget(docfilter_lineedit)
        f_layout.addWidget(clearfilter_btn)

        topline_layout.addWidget(actions_panel)
        topline_layout.addWidget(filter_panel)

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

        v_layout.addWidget(topline)
        v_layout.addWidget(tree_view)

        self.insert_btn = insert_btn
        self.edit_btn = edit_btn
        self.delete_btn = delete_btn
        self.docfilter_lineedit = docfilter_lineedit
        self.clearfilter_btn = clearfilter_btn
        self.tree_view = tree_view

        self.setMainWidget(main)

    def loadData(self, index):

        church_id = index.internalPointer().uid()

        doc_model = DocModel()
        doc_model.setChurchId(church_id)
        doc_model.refresh()

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(doc_model)

        self.model = proxy_model

        self.tree_view.setModel(proxy_model)

        self.tree_view.setColumnWidth(0, 50)
        self.tree_view.setColumnWidth(1, 110)
        self.tree_view.hideColumn(2)
        self.tree_view.hideColumn(3)
        self.tree_view.hideColumn(4)
        self.tree_view.setColumnWidth(5, 200)
        self.tree_view.hideColumn(6)
        self.tree_view.hideColumn(7)
        self.tree_view.hideColumn(8)
        self.tree_view.setColumnWidth(9, 55)
        self.tree_view.setColumnWidth(10, 150)
        self.tree_view.setColumnWidth(11, 200)

        self.docfilter_lineedit.setDisabled(False)
        self.insert_btn.setDisabled(False)
        self.edit_btn.setDisabled(False)
        self.delete_btn.setDisabled(False)

    def filter(self, text):
        self.clearfilter_btn.setDisabled((len(text) == 0))

        self.tree_view.expandAll()

        self.model.setRecursiveFilteringEnabled(True)
        self.model.setFilterRegExp(
            QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))

        self.model.setFilterKeyColumn(5)

    def clearFilter(self):
        if len(self.docfilter_lineedit.text()) > 0:
            self.docfilter_lineedit.setText("")
            self.clearfilter_btn.setDisabled(True)

            self.model.invalidateFilter()

    def insertRow(self):
        pass

    def editRow(self):
        pass

    def deleteRow(self):
        pass
