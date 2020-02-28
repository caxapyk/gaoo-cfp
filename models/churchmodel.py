from models import SqlTreeBaseModel


class ChurchModel(SqlTreeBaseModel):
    def __init__(self):
        super(ChurchModel, self).__init__()
        self.setTable("cfp_church")
        self.setForeignKey('locality_id')
        self.setDisplayName("церковь")
        self.setNewItemName("Новая церковь")
        self.setIconResource(":/icons/church-16.png")
