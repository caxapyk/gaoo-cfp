from PyQt5.Qt import Qt
from PyQt5.QtGui import QIcon
from PyQt5.uic import loadUi
from PyQt5.QtCore import (QModelIndex, QItemSelection, QItemSelectionModel)
from PyQt5.QtSql import QSqlTableModel, QSqlRelationalTableModel, QSqlRelationalDelegate, QSqlRelation
from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QDataWidgetMapper, QMessageBox, QLineEdit)
from models import DocModel, DoctypeModel, DocFlagsModel, DocYearsModel, DocModelPlain
from .yearitemdelegate import YearItemDelegate


class DocFormDialog(QDialog):
    def __init__(self, model, index=None):
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

        # doc model
        doc_model = model
        # doctype model
        doctype_model = DoctypeModel()
        doctype_model.select()
        ui.doctype_comboBox.setModel(doctype_model)
        ui.doctype_comboBox.setModelColumn(1)

        
        
        if index is not None:
            rec = doc_model.record(index.row())

            # data mapper
            mapper = QDataWidgetMapper()
            mapper.setModel(doc_model)
            mapper.setItemDelegate(QSqlRelationalDelegate())
            #mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
            

            mapper.addMapping(ui.doctype_comboBox,
                              rec.indexOf("cfp_doctype.name"))
            mapper.addMapping(ui.fund_lineEdit,
                              rec.indexOf("cfp_doc.fund"))
            mapper.addMapping(ui.inventory_lineEdit,
                              rec.indexOf("cfp_doc.inventory"))
            mapper.addMapping(ui.unit_lineEdit,
                              rec.indexOf("cfp_doc.unit"))
            mapper.addMapping(ui.sheet_spinBox,
                              rec.indexOf("cfp_doc.sheets"))
            mapper.addMapping(ui.comment_textEdit,
                              rec.indexOf("cfp_doc.comment"))

            mapper.setCurrentModelIndex(index)

        # years
        if index is not None:
            rec = doc_model.record(index.row())
            years_model = DocYearsModel(rec.value("years"))
        else:
            years_model = DocYearsModel()

        ui.year_listView.setModel(years_model)
        #ui.year_listView.setModelColumn(2)

        year_delegate = YearItemDelegate()
        year_delegate.closeEditor.connect(self.checkYear)
        ui.year_listView.setItemDelegateForColumn(0, year_delegate)

        ui.yearInsert_pushButton.clicked.connect(self.insertYear)
        ui.yearRemove_pushButton.clicked.connect(self.removeYear)

        # docflags
        if index is not None:
            rec = doc_model.record(index.row())
            docflags_model = DocFlagsModel(rec.value("flags"))
        else:
            docflags_model = DocFlagsModel()

        ui.docflag_listView.setModel(docflags_model)
        ui.docflag_listView.setModelColumn(1)


            #doc_model = QSqlRelationalTableModel()
            #doc_model.setTable("cfp_doc")
            #doc_model.setRelation(2, QSqlRelation(
            #    "cfp_doctype", "id", "name AS `cfp_doctype.name`"))
            #doc_model.setEditStrategy(QSqlRelationalTableModel.OnManualSubmit)
            #doc_model.setFilter("cfp_doc.id=%s" % doc_id)
            #doc_model.select()

        # create empty record
        #if self.doc_id is None:
        #    rec = record()
        #    rec.remove(0)  # remove `id`
        #    rec.setValue("cfp_doc.church_id", church_id)
        #    rec.setValue("cfp_doc.doctype_id", 1)
        #    rec.setNull("cfp_doc.fund")
        #    rec.setNull("cfp_doc.inventory")
        #    rec.setNull("cfp_doc.sheets")
        #    rec.setNull("cfp_doc.comment")

        #    if (doc_model.insertRecord(-1, rec)):
        #        print("ins")

        # doctype
        #doctype_model = doc_model.relationModel(2)
        

        # years
        #years_model = DocYearsModel()
        #if self.doc_id is not None:
        #    years_model.setDocId(self.doc_id)
        #years_model.setEditStrategy(QSqlTableModel.OnManualSubmit)

        #years_model.select()

        #ui.year_listView.setModel(years_model)
        #ui.year_listView.setModelColumn(2)

        #year_delegate = YearItemDelegate()
        #year_delegate.closeEditor.connect(self.checkYear)
        #ui.year_listView.setItemDelegateForColumn(2, year_delegate)

        #ui.yearInsert_pushButton.clicked.connect(self.insertYear)
        #ui.yearRemove_pushButton.clicked.connect(self.removeYear)

        # docflags
        #docflags_model = DocFlagsModel(self.doc_id)

        # if doc_id is not None:
        #docflags_model.select()

        #ui.docflag_listView.setModel(docflags_model)
        #ui.docflag_listView.setModelColumn(1)


        self.ui = ui
        self.doc_model = doc_model
        self.doctype_model = doctype_model
        self.years_model = years_model
        self.index = index
        #self.years_model = years_model
        self.docflags_model = docflags_model
        #self.mapper = mapper
        #self.church_id = church_id

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
        print(self.docflags_model.data_())
        data = {
        "cfp_doc.church_id": self.doc_model.getChurchId(),
        "cfp_doc.doctype_id": self.doctype_model.record(self.ui.doctype_comboBox.currentIndex()).value("id"),

        "cfp_doc.fund": self.ui.fund_lineEdit.text(),
        "cfp_doc.inventory": self.ui.inventory_lineEdit.text(),
        "cfp_doc.unit": self.ui.unit_lineEdit.text(),
        "cfp_doc.sheets": self.ui.sheet_spinBox.value(),
        "cfp_doc.comment": self.ui.comment_textEdit.toPlainText(),
        "years": self.years_model.data_(),
        "flags": self.docflags_model.data_()
        }

        if self.index is None:
            if self.doc_model.lastInsertId():
                print('update')
                data["cfp_doc.id"] = self.doc_model.lastInsertId()
                self.doc_model.update(data)
            else:
                print("indert")
                self.doc_model.insert(data)

        else:
            # pass id of record to data on exising index
            rec = self.doc_model.record(self.index.row())
            data["cfp_doc.id"] = rec.value("cfp_doc.id")

            self.doc_model.update(data)

        #self.doc_model.submit()
        #print(self.doc_model.query().lastQuery())
        #print(self.doc_model.lastError().text())
        #self.years_model.submitAll()
        # self.docflags_model.submitAll()
        print("save")

    def closeAction(self):
        self.doc_model.revertAll()
        self.years_model.revertAll()
        # self.docflags_model.revertAll()
        self.destroy()
