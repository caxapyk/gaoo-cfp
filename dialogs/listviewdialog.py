from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QMessageBox)
from PyQt5.QtGui import QIcon, QBrush
from PyQt5.uic import loadUi
from PyQt5.QtCore import (QModelIndex, QItemSelection, QItemSelectionModel)


class ListViewDialog(QDialog):

    __model = None

    def __init__(self):
        super(ListViewDialog, self).__init__()
        ui = loadUi("ui/listview_dialog.ui", self)

        ui.pushButton_create.clicked.connect(self.insertAction)
        ui.pushButton_remove.clicked.connect(self.removeAction)
        ui.pushButton_edit.clicked.connect(self.editAction)

        ui.listView_doctype.pressed.connect(self.setButtonsState)

        self.ui = ui
        self.setButtonsState()

    def setModel(self, model):
        self.__model = model
        self.__model.select()

        model.dataChanged.connect(self.dataChangedAction)

        self.ui.listView_doctype.setModel(model)
        self.ui.listView_doctype.setModelColumn(1)

    def setModelColumn(self, column):
        self.ui.listView_doctype.setModelColumn(column)

    def insertAction(self):
        total = self.__model.rowCount()

        self.__model.insertRow(total)

        index = self.__model.index(total, 1, QModelIndex())
        self.__model.setData(index, "Новая запись", Qt.EditRole)

        self.__model.submit()

        selection = QItemSelection()
        selection.select(index, index)
        self.ui.listView_doctype.selectionModel().select(
            selection, QItemSelectionModel.Rows | QItemSelectionModel.Select | QItemSelectionModel.Clear)

        self.setButtonsState()

        # edit new item
        self.ui.listView_doctype.edit(index)

    def removeAction(self):
        idx = self.listView_doctype.selectedIndexes()
        if idx:
            result = QMessageBox().critical(
                self, "Удаление объекта",
                "Вы уверены что хотите удалить \"%s\"?" % idx[0].data(),
                QMessageBox.No | QMessageBox.Yes)

            if result == QMessageBox.Yes:
                self.__model.removeRows(idx[0].row(), 1, QModelIndex())
                self.__model.select()

                self.setButtonsState()

    def editAction(self):
        index = self.listView_doctype.selectedIndexes()[0]
        self.ui.listView_doctype.edit(index)

    def dataChangedAction(self):
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setDisabled(True)

    def setButtonsState(self):
        self.ui.pushButton_remove.setDisabled(True)
        self.ui.pushButton_edit.setDisabled(True)

        idx = self.listView_doctype.selectedIndexes()

        if idx:
            default_item = isinstance(idx[0].data(Qt.ForegroundRole), QBrush)
            self.ui.pushButton_remove.setDisabled(default_item)
            self.ui.pushButton_edit.setDisabled(default_item)
