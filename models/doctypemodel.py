from PyQt5.QtSql import QSqlTableModel

class DoctypeModel(QSqlTableModel):
	def __init__(self):
	    super(DoctypeModel, self).__init__()

	    self.setTable("cfp_doctype")
