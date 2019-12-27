from models import GEOBaseModel

"""
Uezd Model
"""


class UezdModel(GEOBaseModel):
    def __init__(self):
        super(UezdModel, self).__init__()
        self.setTable("cfp_uezd")
        self.setForeignKey('gub_id')
        self.setDisplayName("Уезд")
