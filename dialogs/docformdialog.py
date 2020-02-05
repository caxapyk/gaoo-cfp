from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex
from PyQt5.QtSql import QSqlRelationalDelegate
from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QLineEdit, QDataWidgetMapper)
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi

from models import (DoctypeModel, DocFlagsModel, DocYearsModel)
from .yearitemdelegate import YearItemDelegate


class DocFormDialog(QDialog):
    def __init__(self, model, row=None):
        super(DocFormDialog, self).__init__()

        self.ui = loadUi("ui/docform_dialog.ui", self)

        self.ui.buttonBox.button(
            QDialogButtonBox.Ok).clicked.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.closeAction)
        self.ui.buttonBox.button(
                QDialogButtonBox.Save).clicked.connect(self.saveAction)

        self.setWindowTitle("Новый документ")
        self.setWindowIcon(QIcon(":/icons/church-16.png"))
        self.setModal(True)

        # doc model
        self.doc_model = model

        # row
        self.m_row = row

        # doctype model
        self.doctype_model = DoctypeModel()
        self.doctype_model.select()
        self.ui.doctype_comboBox.setModel(self.doctype_model)
        self.ui.doctype_comboBox.setModelColumn(1)

        if self.m_row is not None:
            # years
            self.rec = self.doc_model.record(row)

            # docflags
            #self.docflags_model = DocFlagsModel(self.rec.value("flags"))
            #self.docflags_model.setDoc(self.rec.value("cfp_doc.id"))

            # data mapper
            self.mapper = QDataWidgetMapper()
            self.mapper.setModel(self.doc_model)
            self.mapper.setItemDelegate(QSqlRelationalDelegate())
            self.mapper.setSubmitPolicy(QDataWidgetMapper.AutoSubmit)

            self.mapper.addMapping(self.ui.doctype_comboBox,
                                   self.rec.indexOf("cfp_doctype.name"))
            self.mapper.addMapping(self.ui.fund_lineEdit,
                                   self.rec.indexOf("cfp_doc.fund"))
            self.mapper.addMapping(self.ui.inventory_lineEdit,
                                   self.rec.indexOf("cfp_doc.inventory"))
            self.mapper.addMapping(self.ui.unit_lineEdit,
                                   self.rec.indexOf("cfp_doc.unit"))
            self.mapper.addMapping(self.ui.sheet_spinBox,
                                   self.rec.indexOf("cfp_doc.sheets"))
            self.mapper.addMapping(self.ui.comment_textEdit,
                                   self.rec.indexOf("cfp_doc.comment"))

            self.mapper.setCurrentIndex(row)


        # years
        years_list = self.doc_model.yearsList(self.m_row)
        print("yearsList:", years_list)

        self.years_model = DocYearsModel(years_list)
        self.ui.year_listView.setModel(self.years_model)

        self.year_delegate = YearItemDelegate()
        self.year_delegate.closeEditor.connect(self.checkYear)
        self.ui.year_listView.setItemDelegateForColumn(0, self.year_delegate)

        self.ui.yearInsert_pushButton.clicked.connect(self.insertYear)
        self.ui.yearRemove_pushButton.clicked.connect(self.removeYear)


        # docflags
        flags_list = self.doc_model.flagsList(self.m_row)
        self.flags_model = DocFlagsModel(flags_list)

        self.ui.docflag_listView.setModel(self.flags_model)
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
        if self.m_row is None:

            doctype_id = self.doctype_model.getItemId(
                self.ui.doctype_comboBox.currentIndex())

            record = self.doc_model.record()
            # remove id
            record.remove(0)
            record.setValue("cfp_doc.church_id", self.doc_model.churchId())
            record.setValue("cfp_doctype.name", doctype_id)
            record.setValue("cfp_doc.fund", self.ui.fund_lineEdit.text())
            record.setValue("cfp_doc.inventory", self.ui.inventory_lineEdit.text())
            record.setValue("cfp_doc.unit", self.ui.unit_lineEdit.text())
            record.setValue("cfp_doc.sheets", self.ui.sheet_spinBox.value())
            record.setValue("cfp_doc.comment",
                            self.ui.comment_textEdit.toPlainText())

            print(record.value("doctype_id"))

            if self.doc_model.insertRecord(-1, record):
                print("OK!!!!!!!")
            
            print(self.doc_model.lastError().text())

        if self.doc_model.submitAll():
            print("save")

            if self.doc_model.query().lastInsertId():
                doc_id = self.doc_model.query().lastInsertId()
            else:
                doc_id = self.doc_model.getItemId(self.m_row)
            
            self.years_model.setDoc(doc_id)
            self.flags_model.setDoc(doc_id)
            
            self.years_model.submitAll()
            self.flags_model.submitAll()
        #if self.doc_model.submitAll():

        #    self.doc_model.setData(self.doc_model.index(self.doc_model.currentIndex().row(), self.doc_model.emptyRecord().indexOf("years")), self.years_model.data_())
        #    self.doc_model.setData(self.doc_model.index(self.doc_model.currentIndex().row(), self.doc_model.emptyRecord().indexOf("flags")), self.docflags_model.data_())

        #    doc_id = self.doc_model.lastInsertId()
        #    if doc_id:
        #        self.years_model.setDoc(doc_id)
        #        self.docflags_model.setDoc(doc_id)

        #    self.years_model.submitAll()
        #    self.docflags_model.submitAll()

    def insertAction(self):
        if self.doc_model.currentIndex().isValid():
            print("sfsfsdf")
            return self.saveAction()

        doctype_idx = self.ui.doctype_comboBox.currentIndex()
        doctype_id = self.doctype_model.record(doctype_idx).value("id")

        record = self.doc_model.emptyRecord()

        record.setValue("cfp_doc.church_id", self.doc_model.churchId())
        record.setValue("cfp_doc.doctype_id", doctype_id)
        record.setValue("cfp_doc.fund", self.ui.fund_lineEdit.text())
        record.setValue("cfp_doc.inventory", self.ui.inventory_lineEdit.text())
        record.setValue("cfp_doc.unit", self.ui.unit_lineEdit.text())
        record.setValue("cfp_doc.sheets", self.ui.sheet_spinBox.value())
        record.setValue("cfp_doc.comment",
                        self.ui.comment_textEdit.toPlainText())
        record.setValue("years", self.years_model.data_())
        record.setValue("flags", self.docflags_model.data_())

        if self.doc_model.insertRecord(-1, record):
            self.saveAction()

    def closeAction(self):
        self.destroy()
