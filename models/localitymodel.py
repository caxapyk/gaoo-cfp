from models import SqlTreeBaseModel


class LocalityModel(SqlTreeBaseModel):
    def __init__(self):
        super(LocalityModel, self).__init__()
        self.setTable("cfp_locality")
        self.setForeignKey('uezd_id')
        self.setNewItemName("Новый населенный пункт")
