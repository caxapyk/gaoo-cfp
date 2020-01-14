from models import GEOBaseModel


class ChurchModel(GEOBaseModel):
    def __init__(self):
        super(ChurchModel, self).__init__()
        self.setTable("cfp_church")
        self.setForeignKey('locality_id')
        self.setNewItemName("Новая церковь")
        self.setIconResource(":/icons/church-16.png")
