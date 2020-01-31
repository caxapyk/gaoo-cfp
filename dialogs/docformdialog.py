from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import (QModelIndex, QItemSelection, QItemSelectionModel)
from PyQt5.QtSql import QSqlRelationalTableModel, QSqlRelationalDelegate
from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QDataWidgetMapper, QMessageBox)
from models import DocModel, DoctypeModel, DocFlagsModel, DocYearsModel
from views import YearItemDelegate


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
        self.setModal(True)

        doc_model = index.model()

        # if row is None:
        #    print(row)
        #    #print(row, doc_model.rowCount())
        #    doc_model.insertRows(doc_model.rowCount(), 1, QModelIndex())
        #    row  = doc_model.rowCount() - 1

        #print(row, doc_model.rowCount())
        #    index = index.model().index(index.model().rowCount(), 0)

        # if index.isValid():
        if True:
            doc_id = doc_model.record(index.row()).value("cfp_doc.id")

            # doctype
            doctype_model = doc_model.relationModel(2)
            ui.doctype_comboBox.setModel(doctype_model)
            ui.doctype_comboBox.setModelColumn(
                doctype_model.fieldIndex("name"))

            # years
            years_model = DocYearsModel()
            years_model.setFilter("doc_id=%s" % doc_id)
            years_model.select()
            ui.year_listView.setModel(years_model)
            ui.year_listView.setModelColumn(2)

            year_delegate = YearItemDelegate()
            year_delegate.closeEditor.connect(self.checkYear)
            ui.year_listView.setItemDelegateForColumn(2, year_delegate)

            ui.yearInsert_pushButton.clicked.connect(self.insertYear)
            ui.yearRemove_pushButton.clicked.connect(self.removeYear)

            # docflags
            docflags_model = DocFlagsModel(doc_id)
            docflags_model.select()
            ui.docflag_listView.setModel(docflags_model)
            ui.docflag_listView.setModelColumn(1)

            mapper = QDataWidgetMapper()
            mapper.setModel(doc_model)
            mapper.setItemDelegate(QSqlRelationalDelegate())

            mapper.addMapping(ui.doctype_comboBox,
                              doc_model.fieldIndex("cfp_doctype.name"))
            mapper.addMapping(ui.fund_lineEdit,
                              doc_model.fieldIndex("cfp_doc.fund"))
            mapper.addMapping(ui.inventory_lineEdit,
                              doc_model.fieldIndex("cfp_doc.inventory"))
            mapper.addMapping(ui.unit_lineEdit,
                              doc_model.fieldIndex("cfp_doc.unit"))
            mapper.addMapping(ui.sheet_spinBox,
                              doc_model.fieldIndex("cfp_doc.sheets"))
            mapper.addMapping(ui.comment_textEdit,
                              doc_model.fieldIndex("cfp_doc.comment"))

            mapper.setCurrentIndex(index.row())

        # else:
        #    doc_model = DocModel()

        self.ui = ui
        self.doc_model = doc_model
        self.years_model = years_model
        self.docflags_model = docflags_model
        self.mapper = mapper
        self.doc_id = doc_id

    def insertYear(self):
        record = self.years_model.record()
        record.remove(record.indexOf("id"))
        record.setValue("doc_id", self.doc_id)
        record.setValue("year", "")

        if self.years_model.insertRecord(-1, record):
            index = self.years_model.index(self.years_model.rowCount() - 1, 2)

            self.ui.year_listView.setCurrentIndex(index)
            self.ui.year_listView.edit(index)

    def removeYear(self):
        print(1)
        idx = self.ui.year_listView.selectedIndexes()
        if len(idx) > 0:
            self.years_model.removeRows(idx[0].row(), 1)
            self.ui.year_listView.setRowHidden(idx[0].row(), True)

    def checkYear(self, editor):
        if not editor.hasAcceptableInput():
            self.years_model.removeRows(self.years_model.rowCount() - 1, 1)

    def saveAction(self):
        self.doc_model.submitAll()
        self.years_model.submitAll()
        self.docflags_model.submitAll()

    def closeAction(self):
        self.doc_model.revertAll()
        self.years_model.revertAll()
        self.docflags_model.revertAll()
        self.destroy()
