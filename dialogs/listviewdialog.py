from PyQt5.Qt import Qt, QRegExp
from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QMessageBox, QInputDialog)
from PyQt5.uic import loadUi
from PyQt5.QtCore import (QModelIndex, QSortFilterProxyModel)
from .inputdialog import InputDialog


class ListViewDialog(QDialog):
    def __init__(self, parent):
        super(ListViewDialog, self).__init__(parent)
        self.ui = loadUi("ui/listview_dialog.ui", self)

        self.ui.pushButton_create.clicked.connect(self.insertAction)
        self.ui.pushButton_remove.clicked.connect(self.removeAction)
        self.ui.pushButton_edit.clicked.connect(self.editAction)
        self.ui.listView.pressed.connect(self.setButtonState)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.accepted.connect(self.accept)

        self.model = None
        self.regex = QRegExp("^[(А-яA-z-0-9.,)\\s]+$")

        self.setButtonState()

    def setModel(self, model, model_column=1):
        #self.model = model
        model.setEditStrategy(model.OnRowChange)
        model.select()

        self.model = QSortFilterProxyModel()
        self.model.setSourceModel(model)
        self.model.setDynamicSortFilter(False)
        self.model.sort(model_column, Qt.AscendingOrder)

        self.model.dataChanged.connect(self.dataChangedAction)

        self.ui.listView.setModel(self.model)
        self.ui.listView.setModelColumn(model_column)

    def insertAction(self):
        namedialog = InputDialog(self)
        title = "Cоздание объекта"

        val, res = namedialog.getText(
            title, "Заголовок", "", self.regex)

        if res == InputDialog.Accepted:
            total = self.model.rowCount()
            column = self.ui.listView.modelColumn()
            if len(val) > 0:
                if self.model.insertRow(total):
                    index = self.model.index(total, column)
                    if (not self.model.setData(index, val)) | (not self.model.submit()):
                        self.model.removeRow(total)
                        box = QMessageBox()
                        box.critical(self, title,
                                     "Не удалось сохранить объект!\n", QMessageBox.Ok)
                        return False

                    self.ui.listView.setCurrentIndex(index)
                    self.model.sort(self.model.sortColumn(), self.model.sortOrder())
                else:
                    box = QMessageBox()
                    box.critical(self, title,
                                 "Не удалось сохранить объект!\n", QMessageBox.Ok)
                    return False

                self.setButtonState()

    def editAction(self):
        index = self.ui.listView.currentIndex()

        namedialog = InputDialog(self)
        title = "Редактирование объекта"

        val, res = namedialog.getText(
            title, "Заголовок", index.data(), self.regex)

        if res == InputDialog.Accepted:
            if (not self.model.setData(index, val)) | (not self.model.submit()):
                box = QMessageBox()
                box.critical(self, title,
                             "Не удалось сохранить объект!\n", QMessageBox.Ok)
                return False

            self.listView.setCurrentIndex(index)
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
                    self.model.sourceModel().select()
                else:
                    self.model.revert()
                    self.ui.listView.setCurrentIndex(QModelIndex())
                    box = QMessageBox()
                    box.critical(self, "Удаление объекта",
                                 "Не удалось удалить объект!", QMessageBox.Ok)
                self.setButtonState()

    def dataChangedAction(self):
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setDisabled(True)

    def setButtonState(self):
        index = self.ui.listView.currentIndex()

        self.ui.pushButton_remove.setDisabled(not index.isValid())
        self.ui.pushButton_edit.setDisabled(not index.isValid())