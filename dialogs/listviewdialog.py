from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QMessageBox)
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import (QModelIndex, QItemSelection, QItemSelectionModel)


class ListViewDialog(QDialog):

    __model = None

    def __init__(self):
        super(ListViewDialog, self).__init__()
        ui = loadUi("ui/listview_dialog.ui", self)
        ui.setWindowIcon(QIcon(":/icons/church-16.png"))

        ui.pushButton_create.clicked.connect(self.createAction)
        ui.pushButton_remove.clicked.connect(self.removeAction)
        ui.pushButton_edit.clicked.connect(self.editAction)

        self.ui = ui

        self.show()

    def setModel(self, model):
        self.__model = model
        self.__model.select()

        model.dataChanged.connect(self.dataChangedAction)

        self.ui.listView_doctype.setModel(model)
        self.ui.listView_doctype.setModelColumn(1)

    def setModelColumn(self, column):
        self.ui.listView_doctype.setModelColumn(column)

    def createAction(self):
        total = self.__model.rowCount()

        self.__model.insertRow(total)

        index = self.__model.index(total, 1, QModelIndex())
        self.__model.setData(index, "Новая запись")

        self.__model.submit()

        selection = QItemSelection()
        selection.select(index, index)
        self.ui.listView_doctype.selectionModel().select(
            selection, QItemSelectionModel.Rows | QItemSelectionModel.Select | QItemSelectionModel.Clear)

        # edit new item
        self.ui.listView_doctype.edit(index)

    def removeAction(self):
        index = self.listView_doctype.selectedIndexes()
        if index:
            result = QMessageBox().critical(
                self, "Удаление объекта",
                "Вы уверены что хотите удалить \"%s\"?" % index[0].data(),
                QMessageBox.No | QMessageBox.Yes)

            if result == QMessageBox.Yes:
                self.__model.removeRows(index[0].row(), 1, QModelIndex())
                self.__model.select()

    def editAction(self):
        index = self.listView_doctype.currentIndex()
        self.ui.listView_doctype.edit(index)

    def dataChangedAction(self):
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setDisabled(True)
