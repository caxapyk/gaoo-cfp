from .listviewdialog import ListViewDialog
from models import DocflagModel


class DocflagDialog(ListViewDialog):
    def __init__(self, parent):
        super(DocflagDialog, self).__init__(parent)
        self.setWindowTitle(
            "Справочник [Метки документов (примечания)]")

        model = DocflagModel()

        self.setModel(model)

        self.setInputTitle("Новая метка")
