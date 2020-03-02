from .listviewdialog import ListViewDialog
from models import FundModel


class FundDialog(ListViewDialog):
    def __init__(self, parent):
        super(FundDialog, self).__init__(parent)
        self.setWindowTitle("Справочник [Фонды]")

        model = FundModel()

        self.setModel(model)

        self.setInputTitle("Новый фонд")
        self.setInputLabel("Фонд №")
