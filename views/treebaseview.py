from PyQt5.Qt import Qt, QRegExp, QCursor
from PyQt5.QtCore import (QObject, QModelIndex, pyqtSignal)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QMenu, QMessageBox, QTreeView)
from views import (View, TreeItemDelegate)


class TreeBaseView(QTreeView):

    treeSorted = pyqtSignal(int)
    treeFilterCleared = pyqtSignal()
    treeSortCleared = pyqtSignal()

    def __init__(self, parent=None):
        super(TreeBaseView, self).__init__(parent)

        self.parent = parent
        # Build UI
        #self = QTreeView()
        self.setEditTriggers(QTreeView.NoEditTriggers)

        tree_view_delegate = TreeItemDelegate()
        tree_view_delegate.closeEditor.connect(self.onEditorClosed)

        self.setItemDelegateForColumn(0, tree_view_delegate)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(
            self.showContextMenu)

        self.__isFiltered__ = False
        self.__isSorted__ = False

        self.context_menu = QMenu(self)

    def contextMenu(self):
        return self.context_menu

    def onEditorClosed(self):
        if self.isSorted():
            self.sort(self.model().sortOrder())

    #
    # CRUD
    #

    def insertRow(self):
        index = self.currentIndex()
        if index.isValid():
            if self.isFiltered():
                # store source model index to reload after clearAllFilters()
                # because index of proxy model will be changed
                m_index = self.model().mapToSource(index)
                self.clearAllFilters()
                # restore index
                index = self.model().mapFromSource(m_index)
                self.setCurrentIndex(index)

            # !important: branch must be expanded before new row inserted
            self.setExpanded(index, True)

            if not self.model().insertRows(0, 1, index):
                QMessageBox().critical(
                    self, "Создание объекта",
                    "Не удалось создать объект!\nВозможно у Вас недостаточно привилегий.", QMessageBox.Ok)
                return False
        else:
            if not self.model().insertRows(0, 1, QModelIndex()):
                QMessageBox().critical(
                    self, "Создание объекта",
                    "Не удалось создать объект!\nВозможно у Вас недостаточно привилегий.", QMessageBox.Ok)
                return False

        # map underlying model index
        source_parent = self.model().mapToSource(index)
        source_index = self.model().sourceModel().index(
            self.model().sourceModel().rowCount(source_parent) - 1, 0, source_parent)

        # map back to proxy model
        index = self.model().mapFromSource(source_index)

        self.setCurrentIndex(index)

        # edit new item
        self.edit(index)

    def editRow(self):
        index = self.currentIndex()
        if index.isValid():
            self.edit(index)

    def removeRow(self):
        index = self.currentIndex()
        if index.isValid():
            result = QMessageBox().critical(
                self.parent, "Удаление объекта",
                "Вы уверены что хотите удалить \"%s\"?" % index.data(),
                QMessageBox.No | QMessageBox.Yes)

            if result == QMessageBox.Yes:
                if not self.model().removeRows(index.row(), 1, index.parent()):
                    QMessageBox().critical(self, "Удаление объекта",
                                           "Не удалось удалить объект!\n\nПроверьте нет ли связей с другими объектами или возможно у Вас недостаточно привилегий.",
                                           QMessageBox.Ok)
    #
    # CONTEXT MENU
    #

    def showContextMenu(self, point):
        index = self.indexAt(point)

        actions = []

        sort_actions = [
            (":/icons/sort-az-16.png", "Сортировка по возрастанию",
                lambda: self.sort(0)),
            (":/icons/sort-za-16.png", "Сортировка по убыванию",
                lambda: self.sort(1)),
            (":/icons/delete-16.png", "Очистить сортировку",
                lambda: self.sort(3)),
            "separator"
        ]
        actions.extend(sort_actions)

        if index.isValid():
            source_index = self.model().mapToSource(index)
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
                self.viewport().mapToGlobal(point))
        else:
            self.setCurrentIndex(QModelIndex())
            self.context_menu.exec_(QCursor.pos())

        self.context_menu.clear()

    #
    # SORT AND FILTER
    #

    def filter(self, text):
        self.expandAll()
        self.clearSort()

        self.model().setRecursiveFilteringEnabled(True)
        self.model().setFilterRegExp(
            QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))

        self.__isFiltered__ = True

    def isFiltered(self):
        return self.__isFiltered__

    def clearFilter(self):
        self.treeFilterCleared.emit()

        self.model().invalidateFilter()

        self.__isFiltered__ = False

    def sort(self, order):
        current_sort = self.model().sortOrder()

        self.treeSorted.emit(order)

        if self.isSorted() and current_sort == order:
            self.clearSort()
            return False

        if order == 0:
            sort_order = Qt.AscendingOrder
        elif order == 1:
            sort_order = Qt.DescendingOrder
        else:
            self.clearSort()
            return False

        self.model().sort(0, sort_order)

        self.__isSorted__ = True

        return True

    def isSorted(self):
        return self.__isSorted__

    def clearSort(self):
        self.treeSortCleared.emit()

        self.model().sort(-1)
        self.__isSorted__ = False

    def clearAllFilters(self):
        self.clearFilter()
        self.clearSort()
