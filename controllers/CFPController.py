from PyQt5.QtWidgets import QMainWindow
from PyQt5.uic import loadUi
from models.CFPModel import CFPModel
from models.GEOModel import GEOModel


from PyQt5.QtSql import QSqlQueryModel
from PyQt5.Qt import Qt


class CFPController(QMainWindow):

    def __init__(self):
        super(CFPController, self).__init__()
        self.ui = loadUi("ui/main_window.ui", self)

        self.table_view_cfp()
        self.tree_view_geo()

        self.show()

    def table_view_cfp(self):
        model = CFPModel()
        self.ui.tableView_cfp.setModel(model.select())

    def tree_view_geo(self):
        _model = QSqlQueryModel()
        _model.setQuery("SELECT * FROM cfp_gubernia")

        _model2 = QSqlQueryModel()
        _model2.setQuery("SELECT * FROM cfp_gubernia LEFT JOIN cfp_uezd ON cfp_gubernia.id = cfp_uezd.gubernia_id")
        #_model.setHeaderData(0, Qt.Horizontal, "Name")

        model = GEOModel(_model2)
        self.ui.treeView_geo.setModel(model)
