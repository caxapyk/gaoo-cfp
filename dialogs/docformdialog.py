from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import QModelIndex
from PyQt5.QtSql import QSqlRelationalTableModel
from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QDataWidgetMapper, QMessageBox)
from models import DocModel, DoctypeModel, YearsModel


class DocFormDialog(QDialog):
    def __init__(self, index):
        super(DocFormDialog, self).__init__()

        ui = loadUi("ui/docform_dialog.ui", self)

        ui.buttonBox.button(
            QDialogButtonBox.Save).clicked.connect(self.saveAction)
        ui.buttonBox.button(
            QDialogButtonBox.Ok).clicked.connect(self.accept)
        ui.buttonBox.rejected.connect(self.closeAction)

        self.setWindowTitle("Новый документ")
        self.setWindowIcon(QIcon(":/icons/church-16.png"))

        if index.isValid():
            doc_model = index.model()
            # doc_model.setEditStrategy(QSqlRelationalTableModel.OnRowChange)
            row = index.row()

            doctype_model = DoctypeModel()
            doctype_model.select()

            ui.doctype_comboBox.setModel(doctype_model)
            ui.doctype_comboBox.setModelColumn(1)

            print(index.internalPointer().years())
            print(index.internalPointer().flags())

        #    years_model = doc_model.yearsModel(row)
        #   ui.year_listView.setModel(years_model)
        #    ui.year_listView.setModelColumn(1)

            # ui.docflag_listView.setModel(doc_model.flagRelation(doc_model.record(row).value("cfp_doc.id")))
            # ui.docflag_listView.setModelColumn(1)

            mapper = QDataWidgetMapper()
            mapper.setModel(doc_model)
            mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)

            mapper.addMapping(ui.doctype_comboBox, doc_model.record(row).indexOf("name"))

            mapper.addMapping(ui.fund_lineEdit,
                              doc_model.record(row).indexOf("cfp_doc.fund"))
            mapper.addMapping(ui.inventory_lineEdit,
                              doc_model.record(row).indexOf("cfp_doc.inventory"))
            mapper.addMapping(ui.unit_lineEdit,
                              doc_model.record(row).indexOf("cfp_doc.unit"))
            mapper.addMapping(ui.sheet_spinBox,
                              doc_model.record(row).indexOf("cfp_doc.sheets"))

            # mapper.addMapping(ui.docflag_listView, doc_model.record(
            #    row).indexOf("name"))

            mapper.addMapping(ui.comment_textEdit, doc_model.record(row).indexOf("cfp_doc.comment"))

            mapper.setCurrentIndex(row)

        # else:
        #    doc_model = DocModel()

        self.ui = ui
        self.doc_model = doc_model
        self.mapper = mapper

    def saveAction(self):
        self.mapper.submit()
        # self.doc_model.submitAll()
        #print (self.doc_model.query().lastQuery())
        #print (self.doc_model.lastError().text())
        # self.accept()

    def closeAction(self):
        # if self.ui.buttonBox.button(QDialogButtonBox.Save).isEnabled():
        #    result = QMessageBox().critical(self, "Сохранить данные",
        #                                    "Сохранить изменения?",
        #                                    QMessageBox.No | QMessageBox.Yes)
        #    if result == QMessageBox.Yes:
        #        self.saveAction()
        #    else:
        #        self.mapper.revert()
        # self.destroy()
        pass
