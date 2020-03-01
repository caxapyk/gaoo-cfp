from PyQt5.QtWidgets import (QWidget, QDialogButtonBox, QComboBox,
                             QLineEdit, QSpinBox, QListView, QTextEdit, QPlainTextEdit, QPushButton)
from dialogs import DocFormDialog


class DocViewDialog(DocFormDialog):
    def __init__(self, parent, model, row=None):
        super(DocViewDialog, self).__init__(parent, model, row)

        self.setWindowTitle("Просмотр документа [%s]" % super().storageUnit())
        for widget in self.ui.tabWidget.findChildren(
                (QComboBox,
                    QLineEdit,
                    QSpinBox,
                    QTextEdit,
                    QPlainTextEdit,
                    QPushButton)):
            if isinstance(widget, QComboBox):
                widget.setDisabled(True)
                widget.setStyleSheet("color: black")
            elif isinstance(widget, QPushButton):
                widget.hide()
            else:
                widget.setReadOnly(True)

        self.flags_model.setReadOnly(True)

        self.ui.buttonBox.button(QDialogButtonBox.Save).hide()
