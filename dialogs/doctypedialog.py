from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QMessageBox)
from PyQt5.uic import loadUi
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import (QModelIndex, QItemSelection, QItemSelectionModel)


class DoctypeDialog(QDialog):
    def __init__(self):
        super(DoctypeDialog, self).__init__()
        self.ui = loadUi("ui/doctype_dialog.ui", self)

        self.ui.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)

        model = QSqlTableModel()
        model.setTable("cfp_doctype")
        model.setEditStrategy(QSqlTableModel.OnRowChange)
        model.select()

        model.setHeaderData(0, Qt.Horizontal, "ID")
        model.setHeaderData(1, Qt.Horizontal, "Имя")

        self.ui.listView_doctype.setModel(model)
        self.ui.listView_doctype.setModelColumn(1)

        self.ui.pushButton_create.clicked.connect(self.createAction)
        self.ui.pushButton_remove.clicked.connect(self.removeAction)
        self.ui.pushButton_edit.clicked.connect(self.editAction)
        self.ui.buttonBox.button(
            QDialogButtonBox.Save).clicked.connect(self.saveAction)
        self.ui.buttonBox.rejected.connect(self.closeAction)

        self.model = model

        self.show()

    def createAction(self):
        self.model.insertRow(self.model.rowCount())
        index = self.model.index(self.model.rowCount() - 1, 1, QModelIndex())
        self.model.setData(index, "Новая запись")

        self.ui.buttonBox.button(QDialogButtonBox.Save).setDisabled(False)

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
                self.model.beginRemoveRows(QModelIndex(), index[0].row(), index[0].row())
                self.model.removeRow(index[0].row())
                self.model.endRemoveRows()
                self.ui.buttonBox.button(
                    QDialogButtonBox.Save).setDisabled(False)

    def editAction(self):
        index = self.listView_doctype.currentIndex()
        self.ui.listView_doctype.edit(index)
        self.ui.buttonBox.button(QDialogButtonBox.Save).setDisabled(False)

    def saveAction(self):
        self.model.submitAll()
        self.ui.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)

    def closeAction(self):
        if self.ui.buttonBox.button(QDialogButtonBox.Save).isEnabled():
            result = QMessageBox().critical(self, "Сохранить данные",
                                            "Сохранить изменения?",
                                            QMessageBox.No | QMessageBox.Yes)
            if result == QMessageBox.Yes:
                self.saveAction()
            else:
                self.model.revertAll()
        self.close()
