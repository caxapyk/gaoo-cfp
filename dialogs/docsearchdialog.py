from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (
    QDialog, QWidget, QDialogButtonBox, QMessageBox, QLineEdit, QComboBox, QGroupBox)
from PyQt5.uic import loadUi
from PyQt5.QtCore import (QModelIndex, QItemSelection, QItemSelectionModel)
from PyQt5.QtGui import QIcon
from models import ComboProxyModel, CheckListProxyModel, GuberniaModel, DoctypeModel, DocflagModel, DocSearchModel


class DocSearchDialog(QDialog):

    def __init__(self, parent):
        super(DocSearchDialog, self).__init__(parent)
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

        self.docflag_model = DocflagModel()
        self.doctype_clp_model = CheckListProxyModel(self.docflag_model)
        self.doctype_clp_model.setModelColumn(1)
        self.ui.listView_docflag.setModel(self.doctype_clp_model)

    def clearForm(self):
        result = QMessageBox().critical(
            self, "Поиск документов",
            "Вы уверены, что хотите очистить параметры поиска?",
            QMessageBox.Cancel | QMessageBox.Yes)

        if result == QMessageBox.Yes:
            self.ui.comboBox_gubernia.setCurrentIndex(0)
            self.ui.comboBox_doctype.setCurrentIndex(0)

            for widget in self.ui.findChildren(QLineEdit):
                widget.clear()

            self.ui.listView_docflag.model().reset()

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
        # doc groupt
        if self.ui.groupBox_doc.isChecked():
            if self.ui.comboBox_doctype.currentIndex() > 0:
                self.doc_search_model.andFilterWhere(
                    "=", "cfp_doctype.name", self.ui.comboBox_doctype.currentText())
            self.doc_search_model.andFilterWhere(
                "=", "cfp_doc.fund", self.ui.lineEdit_fund.text())
            self.doc_search_model.andFilterWhere(
                "=", "cfp_doc.inventory", self.ui.lineEdit_inventory.text())
            self.doc_search_model.andFilterWhere(
                "=", "cfp_doc.unit", self.ui.lineEdit_unit.text())
            self.doc_search_model.andFilterWhere(
                "=", "cfp_doc.unit", self.ui.lineEdit_unit.text())
            self.doc_search_model.andFilterWhere(
                "BETWEEN", "cfp_docyears.year", self.ui.lineEdit_year_from.text(), self.ui.lineEdit_year_to.text())
        # flags group   
        if self.ui.groupBox_flags.isChecked():
            if self.ui.checkBox_flaghard.checkState() == Qt.Checked:
                mode = "STRICT"
            else:
                mode = "NONSTRICT"

            self.doc_search_model.andFilterWhere(
                "EXISTS", "cfp_docflag.id", self.doctype_clp_model.data_(), mode)

        self.doc_search_model.refresh()

        self.ui.treeView_docs.setModel(self.doc_search_model)

        self.ui.treeView_docs.resizeColumnToContents(0)
        self.ui.treeView_docs.hideColumn(1)
        self.ui.treeView_docs.setColumnWidth(2, 150)
        self.ui.treeView_docs.setColumnWidth(3, 150)
        self.ui.treeView_docs.setColumnWidth(4, 150)
        self.ui.treeView_docs.setColumnWidth(5, 200)
        self.ui.treeView_docs.hideColumn(6)
        self.ui.treeView_docs.hideColumn(7)
        self.ui.treeView_docs.hideColumn(8)
        self.ui.treeView_docs.hideColumn(9)
        self.ui.treeView_docs.setColumnWidth(10, 75)
        self.ui.treeView_docs.setColumnWidth(11, 200)
        self.ui.treeView_docs.setColumnWidth(12, 75)
        self.ui.treeView_docs.setColumnWidth(13, 200)
        self.ui.treeView_docs.hideColumn(15)
        self.ui.treeView_docs.setColumnWidth(16, 300)
