from PyQt5.Qt import Qt, QRegExp, QCursor
from PyQt5.QtCore import (QModelIndex, pyqtSignal)
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMenu, QMessageBox, QTreeView)
from views import (View, TreeItemDelegate)


class TreeBaseView(View):

    treeSorted = pyqtSignal(int)
    treeFilterCleared = pyqtSignal()
    treeSortCleared = pyqtSignal()
    #contextMenuBeforeOpen = pyqtSignal(QModelIndex)

    def __init__(self, parent=None):
        super(TreeBaseView, self).__init__(parent)

        self.parent = parent
        # Build UI
        self.tree_view = QTreeView()
        self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)

        tree_view_delegate = TreeItemDelegate()
        tree_view_delegate.closeEditor.connect(self.onEditorClosed)

        self.tree_view.setItemDelegateForColumn(0, tree_view_delegate)

        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(
            self.showContextMenu)

        self.__isFiltered__ = False
        self.__isSorted__ = False

        self.model = None

        self.context_menu = QMenu(self.tree_view)
        self.default_actions = []

        self.setMainWidget(self.tree_view)

    #def treeView(self):
    #    return self.tree_view

    def setModel(self, model):
        self.model = model
        self.tree_view.setModel(self.model)

    def refreshModel(self):
        self.model.sourceModel().select()
        self.parent.statusBar().showMessage("Загрука данных...", 500)

    #def contextMenu(self):
    #    return self.context_menu

    def onEditorClosed(self):
        if self.isSorted():
            self.sort(self.model().sortOrder())

    #
    # CRUD
    #
    def insertRow(self):
        index = self.tree_view.currentIndex()
        if index.isValid():
            if self.isFiltered():
                # store source model index to reload after clearAllFilters()
                # because index of proxy model will be changed
                m_index = self.model.mapToSource(index)
                self.clearAllFilters()
                # restore index
                index = self.model.mapFromSource(m_index)
                self.tree_view.setCurrentIndex(index)

            # !important: branch must be expanded before new row inserted
            self.tree_view.setExpanded(index, True)

            if not self.model.insertRows(0, 1, index):
                QMessageBox().critical(
                    self.parent, "Создание объекта",
                    "Не удалось создать объект!\nВозможно у Вас недостаточно привилегий.", QMessageBox.Ok)
                return False
        else:
            self.clearAllFilters()
            if not self.model.insertRows(0, 1, QModelIndex()):
                QMessageBox().critical(
                    self.parent, "Создание объекта",
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
                    QMessageBox().critical(self.parent, "Удаление объекта",
                                           "Не удалось удалить объект!\n\nПроверьте нет ли связей с другими объектами или возможно у Вас недостаточно привилегий.",
                                           QMessageBox.Ok)
    #
    # CONTEXT MENU
    #

    def isEndPointReached(self, index):
        return False

    def showContextMenu(self, point):
        index = self.tree_view.indexAt(point)

        #self.contextMenuBeforeOpen.emit(index)

        self.default_actions = []

        #source_index = self.model.mapToSource(index)
        #model_count = len(self.model.sourceModel().models())
        #level = source_index.internalPointer().level()

        # check model is last in models list, disable create new item
        # only if model is multimodel
        #if (model_count == 1) or (level < (model_count - 1)):
        if not self.isEndPointReached(index):
            self.default_actions.append((":/icons/folder-new-16.png", "Создать объект",
                            self.insertRow))

        if index.isValid():
            item_actions = [
                (":/icons/rename-16.png", "Переименовать", self.editRow),
                (":/icons/delete-16.png", "Удалить", self.removeRow),
                "separator"
            ]
            self.default_actions.extend(item_actions)

        sort_actions = [
            "separator",
            (":/icons/sort-az-16.png", "Сортировка по возрастанию",
                lambda: self.sort(0)),
            (":/icons/sort-za-16.png", "Сортировка по убыванию",
                lambda: self.sort(1)),
            (None, "Очистить сортировку",
                lambda: self.sort(3)),
            "separator",
            (None, "Сбросить все фильтры", self.clearAllFilters),
            "separator"
        ]
        self.default_actions.extend(sort_actions)

        self.default_actions.append((":/icons/refresh-16.png",
                        "Обновить", self.refreshModel))

        for action in self.default_actions:
            if action == "separator":
                self.context_menu.addSeparator()
            else:
                _action = self.context_menu.addAction(action[1])
                _action.triggered.connect(action[2])
                # set icon
                if action[0]:
                    _action.setIcon(QIcon(action[0]))

        if index.isValid():
            self.context_menu.exec_(
                self.tree_view.viewport().mapToGlobal(point))
        else:
            self.tree_view.setCurrentIndex(QModelIndex())
            self.context_menu.exec_(QCursor.pos())

        self.context_menu.clear()

    #
    # SORT AND FILTER
    #
    def filter(self, text):
        self.tree_view.expandAll()

        self.model.setRecursiveFilteringEnabled(True)
        self.model.setFilterRegExp(
            QRegExp(text, Qt.CaseInsensitive, QRegExp.FixedString))

        self.__isFiltered__ = True

    def isFiltered(self):
        return self.__isFiltered__

    def clearFilter(self):
        self.treeFilterCleared.emit()

        self.model.invalidateFilter()

        self.__isFiltered__ = False

    def sort(self, order):
        current_sort = self.model.sortOrder()

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

        self.model.sort(0, sort_order)

        self.__isSorted__ = True

        return True

    def isSorted(self):
        return self.__isSorted__

    def clearSort(self):
        self.treeSortCleared.emit()

        self.model.sort(-1)
        self.__isSorted__ = False

    def clearAllFilters(self):
        self.clearFilter()
        self.clearSort()
