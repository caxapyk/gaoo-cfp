from PyQt5.QtWidgets import (QDialog)
from PyQt5.uic import loadUi
from models import ChurchDTModel


class SetDTDialog(QDialog):
    def __init__(self, index):
        super(SetDTDialog, self).__init__()
        self.ui = loadUi("ui/set_dt_dialog.ui", self)

        self.model = ChurchDTModel(index.internalPointer().uid())
        self.model.refresh()

        self.ui.listView_doctype.setModel(self.model)
        self.ui.listView_doctype.setModelColumn(1)

        self.show()
