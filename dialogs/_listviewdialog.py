from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QMessageBox)
from PyQt5.uic import loadUi
from PyQt5.QtCore import QModelIndex
from models import DefaultItemProxyModel
from .listviewdelegate import ListViewDelegate


class ListViewDialog(QDialog):

    NO_DEFAULT_COLUMN = -1

    def __init__(self, parent):
        super(ListViewDialog, self).__init__(parent)
        self.ui = loadUi("ui/listview_dialog.ui", self)

        self.ui.pushButton_create.clicked.connect(self.insertAction)
        self.ui.pushButton_remove.clicked.connect(self.removeAction)
        self.ui.pushButton_edit.clicked.connect(self.editAction)
        self.ui.listView.pressed.connect(self.setButtonState)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.accepted.connect(self.accept)

        self.delegate = ListViewDelegate()
        self.ui.listView.setItemDelegate(self.delegate)

        self.model = None

        self.setButtonState()

    def setModel(self, model, col=-1):
        """
        col (int) need if model have default items,
        col means column in database
        """
        self.model = model
        self.model.setEditStrategy(self.model.OnRowChange)
        self.model.setSort(0, Qt.AscendingOrder)

        if col != self.NO_DEFAULT_COLUMN:
            # model with default items
            proxy_model = DefaultItemProxyModel(col)
            proxy_model.setSourceModel(self.model)

        self.model.dataChanged.connect(self.dataChangedAction)

        self.ui.listView.setModel(self.model)
        self.ui.listView.setModelColumn(1)

    def insertAction(self):
        total = self.model.rowCount()
        column = self.ui.listView.modelColumn()

        if self.model.insertRow(total):
            index = self.model.index(total, column)
            self.listView.setCurrentIndex(index)

            # edit new item
            self.ui.listView.edit(index)

            self.setButtonState()

    def removeAction(self):
        index = self.ui.listView.currentIndex()
        if index.isValid():
            result = QMessageBox().critical(
                self, "Удаление объекта",
                "Вы уверены что хотите удалить \"%s\"?" % index.data(),
                QMessageBox.No | QMessageBox.Yes)

            if result == QMessageBox.Yes:
                del_result = self.model.removeRow(index.row())

                if del_result:
                    self.model.select()
                else:
                    self.model.revert()
                    self.ui.listView.setCurrentIndex(QModelIndex())
                    QMessageBox().critical(self, "Удаление объекта",
                                           "Не удалось удалить объект!\n\nПроверьте нет ли связей с другими объектами или возможно у Вас недостаточно привилегий.",
                                           QMessageBox.Ok)
                self.setButtonState()

    def editAction(self):
        index = self.ui.listView.currentIndex()
        self.ui.listView.edit(index)

    def dataChangedAction(self):
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setDisabled(True)

    def setButtonState(self):
        index = self.ui.listView.currentIndex()

        self.ui.pushButton_remove.setDisabled(not index.isValid())
        self.ui.pushButton_edit.setDisabled(not index.isValid())
