from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import QModelIndex
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QDataWidgetMapper)
from models import DocModel, DoctypeModel, DocflagModel, YearModel


class DocFormDialog(QDialog):
    def __init__(self, index=QModelIndex()):
        super(DocFormDialog, self).__init__()

        ui = loadUi("ui/docform_dialog.ui", self)
        ui.setWindowIcon(QIcon(":/icons/church-16.png"))

        self.setWindowTitle("Новый документ")

        if index.isValid():
            doc_model = index.model()
        else:
            doc_model = DocModel()

        doctype_model = DoctypeModel()
        doctype_model.select()

        year_model = YearModel()
        year_model.select()

        docflag_model = DocflagModel()
        docflag_model.select()

        ui.doctype_comboBox.setModel(doctype_model)
        ui.doctype_comboBox.setModelColumn(1)


        if index.isValid():
            row = index.row()

            ui.year_listView.setModel(doc_model.yearRelation(doc_model.record(row).value("cfp_doc.id")))
            ui.year_listView.setModelColumn(1)

            ui.docflag_listView.setModel(doc_model.flagRelation(doc_model.record(row).value("cfp_doc.id")))
            ui.docflag_listView.setModelColumn(1)

            mapper = QDataWidgetMapper()
            # mapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)
            mapper.setModel(doc_model)
            mapper.addMapping(ui.doctype_comboBox, doc_model.record(
                row).indexOf("cfp_doctype.name"))
            mapper.addMapping(ui.fund_lineEdit, doc_model.record(
                row).indexOf("cfp_doc.fund"))
            mapper.addMapping(ui.inventory_lineEdit, doc_model.record(
                row).indexOf("cfp_doc.inventory"))
            mapper.addMapping(ui.unit_lineEdit, doc_model.record(
                row).indexOf("cfp_doc.unit"))
            mapper.addMapping(ui.sheet_spinBox, doc_model.record(
                row).indexOf("cfp_doc.sheets"))

            mapper.addMapping(ui.docflag_listView, doc_model.record(
                row).indexOf("cfp_doctype.name"))


            mapper.addMapping(ui.comment_textEdit, doc_model.record(
                row).indexOf("cfp_doc.comment"))

            mapper.setCurrentIndex(row)

        ui.buttonBox.button(
            QDialogButtonBox.Save).clicked.connect(self.submitAction)
        # self.ui.buttonBox.rejected.connect(self.closeAction)

        self.ui = ui
        self.doc_model = doc_model

    def submitAction(self):
        print("s")
