from PyQt5.Qt import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QItemDelegate, QLineEdit, QMessageBox)


class ListViewDelegate(QItemDelegate):
    def __init__(self):
        super(ListViewDelegate, self).__init__()
        self.closeEditor.connect(self.validate)

    def createEditor(self, parent, option, index):
        self.parent = parent
        self.index = index

        editor = QLineEdit(self.parent)

        regex = QRegExp("^[(А-яA-z-0-9.,)\\s]+$")
        editor.setValidator(QRegExpValidator(regex))

        return editor

    def validate(self, editor):
        if not editor.hasAcceptableInput():
            self.index.model().revert()

    def setModelData(self, editor, model, index):
        if editor.hasAcceptableInput():
            if not model.setData(index, editor.text()) or not model.submit():
                model.revert()
                QMessageBox().critical(self.parent, "Сохранение объекта",
                                       "Не удалось сохранить объект!\n\nДубликат записи или возможно у Вас недостаточно привилегий.", QMessageBox.Ok)
