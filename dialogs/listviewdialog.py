from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QMessageBox)
from PyQt5.uic import loadUi
from PyQt5.QtCore import (QModelIndex, QItemSelection, QItemSelectionModel)
from models import SqlListProxyModel


class ListViewDialog(QDialog):

    def __init__(self, model, proxy_model=None):
        super(ListViewDialog, self).__init__()
        self.ui = loadUi("ui/listview_dialog.ui", self)

        self.model = model
        self.proxy_model = proxy_model

        self.setTriggers()
        self.setButtonState()

    def setTriggers(self):
        self.ui.pushButton_create.clicked.connect(self.insertAction)
        self.ui.pushButton_remove.clicked.connect(self.removeAction)
        self.ui.pushButton_edit.clicked.connect(self.editAction)

        self.ui.listView_doctype.pressed.connect(self.setButtonState)

    def setModels(self):
        pass
    #def setModel(self, model, model_column=1, default_column=None):
    #    model.select()
    #    model.dataChanged.connect(self.dataChangedAction)

        # if model has default items load proxy model
    #    if default_column:
    #        list_model = SqlListProxyModel(default_column)
    #        list_model.setSourceModel(model)
    #        self.ui.listView_doctype.setModel(list_model)
    #        self.__proxy_model = list_model
    #    else:
    #        self.ui.listView_doctype.setModel(model)

    #    self.ui.listView_doctype.setModelColumn(model_column)

    #    self.__model = model

    def insertAction(self):
        total = self.__model.rowCount()
        column = self.listView_doctype.modelColumn()

        self.__model.insertRow(total)

        index = self.__model.index(total, column, QModelIndex())
        self.__model.setData(index, "Новая запись", Qt.EditRole)

        self.__model.submit()

        # map index from source model
        if self.proxy_model:
            index = self.__proxy_model.mapFromSource(index)

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
                self.__model.removeRows(idx[0].row(), column, QModelIndex())
                self.__model.select()

                self.setButtonState()

    def editAction(self):
        index = self.listView_doctype.selectedIndexes()[0]
        self.ui.listView_doctype.edit(index)

    def dataChangedAction(self):
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setDisabled(True)

    def setButtonState(self):
        isSelected = len(self.listView_doctype.selectedIndexes()) > 0

        self.ui.pushButton_remove.setDisabled(not isSelected)
        self.ui.pushButton_edit.setDisabled(not isSelected)
