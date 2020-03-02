from .listviewdialog import ListViewDialog
from models import DoctypeModel


class DoctypeDialog(ListViewDialog):
    def __init__(self, parent):
        super(DoctypeDialog, self).__init__(parent)
        self.setWindowTitle("Справочник [Виды документов]")

        model = DoctypeModel()

        self.setModel(model)

        self.setInputTitle("Новый вид документа")
