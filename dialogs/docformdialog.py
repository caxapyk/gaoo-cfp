from PyQt5.Qt import Qt, QRegExp
from PyQt5.QtSql import QSqlRelationalDelegate
from PyQt5.QtWidgets import (
    QDialog, QDialogButtonBox, QDataWidgetMapper, QMessageBox)
from PyQt5.QtGui import (QIcon, QRegExpValidator)
from PyQt5.uic import loadUi
from models import (DocFlagsModel, DocYearsModel)
from .doctypedialog import DoctypeDialog
from .funddialog import FundDialog
from .inputdialog import InputDialog
from .yearitemdelegate import YearItemDelegate


class DocFormDialog(QDialog):

    regex = QRegExp("^[(А-яA-z-0-9.,)\\s]+$")

    def __init__(self, parent, model, row=None):
        super(DocFormDialog, self).__init__(parent)

        self.ui = loadUi("ui/docform_dialog.ui", self)

        self.ui.buttonBox.button(
            QDialogButtonBox.Ok).clicked.connect(self.okAction)
        self.ui.buttonBox.button(
            QDialogButtonBox.Save).clicked.connect(self.saveAction)
        self.ui.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)

        self.ui.buttonBox.rejected.connect(self.reject)

        # set validators
        self.ui.inventory_lineEdit.setValidator(QRegExpValidator(self.regex))
        self.ui.unit_lineEdit.setValidator(QRegExpValidator(self.regex))

        if row is None:
            self.setWindowTitle("Новый документ")

        self.setWindowIcon(QIcon(":/icons/church-16.png"))

        self.currentChanged = False

        # current model row
        self.m_row = row

        # doc model
        self.doc_model = model
        self.doc_model.dataChanged.connect(self.formChanged)

        # set locality
        self.ui.locality_textEdit.setText(self.doc_model.locality())

        # doctype model
        self.doctype_model = self.doc_model.relationModel(2)
        self.doctype_model.sort(1, Qt.AscendingOrder)
        self.doctype_model.dataChanged.connect(self.formChanged)

        self.ui.doctype_comboBox.setModel(self.doctype_model)
        self.ui.doctype_comboBox.setModelColumn(1)
        self.ui.doctype_comboBox.setCurrentIndex(-1)

        self.ui.pushButton_doctype_dlg.clicked.connect(
            lambda: self.chooseItemDialog(
                self.ui.doctype_comboBox,
                DoctypeDialog(self),
                self.doctype_model))

        # fund model
        self.fund_model = self.doc_model.relationModel(3)
        self.fund_model.sort(1, Qt.AscendingOrder)
        self.fund_model.dataChanged.connect(self.formChanged)

        self.ui.fund_comboBox.setModel(self.fund_model)
        self.ui.fund_comboBox.setModelColumn(1)
        self.ui.fund_comboBox.setCurrentIndex(-1)

        self.ui.pushButton_fund_dlg.clicked.connect(
            lambda: self.chooseItemDialog(
                self.ui.fund_comboBox,
                FundDialog(self),
                self.fund_model))

        # years
        years_list = self.doc_model.docYears(self.m_row)

        self.years_model = DocYearsModel(years_list)
        self.years_model.dataChanged.connect(self.formChanged)

        self.ui.year_listView.setModel(self.years_model)

        self.year_delegate = YearItemDelegate()
        self.ui.year_listView.setItemDelegateForColumn(0, self.year_delegate)

        self.ui.yearInsertRange_pushButton.clicked.connect(
            self.yearRangeDialog)
        self.ui.yearInsert_pushButton.clicked.connect(self.insertYear)
        self.ui.yearRemove_pushButton.clicked.connect(self.removeYear)

        # docflags
        flags_list = self.doc_model.docFlags(self.m_row)

        self.flags_model = DocFlagsModel(flags_list)
        self.flags_model.dataChanged.connect(self.formChanged)

        self.ui.docflag_listView.setModel(self.flags_model)
        self.ui.docflag_listView.setModelColumn(1)

        self.map()

        # set triggers to doc_model form changed
        self.ui.doctype_comboBox.currentIndexChanged.connect(self.formChanged)
        self.ui.fund_comboBox.currentIndexChanged.connect(self.formChanged)
        self.ui.inventory_lineEdit.textChanged.connect(self.formChanged)
        self.ui.unit_lineEdit.textChanged.connect(self.formChanged)
        self.ui.sheet_spinBox.valueChanged.connect(self.formChanged)
        self.ui.title_lineEdit.textChanged.connect(self.formChanged)
        self.ui.comment_textEdit.textChanged.connect(self.formChanged)

    def storageUnit(self):
        storage_unit = self.doc_model.data(
            self.doc_model.index(self.m_row, 12))
        return storage_unit

    def chooseItemDialog(self, widget, dialog, model):
        result = dialog.exec_()

        if result == dialog.Accepted:
            # get uid of item
            dlg_index = dialog.ui.listView.currentIndex()
            uid = dialog.model.data(dialog.model.index(dlg_index.row(), 0))

            # update relation model
            model.select()

            # find uid in relation model
            i = 0
            while i < model.rowCount():
                index = model.index(i, 0)
                if index.data() == uid:
                    widget.setCurrentIndex(i)
                    break
                i += 1

    def map(self):
        if self.m_row is not None:
            # set window title
            self.setWindowTitle(
                "Редактировать документ [%s]" % self.storageUnit())

            # data mapper
            self.mapper = QDataWidgetMapper()
            self.mapper.setModel(self.doc_model)
            self.mapper.setItemDelegate(QSqlRelationalDelegate())
            self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)

            dt_name_field = self.doc_model.fieldIndex("cfp_doctype.name")
            self.mapper.addMapping(self.ui.doctype_comboBox, dt_name_field)

            doc_fund_field = self.doc_model.fieldIndex("cfp_fund.name")
            self.mapper.addMapping(self.ui.fund_comboBox, doc_fund_field)

            doc_inv_field = self.doc_model.fieldIndex("cfp_doc.inventory")
            self.mapper.addMapping(self.ui.inventory_lineEdit, doc_inv_field)

            doc_unit_field = self.doc_model.fieldIndex("cfp_doc.unit")
            self.mapper.addMapping(self.ui.unit_lineEdit, doc_unit_field)

            doc_sheets_field = self.doc_model.fieldIndex("cfp_doc.sheets")
            self.mapper.addMapping(self.ui.sheet_spinBox, doc_sheets_field)

            dt_title_field = self.doc_model.fieldIndex(
                "cfp_doc.title")
            self.mapper.addMapping(
                self.ui.title_lineEdit, dt_title_field)

            doc_comm_field = self.doc_model.fieldIndex("cfp_doc.comment")
            self.mapper.addMapping(self.ui.comment_textEdit, doc_comm_field)

            self.mapper.setCurrentIndex(self.m_row)

    def yearRangeDialog(self):
        rangedialog = InputDialog(self)
        title = "Задать диапазон лет"

        val, res = rangedialog.getRange(title, QRegExp("[0-9]{4,4}"))

        if res == InputDialog.Accepted:
            _range = val.split(":")
            _range_from = int(_range[0])
            _range_to = int(_range[1])
            _range_count = _range_to - _range_from

            if _range_count > 100:
                box = QMessageBox()
                box.critical(
                    self, title,
                    'Нельзя задать диапазон более 100 лет!', QMessageBox.Ok)
            elif _range_count > 0:
                year = _range_from
                while year <= _range_to:
                    total_rows = self.years_model.rowCount()

                    self.years_model.insertRows(total_rows, 1)
                    self.years_model.setData(
                        self.years_model.index(total_rows, 0), str(year))

                    year += 1

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
            self.formChanged()

    def formChanged(self):
        self.currentChanged = True
        self.ui.buttonBox.button(QDialogButtonBox.Cancel).setDisabled(False)
        self.ui.buttonBox.button(QDialogButtonBox.Save).setDisabled(False)

    def validateForm(self):
        if not self.ui.doctype_comboBox.currentIndex() >= 0:
            return False
        elif not self.ui.fund_comboBox.currentIndex() >= 0:
            return False
        elif not self.ui.inventory_lineEdit.hasAcceptableInput():
            return False
        elif not self.ui.unit_lineEdit.hasAcceptableInput():
            return False
        # elif self.years_model.rowCount() == 0:
        #    return False

        return True

    def saveAction(self):
        if not self.validateForm():
            QMessageBox().critical(
                self, "Сохранение документа",
                'Не удалось сохранить документ!\n'
                'Проверьте правильность заполнения формы.', QMessageBox.Ok)
            return False

        # check document is a new
        if self.m_row is None:
            doctype_index = self.doctype_model.index(
                self.ui.doctype_comboBox.currentIndex(), 0)
            fund_index = self.fund_model.index(
                self.ui.fund_comboBox.currentIndex(), 0)

            record = self.doc_model.record()
            # remove id field
            record.remove(0)
            record.setValue("cfp_doc.church_id", self.doc_model.churchId())
            record.setValue("cfp_doctype.name", doctype_index.data())
            record.setValue("cfp_fund.name", fund_index.data())
            record.setValue("cfp_doc.inventory",
                            self.ui.inventory_lineEdit.text())
            record.setValue("cfp_doc.unit", self.ui.unit_lineEdit.text())
            record.setValue("cfp_doc.sheets", self.ui.sheet_spinBox.value())
            record.setValue("cfp_doc.title",
                            self.ui.title_lineEdit.text())
            record.setValue("cfp_doc.comment",
                            self.ui.comment_textEdit.toPlainText())

            if self.doc_model.insertRecord(-1, record):
                # set m_row to latest record row im model,
                # then connect wi QDataWidgetMapper
                self.m_row = self.doc_model.rowCount() - 1
                self.map()
            else:
                print(self.doc_model.lastError().text())
                QMessageBox().critical(
                    self, "Редактирование/Создание документа",
                    "Не удалось сохранить документ!(1)", QMessageBox.Ok)
                return False
        else:
            self.mapper.submit()

        if self.doc_model.submitAll():
            # get current document ID and set to years/flags models
            doc_id = self.doc_model.getItemId(self.m_row)

            self.years_model.setDoc(doc_id)
            self.flags_model.setDoc(doc_id)

            self.years_model.submitAll()
            self.flags_model.submitAll()

            self.doc_model.clearCache(self.m_row)

            self.ui.buttonBox.button(QDialogButtonBox.Cancel).setDisabled(True)
            self.ui.buttonBox.button(QDialogButtonBox.Save).setDisabled(True)

            self.currentChanged = False

            return True
        else:
            self.doc_model.revertAll()
            QMessageBox().critical(
                self, "Редактирование/Создание документа",
                "Не удалось сохранить документ!(2)", QMessageBox.Ok)

        return False

    def okAction(self):
        if self.currentChanged:
            result = QMessageBox().critical(
                self, "Сохранение документа",
                "Сохранить документ перед выходом?",
                QMessageBox.No | QMessageBox.Yes)

            if result == QMessageBox.Yes:
                if self.saveAction():
                    self.accept()
            elif result == QMessageBox.No:
                self.doc_model.revertAll()
                super().reject()
        else:
            self.accept()

    def reject(self):
        if self.currentChanged:
            result = QMessageBox().critical(
                self, "Сохранение документа",
                "Вы уверены, что хотите выйти без сохранения документа?",
                QMessageBox.Cancel | QMessageBox.Yes)

            if result == QMessageBox.Yes:
                self.doc_model.revertAll()
                super().reject()
        else:
            super().reject()
