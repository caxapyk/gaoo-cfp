from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QTreeView, QMessageBox)
from views import (View, TreeItemDelegate)
from widgets import TreeSortFilter


class TreeBaseView(View):
    def __init__(self, parent):
        super(TreeBaseView, self).__init__(parent)

        self.parent = parent

        # Build UI
        self.main_widget = QFrame()
        v_layout = QVBoxLayout(self.main_widget)
        v_layout.setContentsMargins(2, 0, 0, 0)
        v_layout.setSpacing(0)

        self.tree_view = QTreeView(self.main_widget)
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)

        tree_view_delegate = TreeItemDelegate()
        tree_view_delegate.closeEditor.connect(self.onEditorClosed)

        self.tree_view.setItemDelegateForColumn(0, tree_view_delegate)

        # tree filter
        self.tree_filter = TreeSortFilter()
        self.tree_filter.setWidget(self.tree_view)

        v_layout.addWidget(self.tree_filter)
        v_layout.addWidget(self.tree_view)

        # set main ad default widget
        self.setMainWidget(self.main_widget)

    def treeView(self):
        return self.tree_view

    def treeFilter(self):
        return self.tree_filter

    def onEditorClosed(self):
        if self.tree_filter.isSorted():
            self.tree_filter.sort(self.model.sortOrder())

    def insertRow(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            if self.tree_filter.isFiltered():
                # store source model index to reload after clearFilter()
                # because index of proxy model will be changed
                m_index = self.model.mapToSource(index)
                self.tree_filter.clearAllFilters()
                # restore index
                index = self.model.mapFromSource(m_index)
                self.tree_view.setCurrentIndex(index)

            # !important: branch must be expanded before new row inserted
            self.tree_view.setExpanded(index, True)

            if not self.model.insertRows(0, 1, index):
                QMessageBox().critical(
                    self.tree_view, "Создание объекта",
                    "Не удалось создать объект!\nВозможно у Вас недостаточно привилегий.", QMessageBox.Ok)
                return False
        else:
            if not self.model.insertRows(0, 1, QModelIndex()):
                QMessageBox().critical(
                    self.tree_view, "Создание объекта",
                    "Не удалось создать объект!\nВозможно у Вас недостаточно привилегий.", QMessageBox.Ok)
                return False

        # map underlying model index
        source_parent = self.model.mapToSource(index)
        source_index = self.model.sourceModel().index(
            self.model.sourceModel().rowCount(source_parent) - 1, 0, source_parent)

        # map back to proxy model
        index = self.model.mapFromSource(source_index)

        self.tree_view.setCurrentIndex(index)

        # edit new item
        self.tree_view.edit(index)

    def editRow(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            self.tree_view.edit(index)

    def removeRow(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            result = QMessageBox().critical(
                self.parent, "Удаление объекта",
                "Вы уверены что хотите удалить \"%s\"?" % index.data(),
                QMessageBox.No | QMessageBox.Yes)

            if result == QMessageBox.Yes:
                if not self.model.removeRows(index.row(), 1, index.parent()):
                    QMessageBox().critical(self.tree_view, "Удаление объекта",
                                           "Не удалось удалить объект!\n\nПроверьте нет ли связей с другими объектами или возможно у Вас недостаточно привилегий.",
                                           QMessageBox.Ok)
