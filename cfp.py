import os
import sys
from application import Application
from PyQt5.QtCore import (QTranslator, QLocale)
from PyQt5.QtCore import QCoreApplication
import PyQt5


def main():
    pyqt = os.path.dirname(PyQt5.__file__)
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(pyqt, "Qt", "plugins")
    os.environ["LD_LIBRARY_PATH"] = os.path.join(pyqt, "Qt", "lib")
    app = Application(sys.argv)
    #app.addLibraryPath(os.path.join(pyqt, "Qt", "lib"))
    #qtTranslator = QTranslator()
    #if qtTranslator.load(QLocale(), ":/qtbase_ru.qm"):
    #    QCoreApplication.installTranslator(qtTranslator)
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
