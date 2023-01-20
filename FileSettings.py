from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.Qt import *
from PyQt5.QtWidgets import QFileDialog
from words import *
import os

# класс Настройки
class Settings(QMainWindow):
    # в инициализации передается ссылка на родителя
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        # загрузка окна с Настройками
        uic.loadUi('ui/settings.ui', self)
        self.setWindowTitle('Настройки')

        self.ChooseDelWord.setEnabled(False)

        # привязывание клавиши Загрузить картинку к методу addImage() при нажатии
        self.addImgBut.clicked.connect(self.addImage)

        # привязывание кнопки Сохранить и выйти в меню к методу show_menu() при нажатии
        self.menuBut.clicked.connect(self.show_menu)

        # привязывание кнопки Выбрать к методу showListForDel() при нажатии
        self.chooseBut.clicked.connect(self.showListForDel)

        # привязывание кнопки Удалить к методу delImage() при нажатии
        self.deleteBut.clicked.connect(self.delImage)

    # метод, где при выборе языка и длине слова появляется список слов для удаления
    def showListForDel(self):
        if len(self.ChooseDelWord) != 0:
            self.ChooseDelWord.clear()
        lang = self.ChooseLangForDel.currentText()
        length = int(self.ChooseLenWordForDel.currentText()[0])

        # выбор путя к картинке
        Path_for_del = [f'картинки/{lang}/картинки_3буквы', f'картинки/{lang}/картинки_4буквы',
                             f'картинки/{lang}/картинки_5букв', f'картинки/{lang}/картинки_6букв']
        path = Path_for_del[length - 3]

        wrds = []
        for img in os.listdir(path):
            wrds.append(img.split('.')[0])

        # загрузка слов для выбора
        for w in wrds:
            self.ChooseDelWord.addItem(w)
        self.ChooseDelWord.setEnabled(True)

    # метод для выбора языка при загрузки Игрового процесса
    def chooseLang_Game(self):
        lang = self.languageBut.currentText()
        if lang == 'русский':
            language = 'ru'
        else:
            language = 'en'
        return language

    # метод для удаления картинки со словом
    def delImage(self):
        # сичтывание слова
        word = self.ChooseDelWord.currentText()
        lang = self.ChooseLangForDel.currentText()
        length = int(self.ChooseLenWordForDel.currentText()[0])
        if word != '':
            # выбор путя, откуда будет удаляться картинка
            Path_for_del = [f'картинки/{lang}/картинки_3буквы', f'картинки/{lang}/картинки_4буквы',
                            f'картинки/{lang}/картинки_5букв', f'картинки/{lang}/картинки_6букв']
            path = Path_for_del[length - 3]
            wrds = {}
            for img in os.listdir(path):
                wrds[img.split('.')[0]] = img.split('.')[1]
            # удаление картинки
            os.remove(f'{path}/{word}.{wrds[word]}')
            self.ChooseDelWord.clear()
            self.ChooseDelWord.setEnabled(False)

    # метод для загрузки новой картинки
    def addImage(self):
        # выбор языка
        lang = self.ChooseLangForAdd.currentText()

        # выбор пути загрузки
        Path_for_add = [f'картинки/{lang}/картинки_3буквы', f'картинки/{lang}/картинки_4буквы',
                             f'картинки/{lang}/картинки_5букв', f'картинки/{lang}/картинки_6букв']

        # открытия окна для выбора картинки на компьютере
        file = QFileDialog.getOpenFileName(self,
            'Выберете картинку',
            '/Загрузки',
            'Все файлы (*);;Картинка (*.jpg);;Картинка (*.jpeg);;Картинка (*.png)'
            )[0]

        # проверка на правильность названия картинки
        if file != '':
            name = file.split('/')[-1]

            lenWord = int(self.ChooseLenWordBut.currentText()[0])
            print(name.split('.')[0])

            # при неправильном написании вызов метода errorCreate()
            if self.ChooseLangForAdd.currentText() == 'русский' and any(let in all_letters_English or let in all_letters_English_Low for let in name.split('.')[0]):
                self.errorCreate('language')
            elif self.ChooseLangForAdd.currentText() == 'английский' and any(let in all_letters_Russian or let in all_letters_Russian_Low for let in name.split('.')[0]):
                self.errorCreate('language')
            elif lenWord != len(name.split('.')[0]):
                self.errorCreate('length')
            else:
                # добваления новой картинки
                path = Path_for_add[lenWord-3]
                os.replace(file, f'{path}/{name}')
        self.show()

    # метод для возвращения в меню с запоминанием параметров для Игрового режима (язык и длина слова)
    def show_menu(self):
        self.parent.language = self.chooseLang_Game()
        self.parent.show()
        self.parent.level = int(self.gameLvlSetup.currentText()[0])

        self.hide()

    # метод для вывода ошибки
    def errorCreate(self, reason=None):

        error = QMessageBox()
        error.setWindowTitle('Ошибка')
        if reason == 'length':
            error.setText('Длинна названия картинки должно соответствовать выбранной вами длине слова')
        elif reason == 'language':
            error.setText('Проверьте язык, на котором написано выбранное слово')
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)

        error.buttonClicked.connect(self.show)

        error.exec_()

    def closeEvent(self, event):
        self.parent.show()
        event.accept()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    win = Settings()

    win.show()
    sys.exit(app.exec_())
