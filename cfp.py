import sys
from application import Application
from PyQt5.QtCore import (QTranslator, QLocale)
from PyQt5.QtCore import QCoreApplication
import PyQt5


def main():
    app = Application(sys.argv)
    #qtTranslator = QTranslator()
    #if qtTranslator.load(QLocale(), ":/qtbase_ru.qm"):
    #    QCoreApplication.installTranslator(qtTranslator)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
