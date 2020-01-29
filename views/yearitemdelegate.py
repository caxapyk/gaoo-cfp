from PyQt5.QtWidgets import (QItemDelegate, QLineEdit)


class YearItemDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)

        editor.setInputMask("9999")

        return editor
