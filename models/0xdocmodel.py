from PyQt5.Qt import Qt
from PyQt5.QtCore import QModelIndex, QAbstractItemModel
from PyQt5.QtSql import QSqlQuery, QSqlRecord, QSqlField
from utils import AbbrMaker


class DocModel(QAbstractItemModel):
    def __init__(self):
        super(DocModel, self).__init__()

        self.__data = []
        self.__cols__ = 0
        self.__headers__ = {}

        self.__query__ = None
        self.__blank_record__ = None
        self.__filter_str__ = None
        self.__last_insert_id__ = None
        self.__church_id__ = None
        self.__current_idx__ = QModelIndex()

    def rowCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return len(self.__data)
        else:
            return 0

    def columnCount(self, parent=QModelIndex()):
        if not parent.isValid():
            return self.__cols__
        else:
            return 0

    def index(self, row, column, parent=QModelIndex()):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()

        item = self.__data[row]
        index = self.createIndex(row, column, item)

        return index

    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        return index

    def data(self, item, role):
        if not item.isValid():
            return None

        if role != Qt.DisplayRole and role != Qt.EditRole:
            return None

        if item.column() == 11:
            return item.row() + 1

        elif item.column() == 12:
            rec = self.record(item.row())
            doctype_abbr = AbbrMaker().make(
                rec.value("cfp_doctype.name"))

            return doctype_abbr

        elif item.column() == 13:
            rec = self.record(item.row())

            storage_unit = "Ф. %s Оп. %s Д. %s" % (
                rec.value("cfp_doc.fund"),
                rec.value("cfp_doc.inventory"),
                rec.value("cfp_doc.unit"))

            return storage_unit

        elif item.column() == 16:
            rec = self.record(item.row())

            flags_list = ""
            for flag in rec.value("flags").split(","):
                flags_list += "%s/" % AbbrMaker().make(flag)

            return flags_list[:-1]

        return self.__data[item.row()].value(item.column())

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            return self.__headers__[section]

        return super().headerData(section, orientation, role)

    def setData(self, index, value, role=Qt.EditRole):
        self.__data[index.row()].setValue(index.column(), value)
        return True

    def setHeaderData(self, section, orientation, value, role=Qt.DisplayRole):
        self.__headers__[section] = value
        self.headerDataChanged.emit(orientation, section, section)
        return True

    def insertColumns(self, column, count, parent=QModelIndex()):
        i = 0
        while i < count:
            field = QSqlField("column_" + str(column + i))

            for item in self.__data:
                item.insert(column + i, field)

            self.__blank_record__.insert(column + i, field)
            i += 1

        self.__cols__ += count

        return True

    def insertRows(self, row, count, parent=QModelIndex()):
        self.beginInsertRows(parent, row, row)
        self.endInsertRows()

        return True

    def removeRows(self, row, count, parent=QModelIndex()):
        self.beginRemoveRows(parent, row, row)

        del self.__data[row]

        self.endRemoveRows()

        return True

    def insertRecord(self, pos, record):
        if self.insertRows(self.rowCount(), 1):
            self.__data.append(record)
            self.setCurrentIndex(self.rowCount())

            return True

        return False

    def refresh(self):
        query = "SELECT \
        cfp_doc.id AS `cfp_doc.id`, \
        cfp_gubernia.name AS `cfp_gubernia.name`, \
        cfp_uezd.name AS `cfp_uezd.name`, \
        cfp_locality.name AS `cfp_locality.name`, \
        cfp_church.name AS `cfp_church.name`, \
        cfp_doc.church_id AS `cfp_doc.church_id`, \
        cfp_doctype.name AS `cfp_doctype.name`, \
        cfp_doc.doctype_id AS `cfp_doc.doctype_id`, \
        cfp_doc.fund AS `cfp_doc.fund`, \
        cfp_doc.inventory AS `cfp_doc.inventory`, \
        cfp_doc.unit AS `cfp_doc.unit`, \
        cfp_doc.sheets AS `cfp_doc.sheets`, \
        (SELECT GROUP_CONCAT(cfp_docyears.year ORDER BY cfp_docyears.year) FROM cfp_docyears WHERE cfp_docyears.doc_id = cfp_doc.id) AS years, \
        (SELECT GROUP_CONCAT(cfp_docflag.name ORDER BY cfp_docflag.name) FROM cfp_docflags LEFT JOIN cfp_docflag ON cfp_docflags.docflag_id=cfp_docflag.id WHERE cfp_docflags.doc_id = cfp_doc.id) AS flags, \
        cfp_doc.comment AS `cfp_doc.comment` \
        FROM cfp_doc \
        LEFT JOIN cfp_church ON cfp_doc.church_id = cfp_church.id \
        LEFT JOIN cfp_locality ON cfp_church.locality_id = cfp_locality.id \
        LEFT JOIN cfp_uezd ON cfp_locality.uezd_id = cfp_uezd.id \
        LEFT JOIN cfp_gubernia ON cfp_uezd.gub_id = cfp_gubernia.id \
        LEFT JOIN cfp_doctype ON cfp_doc.doctype_id=cfp_doctype.id"

        if self.filter():
            query += " WHERE " + self.filter()

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return None

        self.__blank_record__ = sql_query.record()
        self.__cols__ = sql_query.record().count()

        self.setQuery(sql_query)

        # fill local data list by QSqlRecord(s)
        self.__data.clear()
        while sql_query.next():
            self.__data.append(sql_query.record())

        # insert columns for counter/type abbr/storage unit fields
        self.insertColumns(11, 3)
        # insert column for flags abbr
        self.insertColumns(16, 1)

        self.setHeaderData(0, Qt.Horizontal, "Идентификатор документа")
        self.setHeaderData(1, Qt.Horizontal, "Губерния")
        self.setHeaderData(2, Qt.Horizontal, "Уезд")
        self.setHeaderData(3, Qt.Horizontal, "Населенный пункт")
        self.setHeaderData(4, Qt.Horizontal, "Наименование церкви")
        self.setHeaderData(5, Qt.Horizontal, "Идентификатор церкви")
        self.setHeaderData(6, Qt.Horizontal, "Тип документа")
        self.setHeaderData(7, Qt.Horizontal, "Идентификатор типа документа")
        self.setHeaderData(8, Qt.Horizontal, "Фонд")
        self.setHeaderData(9, Qt.Horizontal, "Опись")
        self.setHeaderData(10, Qt.Horizontal, "Дело")
        self.setHeaderData(11, Qt.Horizontal, "#")  # inserted
        self.setHeaderData(12, Qt.Horizontal, "Тип документа")  # inserted
        self.setHeaderData(13, Qt.Horizontal, "Ед. хранения")  # inserted
        self.setHeaderData(14, Qt.Horizontal, "Листов")
        self.setHeaderData(15, Qt.Horizontal, "Годы документов")
        self.setHeaderData(16, Qt.Horizontal, "Флаги")  # inserted
        self.setHeaderData(17, Qt.Horizontal, "Флаги")
        self.setHeaderData(18, Qt.Horizontal, "Комментарий")

    def submitAll(self):
        if self.currentIndex().isValid():
            query = "UPDATE cfp_doc SET church_id=?, doctype_id=?, fund=?, \
                inventory=?, unit=?, sheets=?, comment=? WHERE id=?"
        else:
            query = "INSERT INTO cfp_doc \
                (church_id, doctype_id, fund, inventory, unit, sheets, \
                comment) VALUES(?,?,?,?,?,?,?)"

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        rec = self.record(self.currentIndex().row())

        sql_query.addBindValue(rec.value("cfp_doc.church_id"))
        sql_query.addBindValue(rec.value("cfp_doc.doctype_id"))
        sql_query.addBindValue(rec.value("cfp_doc.fund"))
        sql_query.addBindValue(rec.value("cfp_doc.inventory"))
        sql_query.addBindValue(rec.value("cfp_doc.unit"))
        sql_query.addBindValue(rec.value("cfp_doc.sheets"))
        sql_query.addBindValue(rec.value("cfp_doc.comment"))

        if self.currentIndex().isValid():
            sql_query.addBindValue(rec.value("cfp_doc.id"))

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return False

        doc_id = sql_query.lastInsertId()
        if doc_id is not None:
            # set id to new inserted row
            rec.setValue(0, doc_id)
            self.setLastInsertId(doc_id)

            self.setCurrentIndex(self.rowCount() - 1)

        return True

    def remove(self, doc_id):
        # docyears and docflags removes by ON CASCADE MYSQL feature
        query = "DELETE FROM cfp_doc WHERE id=%s" % doc_id

        sql_query = QSqlQuery()
        sql_query.prepare(query)

        print(sql_query.lastQuery())

        if not sql_query.exec_():
            print(sql_query.lastError().text())
            return False

        return True

    def setQuery(self, query):
        self.__query__ = query

    def query(self):
        if self.__query__:
            return self.__query__
        return QSqlQuery()

    def setLastInsertId(self, lid):
        self.__last_insert_id__ = lid

    def lastInsertId(self):
        return self.__last_insert_id__

    def setFilter(self, f_str):
        self.__filter_str__ = f_str

    def filter(self):
        return self.__filter_str__

    def record(self, row):
        return self.__data[row]

    def emptyRecord(self):
        if self.query().isActive():
            return QSqlRecord(self.__blank_record__)
        return QSqlRecord()

    def setChurch(self, id):
        self.__church_id__ = id

    def churchId(self):
        return self.__church_id__

    def setCurrentIndex(self, row):
        self.__current_idx__ = self.index(row, 0)

    def currentIndex(self):
        return self.__current_idx__
