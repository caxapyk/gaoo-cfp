from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (
    QDialog, QWidget, QDialogButtonBox, QMessageBox, QLineEdit, QComboBox, QGroupBox)
from PyQt5.uic import loadUi
from PyQt5.QtCore import (QModelIndex, QItemSelection, QItemSelectionModel)
from PyQt5.QtGui import QIcon
from models import ComboProxyModel, CheckListProxyModel, GuberniaModel, DoctypeModel, DocflagModel, DocSearchModel


class SearchDialog(QDialog):

    def __init__(self, parent):
        super(SearchDialog, self).__init__(parent)
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
        print("search")
        filter_ = ""

        self.doc_search_model = DocSearchModel()
        # geo group
        if self.ui.groupBox_geo.isEnabled():
            if self.ui.comboBox_gubernia.currentIndex() > 0:
                self.doc_search_model.andFilterWhere(
                    "=", "cfp_gubernia.name", self.ui.comboBox_gubernia.currentText())
            self.doc_search_model.andFilterWhere(
                "LIKE", "cfp_uezd.name", self.ui.lineEdit_uezd.text())
            self.doc_search_model.andFilterWhere(
                "LIKE", "cfp_locality.name", self.ui.lineEdit_locality.text())
            self.doc_search_model.andFilterWhere(
                "LIKE", "cfp_church.name", self.ui.lineEdit_church.text())

        if self.ui.groupBox_doc.isEnabled():
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
            if self.ui.checkBox_flaghard.checkState() == Qt.Checked:
                self.doc_search_model.andFilterWhere(
                    "IN", "cfp_docflag.id", self.doctype_clp_model.data_(), "=")
            else:
                self.doc_search_model.andFilterWhere(
                    "IN", "cfp_docflag.id", self.doctype_clp_model.data_(), "IN")

            #    filter_ += " cfp_gubernia.name=\"%s\"" % widget.currentText()
            # elif widget.objectName() == "comboBox_doctype":
            #    filter_ += " cfp_doctype.name.name=\"%s\"" % widget.currentText()
        print(filter_)

        #    if len(self.ui.lineEdit_uezd.text()) > 0:
        #        filter_ += " cfp_uezd.name LIKE \"%%%s%%\"" % self.ui.lineEdit_uezd.text()

        # self.doc_search_model.setFilter(filter_)
        self.doc_search_model.refresh()

        self.ui.treeView_docs.setModel(self.doc_search_model)
