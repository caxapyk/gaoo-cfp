from PyQt5.Qt import (Qt, QRegExp)
from PyQt5.QtWidgets import (QDialog, QWidget, QDialogButtonBox,
                             QMessageBox, QLineEdit, QComboBox, QGroupBox, QCompleter)
from PyQt5.uic import loadUi
from PyQt5.QtCore import (QModelIndex, QItemSelection,
                          QItemSelectionModel, QSortFilterProxyModel)
from PyQt5.QtGui import (QIcon,  QRegExpValidator)
from PyQt5.QtSql import QSqlTableModel
from models import (ComboProxyModel, CheckListProxyModel, GuberniaModel,
                    DoctypeModel, DocflagModel, DocSearchModel, DocModel, FundModel, ChurchModel, DocSearchProxyModel)
from dialogs import DocViewDialog


class DocSearchDialog(QDialog):

    def __init__(self):
        super(DocSearchDialog, self).__init__()
        self.ui = loadUi("ui/search_dialog.ui", self)

        self.ui.pushButton_search.clicked.connect(self.search)
        self.ui.pushButton_clear.clicked.connect(self.clearForm)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.gub_model = GuberniaModel()
        self.gub_cp_model = ComboProxyModel(self.gub_model)
        self.gub_cp_model.setModelColumn(1)
        self.ui.comboBox_gubernia.setModel(self.gub_cp_model)

        self.doctype_model = DoctypeModel()
        self.doctype_cp_model = ComboProxyModel(self.doctype_model)
        self.doctype_cp_model.setModelColumn(1)
        self.ui.comboBox_doctype.setModel(self.doctype_cp_model)

        self.fund_model = FundModel()
        self.fund_cp_model = ComboProxyModel(self.fund_model)
        self.fund_cp_model.setModelColumn(1)
        self.ui.comboBox_fund.setModel(self.fund_cp_model)

        self.docflag_model = DocflagModel()
        self.doctype_clp_model = CheckListProxyModel(self.docflag_model)
        self.doctype_clp_model.setModelColumn(1)
        self.ui.listView_docflag.setModel(self.doctype_clp_model)

        # geo completers
        geo_tables = {
            "cfp_church": self.ui.lineEdit_church,
            "cfp_uezd": self.ui.lineEdit_uezd,
            "cfp_locality": self.ui.lineEdit_locality}

        for gt in geo_tables.items():
            geo_model = QSqlTableModel()
            geo_model.setTable(gt[0])
            geo_model.select()

            geo_completer = QCompleter(self)
            geo_completer.setModel(geo_model)
            geo_completer.setCompletionColumn(2)
            geo_completer.setCaseSensitivity(Qt.CaseInsensitive)

            widget = gt[1]
            widget.setCompleter(geo_completer)

        # set validators on year lineEdits
        year_regex = QRegExp("\\d{4,4}")
        self.ui.lineEdit_year_from.setValidator(QRegExpValidator(year_regex))
        self.ui.lineEdit_year_to.setValidator(QRegExpValidator(year_regex))

        self.ui.treeView_docs.doubleClicked.connect(self.viewDocDialog)

    def search(self):
        self.doc_search_model = DocSearchModel()
        # geo group
        if self.ui.groupBox_geo.isChecked():
            if self.ui.comboBox_gubernia.currentIndex() > 0:
                self.doc_search_model.andFilterWhere(
                    "=", "cfp_gubernia.name", self.ui.comboBox_gubernia.currentText())
            self.doc_search_model.andFilterWhere(
                "LIKE", "cfp_uezd.name", self.ui.lineEdit_uezd.text())
            self.doc_search_model.andFilterWhere(
                "LIKE", "cfp_locality.name", self.ui.lineEdit_locality.text())
            self.doc_search_model.andFilterWhere(
                "LIKE", "cfp_church.name", self.ui.lineEdit_church.text())
        # doc group
        if self.ui.groupBox_doc.isChecked():
            if self.ui.comboBox_doctype.currentIndex() > 0:
                self.doc_search_model.andFilterWhere(
                    "=", "cfp_doctype.name", self.ui.comboBox_doctype.currentText())
            if self.ui.comboBox_fund.currentIndex() > 0:
                self.doc_search_model.andFilterWhere(
                    "=", "cfp_fund.name", self.ui.comboBox_fund.currentText())
            self.doc_search_model.andFilterWhere(
                "=", "cfp_doc.inventory", self.ui.lineEdit_inventory.text())
            self.doc_search_model.andFilterWhere(
                "=", "cfp_doc.unit", self.ui.lineEdit_unit.text())
            self.doc_search_model.andFilterWhere(
                "=", "cfp_doc.unit", self.ui.lineEdit_unit.text())
            self.doc_search_model.andFilterWhere(
                "BETWEEN", "cfp_docyears.year", self.ui.lineEdit_year_from.text(), self.ui.lineEdit_year_to.text())
            self.doc_search_model.andFilterWhere(
                "LIKE", "cfp_doc.comment", self.ui.lineEdit_comment.text())
        # flags group
        if self.ui.groupBox_flags.isChecked():
            if self.ui.checkBox_flaghard.checkState() == Qt.Checked:
                mode = "STRICT"
            else:
                mode = "NONSTRICT"

            self.doc_search_model.andFilterWhere(
                "EXISTS", "cfp_docflag.id", self.doctype_clp_model.data_(), mode)

        self.doc_search_model.refresh()

        self.proxy_model = DocSearchProxyModel()
        self.proxy_model.setSourceModel(self.doc_search_model)

        self.ui.treeView_docs.setModel(self.proxy_model)
        # disable default sorting
        self.ui.treeView_docs.sortByColumn(-1, Qt.AscendingOrder)

        self.ui.treeView_docs.resizeColumnToContents(2)
        self.ui.treeView_docs.hideColumn(1)
        self.ui.treeView_docs.resizeColumnToContents(2)
        self.ui.treeView_docs.resizeColumnToContents(3)
        self.ui.treeView_docs.resizeColumnToContents(4)
        self.ui.treeView_docs.hideColumn(5)
        self.ui.treeView_docs.setColumnWidth(6, 200)
        self.ui.treeView_docs.resizeColumnToContents(7)
        self.ui.treeView_docs.setColumnWidth(8, 200)
        self.ui.treeView_docs.hideColumn(9)
        self.ui.treeView_docs.hideColumn(10)
        self.ui.treeView_docs.hideColumn(11)
        self.ui.treeView_docs.resizeColumnToContents(12)
        self.ui.treeView_docs.resizeColumnToContents(13)
        self.ui.treeView_docs.resizeColumnToContents(14)
        self.ui.treeView_docs.setColumnWidth(15, 300)

        self.setStatus()

    def setStatus(self):
        rows = self.doc_search_model.rowCount()
        status_text = "Найдено результатов: %s" % rows
        if rows > 499:
            status_text += ". \
Количество результатов ограничено до 500, уточните параметры поиска!"
        self.ui.label_status.setText(status_text)

    def clearForm(self):
        result = QMessageBox().critical(
            self, "Поиск документов",
            "Вы уверены, что хотите очистить параметры поиска?",
            QMessageBox.Cancel | QMessageBox.Yes)

        if result == QMessageBox.Yes:
            for widget in self.ui.findChildren((QComboBox, QLineEdit)):
                if isinstance(widget, QComboBox):
                    widget.setCurrentIndex(0)
                elif isinstance(widget, QLineEdit):
                    widget.clear()

            self.ui.listView_docflag.model().reset()

    def viewDocDialog(self):
        print("here")
        proxy_index = self.ui.treeView_docs.currentIndex()
        index = self.proxy_model.mapToSource(proxy_index)

        doc_id = self.doc_search_model.data(
            self.doc_search_model.index(index.row(), 1))  # `id` column is 1
        church_id = self.doc_search_model.data(
            self.doc_search_model.index(index.row(), 5))  # `church_id` column is 5

        doc_model = DocModel()
        doc_model.setFilter("cfp_doc.id=%s" % doc_id)
        doc_model.setChurch(church_id)
        doc_model.select()

        docview_dialog = DocViewDialog(self, doc_model, 0)
        docview_dialog.exec_()
