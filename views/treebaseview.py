from PyQt5.Qt import Qt, QCursor
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QFrame, QVBoxLayout, QTreeView, QMenu, QMessageBox)
from views import View


class TreeBaseView(View):
    def __init__(self, parent):
        super(TreeBaseView, self).__init__(parent)

        self.parent = parent
        self.tree_view = None
        self.tree_filter = None

        self.context_menu = QMenu(self.tree_view)

    def setTreeView(self, tree_view):
        self.tree_view = tree_view

    def setTreeFilter(self, tree_filter):
        self.tree_filter = tree_filter

    def isFilterSet(self):
        return (self.tree_filter is not None)

    def contextMenu(self):
        return self.context_menu

    def onEditorClosed(self):
        if self.isFilterSet() & self.tree_filter.isSorted():
            self.tree_filter.sort(self.model.sortOrder())

    def insertRow(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            if self.isFilterSet() & self.tree_filter.isFiltered():
                # store source model index to reload after clearAllFilters()
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

    def showContextMenu(self, point):
        index = self.tree_view.indexAt(point)

        actions = []

        if self.isFilterSet():
            sort_actions = [
                ("", "Сортировка по возрастанию", lambda: self.tree_filter.sort(0)),
                ("", "Сортировка по убыванию", lambda: self.tree_filter.sort(1)),
                ("", "Очистить сортировку", lambda: self.tree_filter.sort(3)),
                "separator"
            ]
            actions.extend(sort_actions)

        if index.isValid():
            source_index = self.model.mapToSource(index)
            sql_model = source_index.internalPointer()

            display_name = sql_model.model().displayName()

            crud_actions = [
                (":/icons/folder-new-16.png", "Создать %s" % display_name,
                    self.insertRow),
                (":/icons/rename-16.png", "Переименовать", self.editRow),
                (":/icons/delete-16.png", "Удалить", self.removeRow),
                "separator"
            ]
            actions.extend(crud_actions)

        else:
            actions.insert(0, ("", "Создать группировку", self.insertRow))
            actions.insert(1, "separator")

        for action in actions:
            if action == "separator":
                self.context_menu.addSeparator()
            else:
                _action = self.context_menu.addAction(action[1])
                _action.setIcon(QIcon(action[0]))
                _action.triggered.connect(action[2])

        if index.isValid():
            self.context_menu.exec_(
                self.tree_view.viewport().mapToGlobal(point))
        else:
            self.tree_view.setCurrentIndex(QModelIndex())
            self.context_menu.exec_(QCursor.pos())

        self.context_menu.clear()

