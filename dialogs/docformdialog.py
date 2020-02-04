from PyQt5.Qt import Qt
from PyQt5.QtSql import QSqlRelationalDelegate
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QLineEdit, QDataWidgetMapper)
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

from models import (DoctypeModel, DocFlagsModel, DocYearsModel)
from .yearitemdelegate import YearItemDelegate


class DocFormDialog(QDialog):
    def __init__(self, model, index=None):
        super(DocFormDialog, self).__init__()

        self.ui = loadUi("ui/docform_dialog.ui", self)

        self.ui.buttonBox.button(
            QDialogButtonBox.Save).clicked.connect(self.saveAction)
        self.ui.buttonBox.button(
            QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.closeAction)

        self.setWindowTitle("Новый документ")
        self.setWindowIcon(QIcon(":/icons/church-16.png"))
        self.setModal(True)

        self.model_index = index

        # doc model
        self.doc_model = model
        self.doc_model.setCurrentIndex(index)

        # doctype model
        self.doctype_model = DoctypeModel()
        self.doctype_model.select()
        self.ui.doctype_comboBox.setModel(self.doctype_model)
        self.ui.doctype_comboBox.setModelColumn(1)

        self.year_list = ""
        self.flag_list = ""

        if self.model_index is not None:
            self.record = self.doc_model.record(self.model_index.row())
            self.year_list = self.record.value("years")
            self.flag_list = self.record.value("flags")

            # data mapper
            mapper = QDataWidgetMapper()
            mapper.setModel(self.doc_model)
            mapper.setItemDelegate(QSqlRelationalDelegate())
            mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)

            print(self.record.indexOf("cfp_doctype.name"))

            mapper.addMapping(self.ui.doctype_comboBox,
                              self.record.indexOf("cfp_doctype.name"))
            mapper.addMapping(self.ui.fund_lineEdit,
                              self.record.indexOf("cfp_doc.fund"))
            mapper.addMapping(self.ui.inventory_lineEdit,
                              self.record.indexOf("cfp_doc.inventory"))
            mapper.addMapping(self.ui.unit_lineEdit,
                              self.record.indexOf("cfp_doc.unit"))
            mapper.addMapping(self.ui.sheet_spinBox,
                              self.record.indexOf("cfp_doc.sheets"))
            mapper.addMapping(self.ui.comment_textEdit,
                              self.record.indexOf("cfp_doc.comment"))
            # virtal mappings
            self.years_lineedit = QLineEdit()
            mapper.addMapping(self.years_lineedit,
                              self.record.indexOf("years"))
            self.flags_lineedit = QLineEdit()
            mapper.addMapping(self.flags_lineedit,
                              self.record.indexOf("flags"))

            mapper.setCurrentIndex(self.model_index.row())
            self.mapper = mapper

        # years
        self.years_model = DocYearsModel(self.year_list)

        self.ui.year_listView.setModel(self.years_model)

        year_delegate = YearItemDelegate()
        year_delegate.closeEditor.connect(self.checkYear)
        self.ui.year_listView.setItemDelegateForColumn(0, year_delegate)

        self.ui.yearInsert_pushButton.clicked.connect(self.insertYear)
        self.ui.yearRemove_pushButton.clicked.connect(self.removeYear)

        # docflags
        self.docflags_model = DocFlagsModel(self.flag_list)

        self.ui.docflag_listView.setModel(self.docflags_model)
        self.ui.docflag_listView.setModelColumn(1)

    def insertYear(self):
        total_rows = self.years_model.rowCount()
        if self.years_model.insertRows(total_rows, 1):
            index = self.years_model.index(total_rows)

            self.ui.year_listView.setCurrentIndex(index)
            self.ui.year_listView.edit(index)

    def removeYear(self):
        idx = self.ui.year_listView.selectedIndexes()
        if len(idx) > 0:
            self.years_model.removeRows(idx[0].row(), 1)

    def checkYear(self, editor):
        if not editor.hasAcceptableInput():
            self.years_model.removeRows(self.years_model.rowCount() - 1, 1)

    def saveAction(self):
        print("saveAction")
        self.years_lineedit.setText(self.years_model.data_())
        self.flags_lineedit.setText(self.docflags_model.data_())
        #self.record.setValue("years", self.years_model.data_())
        self.mapper.submit()

        #doctype_idx = self.ui.doctype_comboBox.currentIndex()
        #self.doctype_model.record(doctype_idx).value("id")

        #record = self.doc_model.emptyRecord()
        #record.setValue("cfp_doc.church_id", self.doc_model.churchId())
        #record.setValue("cfp_doc.doctype_id", ?)
        #record.setValue("cfp_doc.fund", self.ui.fund_lineEdit.text())
        #record.setValue("cfp_doc.inventory", self.ui.inventory_lineEdit.text())
        #record.setValue("cfp_doc.unit", self.ui.unit_lineEdit.text())
        #record.setValue("cfp_doc.sheets", self.ui.sheet_spinBox.value())
        #record.setValue("cfp_doc.comment", self.ui.comment_textEdit.toPlainText())

        #self.mapper.submit()
        #self.doc_model.setData(self.doc_model.index(self.model_index.row(), 14), ",".join(self.years_model.data_()))
        #self.doc_model.setData(self.doc_model.index(self.model_index.row(), 15), ",".join(self.docflags_model.data_()))
        #doctype_idx = self.ui.doctype_comboBox.currentIndex()
        #data = {
        #    "cfp_doc.church_id": self.record.value("cfp_doc.church_id"),
        #    "cfp_doc.doctype_id": self.doctype_model.record(doctype_idx).value("id"),
        #    "cfp_doc.fund": self.ui.fund_lineEdit.text(),
        #    "cfp_doc.inventory": self.ui.inventory_lineEdit.text(),
        #    "cfp_doc.unit": self.ui.unit_lineEdit.text(),
        #    "cfp_doc.sheets": self.ui.sheet_spinBox.value(),
        #    "cfp_doc.comment": self.ui.comment_textEdit.toPlainText(),
        #    "years": self.years_model.data_(),
        #    "flags": self.docflags_model.data_()
        #}

        #if self.model_index is None:
        #    # pass id of record to data on last inserted id
        #    if self.doc_model.lastInsertId():
        #        data["cfp_doc.id"] = self.doc_model.lastInsertId()
        #        self.doc_model.update(data, self.model_index)
        #    else:
       #         self.doc_model.insert(data)
       # else:
       #     # pass id of record to data on exising index
       #     data["cfp_doc.id"] = self.record.value("cfp_doc.id")
       #     self.doc_model.update(data, self.model_index)

    def closeAction(self):
        self.destroy()
