from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.Qt import *
from words import BG


class GuessWord(QMainWindow):
    def __init__(self, parent=None, col=None):
        super().__init__()

        uic.loadUi('congratulations.ui', self)
        self.parent = parent
        self.NextBut.clicked.connect(self.closeWord)
        self.setStyleSheet(BG[col])
    def closeWord(self):
        self.hide()
        self.parent.show()
    def closeEvent(self, event):
        self.parent.show()
        event.accept()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle("Поздравляю")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = GuessWord()

    win.show()
    sys.exit(app.exec_())
