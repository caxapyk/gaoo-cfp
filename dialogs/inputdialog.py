from PyQt5.Qt import Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit, QFrame,
                             QMessageBox, QFormLayout, QVBoxLayout, QDialogButtonBox)


class InputDialog(QDialog):
    def __init__(self, parent):
        super(InputDialog, self).__init__(parent)

        self.v_layout = QVBoxLayout(self)

        self.form_layout = QFormLayout()
        self.form_layout.setContentsMargins(0, 0, 0, 0)
        self.form_layout.setSpacing(5)

        self.button_box = QDialogButtonBox(self)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(
            QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.v_layout.addLayout(self.form_layout)
        self.v_layout.addWidget(self.button_box)

        self.widget = None

    def getText(self, title, label, text="", regex=None):

        self.setWindowTitle(title)

        self.label = QLabel(self)
        self.label.setText(label)

        self.line_edit = QLineEdit(self)
        self.line_edit.setText(text)

        self.widget = self.line_edit

        if regex:
            self.line_edit.setValidator(QRegExpValidator(regex))

        self.form_layout.setWidget(0, QFormLayout.LabelRole, self.label)
        self.form_layout.setWidget(0, QFormLayout.FieldRole, self.line_edit)

        res = self.exec_()
        if res == QDialog.Accepted:
            return (self.line_edit.text(), QDialog.Accepted)
        elif res == QDialog.Rejected:
           return (self.line_edit.text(), QDialog.Rejected)

    def accept(self):
        if self.widget.hasAcceptableInput():
            return super().accept()
        else:
            QMessageBox().critical(self, "Сохранение объекта",
                                   "Ошибка при заполнении формы!", QMessageBox.Ok)