from PyQt5.Qt import Qt, QCursor, QRegExp
from PyQt5.QtCore import (QModelIndex, QItemSelection,
                          QItemSelectionModel, QSortFilterProxyModel, QSize, QModelIndex)
from PyQt5.QtWidgets import (QWidget, QAbstractItemView, QFrame, QSizePolicy, QHBoxLayout, QVBoxLayout, QLineEdit,
                             QButtonGroup, QPushButton, QTreeView, QMenu, QAction, QMessageBox)
from PyQt5.QtGui import (QIcon, QPixmap, QKeySequence)
from PyQt5.QtSql import QSqlRelationalTableModel
from PyQt5.QtCore import QModelIndex
from views import (View, StorageUnitDelegate)
from dialogs import DocFormDialog
from models import DocModelPlain


class DocView(View):
    def __init__(self, parent):
        super(DocView, self).__init__()

        self.parent = parent
        self.model = None

        # view actions
        action_create = QAction("Новый документ")
        action_create.setIcon(QIcon(":/icons/doc-new-20.png"))
        action_create.setDisabled(True)
        action_create.setShortcut(QKeySequence.New)
        action_create.triggered.connect(self.createDocDialog)
        self.addViewAction("doc_create", action_create)

        action_update = QAction("Редактировать")
        action_update.setIcon(QIcon(":/icons/doc-edit-20.png"))
        action_update.setDisabled(True)
        action_update.triggered.connect(self.editDocDialog)
        self.addViewAction("doc_update", action_update)

        action_remove = QAction("Удалить")
        action_remove.setIcon(QIcon(":/icons/delete-20.png"))
        action_remove.setDisabled(True)
        action_remove.setShortcut(QKeySequence.Delete)
        action_remove.triggered.connect(self.removeDoc)
        self.addViewAction("doc_remove", action_remove)

        # toolbar widget
        filter_panel = QWidget()
        f_layout = QHBoxLayout(filter_panel)
        f_layout.setContentsMargins(0, 0, 0, 0)
        f_layout.setAlignment(Qt.AlignRight)

        filter_lineedit = QLineEdit(filter_panel)
        filter_lineedit.setPlaceholderText("Фильтр по единице хранения...")
        filter_lineedit.setMaximumWidth(300)
        filter_lineedit.setDisabled(True)
        filter_lineedit.textChanged.connect(self.filter)

        clearfilter_btn = QPushButton(filter_panel)
        clearfilter_btn.setIcon(QIcon(":/icons/clear-filter-16.png"))
        clearfilter_btn.setToolTip("Сбросить фильтр")
        clearfilter_btn.setMaximumWidth(30)
        clearfilter_btn.setDisabled(True)
        clearfilter_btn.clicked.connect(self.clearFilter)

        f_layout.addWidget(filter_lineedit)
        f_layout.addWidget(clearfilter_btn)

        self.addToolBarWidget("doc_filter", filter_panel)

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
        tree_view.pressed.connect(self.docSelected)

        v_layout.addWidget(tree_view)

        # context menu
        c_menu = QMenu(tree_view)

        self.tree_view = tree_view
        self.filter_lineedit = filter_lineedit
        self.clearfilter_btn = clearfilter_btn
        self.c_menu = c_menu

        self.setMainWidget(main)

    def loadData(self, index):

        church_id = index.internalPointer().uid()
        self.church_id = church_id

        doc_model = DocModelPlain()
        doc_model.setChurch(church_id)
        doc_model.refresh()

        proxy_model = QSortFilterProxyModel()
        proxy_model.setSourceModel(doc_model)

        self.model = proxy_model

        self.tree_view.setModel(proxy_model)

        #self.tree_view.setColumnWidth(0, 50)
        #self.tree_view.setColumnWidth(1, 110)
        #self.tree_view.hideColumn(2)
        #elf.tree_view.hideColumn(3)
        #elf.tree_view.hideColumn(4)
        #self.tree_view.setColumnWidth(5, 200)
        #self.tree_view.hideColumn(6)
        #self.tree_view.hideColumn(7)
        #self.tree_view.hideColumn(8)
        #self.tree_view.setColumnWidth(9, 55)
        #self.tree_view.setColumnWidth(10, 150)
        #self.tree_view.setColumnWidth(11, 200)

        self.vAction("doc_create").setDisabled(False)
        self.filter_lineedit.setDisabled(False)

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
            self.c_menu.addAction(self.vAction("doc_update"))
            self.c_menu.addAction(self.vAction("doc_remove"))
        else:
            self.c_menu.addAction(self.vAction("doc_create"))

        self.c_menu.exec(
            self.tree_view.viewport().mapToGlobal(point))

    def filter(self, text):
        self.clearfilter_btn.setDisabled((len(text) == 0))

        self.tree_view.expandAll()

        self.model.setRecursiveFilteringEnabled(True)
        self.model.setFilterRegExp(
            QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))

        self.model.setFilterKeyColumn(5)

    def clearFilter(self):
        if len(self.filter_lineedit.text()) > 0:
            self.filter_lineedit.setText("")
            self.clearfilter_btn.setDisabled(True)

            self.model.invalidateFilter()

    def insertRow(self):
        print("insertRow")

    def editRow(self):
        pass

    def removeDoc(self):
        proxy_index = self.tree_view.currentIndex()
        if proxy_index:
            result = QMessageBox().critical(
                self.parent, "Удаление документа",
                "Вы уверены что хотите удалить этот документ?",
                QMessageBox.No | QMessageBox.Yes)

            if result == QMessageBox.Yes:
                index = self.model.mapToSource(proxy_index)
                doc_id = index.model().record(index.row()).value("cfp_doc.id")
                print(doc_id)
                if self.model.sourceModel().remove(doc_id):
                    self.tree_view.setRowHidden(proxy_index.row(), QModelIndex(), True)
                else:    
                    QMessageBox().critical(self.tree_view, "Удаление документа",
                                           "Не удалось удалить документ!",
                                           QMessageBox.Ok)
        
    def editDocDialog(self):
        proxy_index = self.tree_view.currentIndex()
        index = self.model.mapToSource(proxy_index)

        

        docform_dialog = DocFormDialog(self.model.sourceModel(), index)
        res = docform_dialog.exec()

        if res == DocFormDialog.Accepted:
            self.model.sourceModel().refresh()

    def createDocDialog(self):
        docform_dialog = DocFormDialog(self.model.sourceModel())
        res = docform_dialog.exec()

        if res == DocFormDialog.Accepted:
            self.model.sourceModel().refresh()

    def docSelected(self):
        self.vAction("doc_update").setDisabled(False)
        self.vAction("doc_remove").setDisabled(False)
