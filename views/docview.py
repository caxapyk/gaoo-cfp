from PyQt5.Qt import Qt, QCursor, QRegExp
from PyQt5.QtCore import (QModelIndex, QItemSelection,
                          QItemSelectionModel, QSortFilterProxyModel,
                          QSize, QModelIndex, QItemSelectionModel)
from PyQt5.QtWidgets import (QWidget, QAbstractItemView, QFrame, QSizePolicy,
                             QHBoxLayout, QVBoxLayout, QLineEdit,
                             QButtonGroup, QPushButton, QTreeView, QMenu,
                             QAction, QMessageBox)
from PyQt5.QtGui import (QIcon, QPixmap, QKeySequence)
from PyQt5.QtSql import QSqlRelationalTableModel
from PyQt5.QtCore import QModelIndex
from models import DocModel
from dialogs import (DocFormDialog, DocViewDialog)
from views import View
import time


class DocView(View):
    def __init__(self, parent):
        super(DocView, self).__init__(parent)

        self.parent = parent

        # main layout
        main = QFrame()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(85)
        main.setSizePolicy(sizePolicy)

        v_layout = QVBoxLayout(main)
        v_layout.setContentsMargins(2, 0, 0, 0)
        v_layout.setSpacing(0)

        self.tree_view = QTreeView(main)
        self.tree_view.setSortingEnabled(True)
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(
            self.showContextMenu)
        self.tree_view.doubleClicked.connect(self.viewDocDialog)

        v_layout.addWidget(self.tree_view)

        # context menu
        self.c_menu = QMenu(self.tree_view)

        self.doc_model = None
        self.model = None

        self.setMainWidget(main)

    def loadData(self, church_id):
        self.church_id = church_id

        self.parent.statusBar().showMessage("Загрука данных...", 1000)

        self.doc_model = DocModel()
        self.doc_model.setEditStrategy(QSqlRelationalTableModel.OnRowChange)
        self.doc_model.setFilter("cfp_doc.church_id=%s" % self.church_id)
        self.doc_model.setChurch(church_id)
        self.doc_model.select()

        self.parent.statusBar().showMessage("Загружено документов: %s" %
                                            self.doc_model.query().size())

        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(self.doc_model)
        self.model.setDynamicSortFilter(False)

        self.sel_model = QItemSelectionModel()
        self.sel_model.setModel(self.model)
        self.sel_model.currentChanged.connect(self.docSelected)
        self.sel_model.currentChanged.emit(QModelIndex(), QModelIndex())

        self.tree_view.setModel(self.model)
        self.tree_view.setSelectionModel(self.sel_model)
        # disable default sorting
        self.tree_view.sortByColumn(-1, Qt.AscendingOrder)

        self.tree_view.hideColumn(0)
        self.tree_view.hideColumn(1)
        self.tree_view.hideColumn(2)
        self.tree_view.hideColumn(3)
        self.tree_view.hideColumn(4)
        self.tree_view.hideColumn(5)
        self.tree_view.hideColumn(6)
        self.tree_view.hideColumn(7)
        self.tree_view.resizeColumnToContents(8)
        self.tree_view.setColumnWidth(9, 150)
        self.tree_view.setColumnWidth(10, 200)
        self.tree_view.setColumnWidth(11, 100)
        self.tree_view.setColumnWidth(12, 150)
        self.tree_view.setColumnWidth(13, 150)
        self.tree_view.resizeColumnToContents(14)

        self.parent.doc_create.setDisabled(False)
        self.parent.doc_refresh.setDisabled(False)
        self.parent.filter_panel.setDisabled(False)

    def showContextMenu(self, point):
        index = self.tree_view.indexAt(point)

        self.c_menu.clear()

        if index.isValid():
            self.c_menu.addAction(self.parent.doc_update)
            self.c_menu.addAction(self.parent.doc_remove)
        else:
            self.c_menu.addAction(self.parent.doc_create)
            self.c_menu.addSeparator()
            self.c_menu.addAction(self.parent.doc_refresh)

        self.c_menu.exec(
            self.tree_view.viewport().mapToGlobal(point))

    def filter(self, text):
        self.parent.clearfilter_btn.setDisabled((len(text) == 0))

        self.tree_view.expandAll()

        self.model.setFilterKeyColumn(10)
        self.model.setFilterRegExp(
            QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))

    def clearFilter(self):
        if len(self.parent.filter_lineedit.text()) > 0:
            self.parent.filter_lineedit.setText("")
            self.parent.clearfilter_btn.setDisabled(True)

            self.model.invalidateFilter()

    def removeDoc(self):
        index = self.tree_view.currentIndex()
        if index:
            result = QMessageBox().critical(
                self.parent, "Удаление документа",
                "Вы уверены что хотите удалить этот документ?",
                QMessageBox.No | QMessageBox.Yes)

            if result == QMessageBox.Yes:
                self.doc_model.clearCache(index.row())
                self.tree_view.setRowHidden(
                    index.row(), QModelIndex(), True)
                if self.model.removeRow(index.row()):
                    self.tree_view.setCurrentIndex(QModelIndex())
                else:
                    QMessageBox().critical(
                        self.tree_view, "Удаление документа",
                        "Не удалось удалить документ!", QMessageBox.Ok)

    def viewDocDialog(self):
        proxy_index = self.tree_view.currentIndex()
        index = self.model.mapToSource(proxy_index)

        docview_dialog = DocViewDialog(self.parent, self.doc_model, index.row())
        res = docview_dialog.exec()

    def editDocDialog(self):
        proxy_index = self.tree_view.currentIndex()
        index = self.model.mapToSource(proxy_index)

        docform_dialog = DocFormDialog(self.parent, self.doc_model, index.row())
        res = docform_dialog.exec()

    def createDocDialog(self):
        self.tree_view.setCurrentIndex(QModelIndex())

        docform_dialog = DocFormDialog(self.parent, self.doc_model)
        res = docform_dialog.exec()

        if res == DocFormDialog.Accepted:
            self.model.sort(8)
            index = self.doc_model.index(self.doc_model.rowCount() - 1, 0)
            proxy_index = self.model.mapFromSource(index)

            self.tree_view.setCurrentIndex(proxy_index)

            # self.model.setDynamicSortFilter(True)

    def docSelected(self, index):
        self.parent.doc_update.setDisabled(not index.isValid())
        self.parent.doc_remove.setDisabled(not index.isValid())

    def refreshDocs(self):
        self.loadData(self.church_id)
