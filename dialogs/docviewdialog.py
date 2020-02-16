from PyQt5.QtWidgets import (QWidget, QDialogButtonBox, QComboBox, QLineEdit, QSpinBox, QListView, QPlainTextEdit)
from dialogs import DocFormDialog


class DocViewDialog(DocFormDialog):
    def __init__(self, parent, model, row=None):
        super(DocViewDialog, self).__init__(parent, model, row)

        self.setWindowTitle("Просмотр документа [%s]" % super().storageUnit())
        for widget in self.ui.tabWidget.findChildren(
            (QComboBox, QLineEdit, QSpinBox, QListView, QPlainTextEdit)):
                if isinstance(widget, QComboBox) or isinstance(widget, QListView):
                	widget.setDisabled(True)
                	widget.setStyleSheet("background-color:white;color:black")
                else:
                    widget.setReadOnly(True)

        self.ui.yearInsert_pushButton.hide()
        self.ui.yearRemove_pushButton.hide()
        self.ui.buttonBox.button(QDialogButtonBox.Save).hide()

		

