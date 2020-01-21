from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QItemDelegate, QLineEdit)


class GeoItemDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)

        regex = QRegExp("^[(А-я-0-9.,)\\s]+$")
        validator = QRegExpValidator(regex)

        editor.setMaxLength(100)
        editor.setValidator(validator)

        return editor
