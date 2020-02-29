from PyQt5.Qt import Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QDialog, QLabel, QLineEdit,
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

        self.fields = []

    def getText(self, title, label, text="", regex=None):

        self.setWindowTitle(title)

        self.label = QLabel(self)
        self.label.setText(label)

        self.line_edit = QLineEdit(self)
        self.line_edit.setFocus(Qt.OtherFocusReason)
        self.line_edit.setText(text)

        if regex:
            self.line_edit.setValidator(QRegExpValidator(regex))

        self.form_layout.setWidget(0, QFormLayout.LabelRole, self.label)
        self.form_layout.setWidget(0, QFormLayout.FieldRole, self.line_edit)

        self.fields.append(self.line_edit)

        res = self.exec_()
        if res == QDialog.Accepted:
            return (self.line_edit.text(), QDialog.Accepted)
        elif res == QDialog.Rejected:
            return (self.line_edit.text(), QDialog.Rejected)

    def getRange(self, title, regex=None):

        self.setWindowTitle(title)

        self.label_from = QLabel(self)
        self.label_from.setText("с ")

        self.label_to = QLabel(self)
        self.label_to.setText("по ")

        self.line_edit_from = QLineEdit(self)
        self.line_edit_from.setFocus(Qt.OtherFocusReason)

        self.line_edit_to = QLineEdit(self)

        if regex:
            self.line_edit_from.setValidator(QRegExpValidator(regex))
            self.line_edit_to.setValidator(QRegExpValidator(regex))

        self.form_layout.setWidget(0, QFormLayout.LabelRole, self.label_from)
        self.form_layout.setWidget(
            0, QFormLayout.FieldRole, self.line_edit_from)

        self.form_layout.setWidget(1, QFormLayout.LabelRole, self.label_to)
        self.form_layout.setWidget(1, QFormLayout.FieldRole, self.line_edit_to)

        self.fields.append(self.line_edit_from)
        self.fields.append(self.line_edit_to)

        res = self.exec_()

        _range = "%s:%s" % (self.line_edit_from.text(),
                            self.line_edit_to.text())

        if res == QDialog.Accepted:
            return (_range, QDialog.Accepted)
        elif res == QDialog.Rejected:
            return (_range, QDialog.Rejected)

    def accept(self):
        for widget in self.fields:
            if not widget.hasAcceptableInput():
                box = QMessageBox()
                box.critical(self, "Сохранение объекта",
                             "Ошибка при заполнении формы!", QMessageBox.Ok)
                return

        return super().accept()
