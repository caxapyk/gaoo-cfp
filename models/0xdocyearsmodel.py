from PyQt5.QtSql import QSqlTableModel, QSqlRecord


class DocYearsModel(QSqlTableModel):
    def __init__(self):
        super(DocYearsModel, self).__init__()

        self.setTable("cfp_docyears")

        self.doc_id = None

    def setDocId(self, doc_id):
        self.setFilter("doc_id=%s" % doc_id)
        self.doc_id = doc_id

    def insertRecord(self, row, record=QSqlRecord()):
        if record.isEmpty():
            print("empty")
            rec = self.record()
            rec.remove(rec.indexOf("id"))
            # set Null if doc_id is None (for a new doc)
            if self.doc_id is None:
                rec.setNull("doc_id")
            else:
                rec.setValue("doc_id", self.doc_id)

            rec.setValue("year", "")

            return super().insertRecord(row, rec)
        else:
            return super().insertRecord(row, record)

    # def sumbitAll():
    #   return True
