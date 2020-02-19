from .listviewdialog import ListViewDialog
from models import FundModel


class FundDialog(ListViewDialog):
    def __init__(self, parent, model=None):
        super(FundDialog, self).__init__(parent)
        self.setWindowTitle("Справочник [Фонды]")

        if not model:
            model = FundModel()
            model.select()

        self.setModel(model)
