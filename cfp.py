import os
import sys
import resources
import PyQt5
from PyQt5.QtCore import (QTranslator, QLocale)
from application import Application


def main():
    pyqt = os.path.dirname(PyQt5.__file__)
    os.environ["QT_QPA_PLATFORM_PLUGIN_PATH"] = os.path.join(
        pyqt, "Qt", "plugins")
    os.environ["LD_LIBRARY_PATH"] = os.path.join(pyqt, "Qt", "lib")
    app = Application(sys.argv)

    qtTranslator = QTranslator()
    if qtTranslator.load(QLocale(), ":/qtbase_ru.qm"):
        app.installTranslator(qtTranslator)

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
