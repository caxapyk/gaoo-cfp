from models import GEOBaseModel

"""
Locality Model
"""


class LocalityModel(GEOBaseModel):
    def __init__(self):
        super(LocalityModel, self).__init__()
        self.setTable("cfp_locality")
        self.setForeignKey('uezd_id')
        self.setDisplayName("Населенный_пункт")
