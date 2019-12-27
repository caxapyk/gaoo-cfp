from models import GEOBaseModel

"""
Church Model
"""


class ChurchModel(GEOBaseModel):

    def __init__(self):
        super(ChurchModel, self).__init__()
        self.setTable("cfp_church")
        self.setForeignKey('locality_id')
        self.setDisplayName("Церковь")
