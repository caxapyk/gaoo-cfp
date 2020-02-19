from PyQt5.QtWidgets import (QItemDelegate, QLineEdit)


class YearItemDelegate(QItemDelegate):
    def __init__(self):
        super(YearItemDelegate, self).__init__()

        self.closeEditor.connect(self.validate)

    def createEditor(self, parent, option, index):
        self.index = index

        editor = QLineEdit(parent)
        editor.setInputMask("9999")

        return editor

    def validate(self, editor):
        if not editor.hasAcceptableInput():
            self.index.model().removeRows(self.index.model().rowCount() - 1, 1)
