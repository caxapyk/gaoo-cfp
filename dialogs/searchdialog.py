from PyQt5.Qt import Qt
from PyQt5.QtWidgets import (QDialog, QDialogButtonBox, QMessageBox, QLineEdit)
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
        self.doc_search_model = DocSearchModel()
        self.doc_search_model.refresh()

        self.ui.treeView_docs.setModel(self.doc_search_model)
