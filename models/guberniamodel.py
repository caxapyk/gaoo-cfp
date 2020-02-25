from models import SqlTreeBaseModel


class GuberniaModel(SqlTreeBaseModel):
    def __init__(self):
        super(GuberniaModel, self).__init__()
        self.setTable("cfp_gubernia")
        self.setDisplayName("губерния")
        self.setNewItemName("Новая губерния")
