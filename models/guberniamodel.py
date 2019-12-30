from PyQt5.QtSql import QSqlQueryModel
from models import GEOBaseModel

"""
Gubernia Model
"""


class GuberniaModel(GEOBaseModel):
    def __init__(self):
        super(GuberniaModel, self).__init__()
        self.setTable("cfp_gubernia")
        self.setNewItemName("Губерния")
