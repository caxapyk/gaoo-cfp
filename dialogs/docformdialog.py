from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import (QModelIndex, QItemSelection, QItemSelectionModel)
from PyQt5.QtSql import QSqlRelationalTableModel
from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QDataWidgetMapper, QMessageBox)
from models import DocModel, DoctypeModel, DocFlagsModel, DocYearsModel
from views import YearItemDelegate


class DocFormDialog(QDialog):
    def __init__(self, model, row=None):
        super(DocFormDialog, self).__init__()

        ui = loadUi("ui/docform_dialog.ui", self)

        ui.buttonBox.button(
            QDialogButtonBox.Save).clicked.connect(self.saveAction)
        ui.buttonBox.button(
            QDialogButtonBox.Ok).clicked.connect(self.accept)
        ui.buttonBox.rejected.connect(self.closeAction)

        self.setWindowTitle("Новый документ")
        self.setWindowIcon(QIcon(":/icons/church-16.png"))
        self.setModal(True)

        doc_model = model

        if row is None:
            print(row)
            #print(row, doc_model.rowCount())
            doc_model.insertRows(doc_model.rowCount(), 1, QModelIndex())
            row  = doc_model.rowCount() - 1

            #print(row, doc_model.rowCount())
        #    index = index.model().index(index.model().rowCount(), 0)

        #if index.isValid():
        if True:

            mapper = QDataWidgetMapper()
            mapper.setModel(doc_model)
            mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)

            mapper.addMapping(ui.doctype_comboBox, doc_model.record(row).indexOf("cfp_doc.doctype_id"))
            mapper.addMapping(ui.fund_lineEdit, doc_model.record(row).indexOf("cfp_doc.fund"))
            mapper.addMapping(ui.inventory_lineEdit, doc_model.record(row).indexOf("cfp_doc.inventory"))
            mapper.addMapping(ui.unit_lineEdit, doc_model.record(row).indexOf("cfp_doc.unit"))
            mapper.addMapping(ui.sheet_spinBox, doc_model.record(row).indexOf("cfp_doc.sheets"))
            mapper.addMapping(ui.comment_textEdit, doc_model.record(row).indexOf("cfp_doc.comment"))

            mapper.setCurrentIndex(row)

            # doctype
            doctype_model = DoctypeModel()
            doctype_model.select()

            ui.doctype_comboBox.setModel(doctype_model)
            ui.doctype_comboBox.setModelColumn(0)

            # years
            #years_model = DocYearsModel(index)
            #ui.year_listView.setModel(years_model)

            #year_delegate = YearItemDelegate()
            #year_delegate.closeEditor.connect(self.checkYear)
            #ui.year_listView.setItemDelegateForColumn(0, year_delegate)

            #ui.yearInsert_pushButton.clicked.connect(self.insertYear)
            #ui.yearRemove_pushButton.clicked.connect(self.removeYear)

            # docflags
            #docflag_model = DocFlagsModel(index)
            #ui.docflag_listView.setModel(docflag_model)
            #ui.docflag_listView.setModelColumn(1)

        # else:
        #    doc_model = DocModel()

        self.ui = ui
        self.doc_model = doc_model
        #self.years_model = years_model
        self.mapper = mapper

    def insertYear(self):
        t_rows = self.years_model.rowCount(QModelIndex())

        if self.years_model.insertRows(t_rows, 1, QModelIndex()):
            index = self.years_model.index(t_rows)

            self.ui.year_listView.setCurrentIndex(index)
            self.ui.year_listView.edit(index)

    def removeYear(self):
        idx = self.ui.year_listView.selectedIndexes()
        if len(idx) > 0:
            self.years_model.removeRows(idx[0].row(), 1, QModelIndex())

    def checkYear(self, editor):
        if not editor.hasAcceptableInput():
            self.removeYear()

    def saveAction(self):
        self.mapper.submit()
        self.doc_model.submitAll()

    def closeAction(self):
        self.destroy()
