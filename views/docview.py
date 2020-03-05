from PyQt5.Qt import Qt
from PyQt5.QtCore import (QModelIndex, QItemSelectionModel)
from PyQt5.QtWidgets import (QWidget, QFrame, QSizePolicy,
                             QHBoxLayout, QVBoxLayout,
                             QMessageBox)
from PyQt5.QtSql import QSqlRelationalTableModel
from models import (DocModel, DocProxyModel)
from dialogs import (DocFormDialog, DocViewDialog)
from views import TreeBaseView
from widgets import TreeSortFilter


class DocView(TreeBaseView):
    def __init__(self, parent):
        super(DocView, self).__init__(parent)

        self.parent = parent
        self.__model_loaded__ = False
        self.model = None

        # self.main_widget layout
        self.main_widget = QFrame()
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(85)
        self.main_widget.setSizePolicy(sizePolicy)

        v_layout = QVBoxLayout(self.main_widget)
        v_layout.setContentsMargins(2, 0, 0, 0)
        v_layout.setSpacing(0)

        self.tree_view.setSortingEnabled(True)
        self.tree_view.doubleClicked.connect(self.openDocDialog)

        v_layout.addWidget(self.tree_view)

        # Toolbar actions
        self.parent.doc_create.triggered.connect(self.insertRow)
        self.parent.doc_update.triggered.connect(self.editRow)
        self.parent.doc_remove.triggered.connect(self.removeRow)
        self.parent.doc_refresh.triggered.connect(self.refreshModel)

        self.filter_panel = QWidget()
        self.filter_panel.setDisabled(True)
        f_layout = QHBoxLayout(self.filter_panel)
        f_layout.setContentsMargins(0, 0, 0, 0)
        f_layout.setAlignment(Qt.AlignRight)

        self.doc_filter = TreeSortFilter(self)
        self.doc_filter.setMode(TreeSortFilter.FilterMode)
        self.doc_filter.setFilterPlaceHolder("Фильтр по единице хранения...")
        self.doc_filter.setMaximumWidth(300)

        f_layout.addWidget(self.doc_filter)

        self.parent.toolbar.addWidget(self.filter_panel)

        self.setMainWidget(self.main_widget)

    def loadData(self, church_id):
        self.church_id = church_id

        # set models
        doc_model = DocModel()
        doc_model.setEditStrategy(QSqlRelationalTableModel.OnRowChange)
        doc_model.setFilter(
            "cfp_doc.church_id=%s" % self.church_id)
        doc_model.setChurch(church_id)

        res = doc_model.select()
        if res:
            self.model = DocProxyModel()
            self.model.setSourceModel(doc_model)

            # enable dynamic filtering
            self.model.setDynamicSortFilter(True)

            self.model.setFilterKeyColumn(12)

            self.sel_model = QItemSelectionModel()
            self.sel_model.setModel(self.model)
            self.sel_model.currentChanged.connect(self.docSelected)

            self.sel_model.currentChanged.emit(QModelIndex(), QModelIndex())

            # set model
            self.tree_view.setModel(self.model)
            self.tree_view.setSelectionModel(self.sel_model)

            for i in range(0, 9):
                self.tree_view.hideColumn(i)

            self.tree_view.resizeColumnToContents(9)
            self.tree_view.setColumnWidth(10, 250)
            self.tree_view.setColumnWidth(11, 150)
            self.tree_view.setColumnWidth(12, 200)
            self.tree_view.setColumnWidth(13, 125)
            self.tree_view.setColumnWidth(14, 150)
            self.tree_view.resizeColumnToContents(15)

            # disable default sorting
            self.tree_view.sortByColumn(-1, Qt.AscendingOrder)

            self.parent.doc_create.setDisabled(False)
            self.parent.doc_refresh.setDisabled(False)

            self.filter_panel.setDisabled(False)

            self.setModel(self.model)

            self.__model_loaded__ = True

            self.parent.statusBar().showMessage("Готово", 2000)

    def removeRow(self):
        index = self.tree_view.currentIndex()
        if index:
            result = QMessageBox().critical(
                self.parent, "Удаление документа",
                "Вы уверены что хотите удалить этот документ?",
                QMessageBox.No | QMessageBox.Yes)

            if result == QMessageBox.Yes:
                self.model.sourceModel().clearCache(index.row())
                self.tree_view.setRowHidden(
                    index.row(), QModelIndex(), True)
                if self.model.removeRow(index.row()):
                    self.tree_view.setCurrentIndex(QModelIndex())
                else:
                    self.tree_view.setRowHidden(
                        index.row(), QModelIndex(), False)
                    QMessageBox().critical(
                        self.tree_view, "Удаление документа",
                        "Не удалось удалить документ!", QMessageBox.Ok)

    def openDocDialog(self):
        proxy_index = self.tree_view.currentIndex()
        index = self.model.mapToSource(proxy_index)

        docview_dialog = DocViewDialog(
            self.parent, self.model.sourceModel(), index.row())
        docview_dialog.exec_()

    def editRow(self):
        proxy_index = self.tree_view.currentIndex()
        index = self.model.mapToSource(proxy_index)

        docform_dialog = DocFormDialog(
            self.parent, self.model.sourceModel(), index.row())
        docform_dialog.exec_()

    def insertRow(self):
        self.tree_view.setCurrentIndex(QModelIndex())

        docform_dialog = DocFormDialog(self.parent, self.model.sourceModel())
        res = docform_dialog.exec_()

        if res == DocFormDialog.Accepted:
            self.model.sort(-1)
            index = self.model.sourceModel().index(
                self.model.sourceModel().rowCount() - 1, 0)
            proxy_index = self.model.mapFromSource(index)

            self.tree_view.setCurrentIndex(proxy_index)

    def docSelected(self, index):
        self.parent.doc_update.setDisabled(not index.isValid())
        self.parent.doc_remove.setDisabled(not index.isValid())

    def refreshModel(self):
        self.clearAllFilters()
        self.loadData(self.church_id)

    def showContextMenu(self, point):
        if self.__model_loaded__:
            self.setDefaultItemName("документ")
            super().showContextMenu(point)
