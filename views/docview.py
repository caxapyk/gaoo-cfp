from PyQt5.Qt import Qt, QCursor, QRegExp
from PyQt5.QtCore import (QModelIndex, QItemSelection,
                          QItemSelectionModel, QSortFilterProxyModel, QSize, QModelIndex)
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
        self.model = None

        # main layout
        main = QFrame()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(85)
        main.setSizePolicy(sizePolicy)

        v_layout = QVBoxLayout(main)
        v_layout.setContentsMargins(2, 0, 0, 0)
        v_layout.setSpacing(0)

        tree_view = QTreeView(main)
        tree_view.setSortingEnabled(True)
        tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        tree_view.customContextMenuRequested.connect(
            self.showContextMenu)

        v_layout.addWidget(tree_view)

        self.c_menu = QMenu(tree_view)
        self.tree_view = tree_view

        self.setMainWidget(main)

    def loadData(self, index):

        church_id = index.internalPointer().uid()

        doc_model = DocModel()
        #doc_model.setChurchId(church_id)
        doc_model.setFilter("church_id=%s" % church_id)
        doc_model.select()

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(doc_model)

        self.model = proxy_model

        self.tree_view.setModel(proxy_model)

        #self.tree_view.setColumnWidth(0, 50)
        #self.tree_view.setColumnWidth(1, 110)
        #self.tree_view.hideColumn(2)
        #self.tree_view.hideColumn(3)
        #self.tree_view.hideColumn(4)
        #self.tree_view.setColumnWidth(5, 200)
        #self.tree_view.hideColumn(6)
        #self.tree_view.hideColumn(7)
        #self.tree_view.hideColumn(8)
        #self.tree_view.setColumnWidth(9, 55)
        #self.tree_view.setColumnWidth(10, 150)
        #self.tree_view.setColumnWidth(11, 200)
        #self.tree_view.hideColumn(12)

    def currentIndex(self):
        if self.tree_view.selectedIndexes():
            proxy_index = self.tree_view.currentIndex()
            index = self.model.mapToSource(proxy_index)

            return index

        return QModelIndex()


    def showContextMenu(self, point):
        index = self.tree_view.indexAt(point)

        self.c_menu.clear()

        if index.isValid():
            self.c_menu.addAction(self.parent.action_edit)
            self.c_menu.addAction(self.parent.action_delete)
        else:
            self.c_menu.addAction(self.parent.action_create)

        self.c_menu.exec(
            self.tree_view.viewport().mapToGlobal(point))

    def filter(self, text):
        self.parent.clearfilter_btn.setDisabled((len(text) == 0))

        self.tree_view.expandAll()

        self.model.setRecursiveFilteringEnabled(True)
        self.model.setFilterRegExp(
            QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))

        self.model.setFilterKeyColumn(5)

    def clearFilter(self):
        if len(self.parent.filter_line.text()) > 0:
            self.parent.filter_line.setText("")
            self.parent.clearfilter_btn.setDisabled(True)

            self.model.invalidateFilter()

    def insertRow(self):
        print("insertRow")

    def editRow(self):
        pass

    def deleteRow(self):
        pass
