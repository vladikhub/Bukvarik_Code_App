from PyQt5 import QtWidgets, uic
from PyQt5.Qt import *
from StartLevels import Game
from FileSettings import Settings

# Класс, отвечающий за создание меню
class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        # загрузка окна Меню
        uic.loadUi('ui/menu.ui', self)

        # привязывание кнопки Начать к методу start_game() при нажатии
        self.start.clicked.connect(self.start_game)

        # привязывание кнопки Настройки к методу open_settings() при нажатии
        self.settings.clicked.connect(self.open_settings)

        self.setWindowTitle('Меню')
        self.language = 'ru'
        self.level = 3
        self.mode = 1
        self.lang_path = 'русский'

    # метод, который вызывает Game, отвечающий за Игровой процесс
    def start_game(self):
        self.game = Game(self, self.level, self.language, self.lang_path)

    # создание класса Settings, отвечающий за Настройки
    def open_settings(self):
        self.stns = Settings(self)
        self.stns.show()
        self.hide()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = Menu()
    win.show()
    sys.exit(app.exec_())
