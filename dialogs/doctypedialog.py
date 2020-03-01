from .listviewdialog import ListViewDialog
from models import DoctypeModel


class DoctypeDialog(ListViewDialog):
    def __init__(self, parent, model=None):
        super(DoctypeDialog, self).__init__(parent)
        self.setWindowTitle("Справочник [Виды документов]")

        if not model:
            model = DoctypeModel()

        self.setModel(model)
