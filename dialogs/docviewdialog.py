from PyQt5.QtWidgets import (QWidget, QDialogButtonBox)
from dialogs import DocFormDialog


class DocViewDialog(DocFormDialog):
	def __init__(self, parent, model, row=None):
		super(DocViewDialog, self).__init__(parent, model, row)

		self.setWindowTitle("Просмотр документа [%s]" % super().storageUnit())
		#for widget in self.ui.tabWidget.findChildren(QWidget):
		#    widget.setStyleSheet("color: black")

		self.ui.tab_main.setDisabled(True)
		self.ui.tab_add.setDisabled(True)
		self.ui.yearInsert_pushButton.hide()
		self.ui.yearRemove_pushButton.hide()
		self.ui.buttonBox.button(QDialogButtonBox.Save).hide()

		

