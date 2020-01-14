from models import GEOBaseModel


class GuberniaModel(GEOBaseModel):
    def __init__(self):
        super(GuberniaModel, self).__init__()
        self.setTable("cfp_gubernia")
        self.setNewItemName("Новая губерния")
