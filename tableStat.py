from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.Qt import *
from PyQt5.QtWidgets import QFileDialog
from words import *
import random
import os
from StartLevels import First, Third, Game


class TableStat(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('ui/statistics.ui', self)
        self.parent = parent
        self.fill()
        data = [('Смольков', '23.12', )]

    def fill(self):
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels([
            'Пользователь', 'Дата', 'Глаз', 'Ошибки', 'Режим'
        ])


    def closeEvent(self, event):
        self.parent.show()
        event.accept()



    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle("Настройки")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = TableStat()

    win.show()
    sys.exit(app.exec_())
