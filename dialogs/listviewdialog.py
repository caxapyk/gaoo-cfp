from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QMessageBox)
from PyQt5.uic import loadUi
from PyQt5.QtCore import (QModelIndex, QItemSelection, QItemSelectionModel)
from models import SqlListProxyModel


class ListViewDialog(QDialog):

    def __init__(self):
        super(ListViewDialog, self).__init__()
        ui = loadUi("ui/listview_dialog.ui", self)

        ui.pushButton_create.clicked.connect(self.insertAction)
        ui.pushButton_remove.clicked.connect(self.removeAction)
        ui.pushButton_edit.clicked.connect(self.editAction)
        ui.listView_doctype.pressed.connect(self.setButtonState)

        self.model = None
        self.ui = ui

        self.setButtonState()

    def setModel(self, model):
        self.model = model
        self.model.dataChanged.connect(self.dataChangedAction)

        self.ui.listView_doctype.setModel(self.model)
        self.ui.listView_doctype.setModelColumn(1)

    def insertAction(self):
        total = self.model.rowCount()
        column = self.listView_doctype.modelColumn()

        self.model.insertRow(total)

        index = self.model.index(total, column, QModelIndex())
        self.model.setData(index, "Новая запись", Qt.EditRole)

        self.model.submit()

        selection = QItemSelection()
        selection.select(index, index)
        self.ui.listView_doctype.selectionModel().select(
            selection, QItemSelectionModel.Rows | QItemSelectionModel.Select | QItemSelectionModel.Clear)

        self.setButtonState()

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
                column = self.listView_doctype.modelColumn()
                self.model.removeRows(idx[0].row(), column, QModelIndex())
                self.model.sourceModel().select()

                self.setButtonState()

    def editAction(self):
        idx = self.listView_doctype.selectedIndexes()
        if idx:
            self.ui.listView_doctype.edit(idx[0])

    def dataChangedAction(self):
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setDisabled(True)

    def setButtonState(self):
        isSelected = len(self.listView_doctype.selectedIndexes()) > 0

        self.ui.pushButton_remove.setDisabled(not isSelected)
        self.ui.pushButton_edit.setDisabled(not isSelected)
