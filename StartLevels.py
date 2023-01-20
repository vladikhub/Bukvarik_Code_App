from PyQt5 import QtWidgets
from PyQt5.Qt import *
from words import *
from AllLevels import First, Second, Third
import os, random, sys
# класс Game, отвечающий за Игровой процесс
class Game():
    # в инициализации класса передаются сслка на родителя, уровень, язык, путь до папки с картинками
    def __init__(self, parent=None, level=None, language=None, lang_path=None):
        super().__init__()
        self.menu = parent
        self.language = language
        self.len_word = level
        self.lang_path = lang_path

        # определение алфавита
        if self.language == 'ru': self.all_letters = all_letters_Russian; self.lang_path = 'русский'
        else: self.all_letters = all_letters_English; self.lang_path = 'английский'

        self.load_image_and_words()

        self.curr_word = 0
        self.curr_col = -1
        self.cur_level = 1

        self.one = False
        self.two = False
        self.three = False

        # определение шага, через сколько слов будет меняться уровень
        self.step_level = len(self.WORDS[self.len_word-3])//3
        if self.step_level == 0: self.step_level = 1
        self.startSecondLevel = self.step_level
        self.startThirdLevel = self.step_level*2

        self.set_level()

    # функция, отвечающая за выгузку картинок с папки и создание списка слов
    def load_image_and_words(self):
        self.path_3 = f'картинки/{self.lang_path}/картинки_3буквы'
        self.path_4 = f'картинки/{self.lang_path}/картинки_4буквы'
        self.path_5 = f'картинки/{self.lang_path}/картинки_5букв'
        self.path_6 = f'картинки/{self.lang_path}/картинки_6букв'
        self.PATH = [self.path_3, self.path_4, self.path_5, self.path_6]

        #создание словарей для привязки картинки к слову
        self.imgs_3 = {}
        for img in os.listdir(self.path_3):
            self.imgs_3[img.split('.')[0].upper()] = self.path_3 + '/' + img
        self.imgs_4 = {}
        for img in os.listdir(self.path_4):
            self.imgs_4[img.split('.')[0].upper()] = self.path_4 + '/' + img
        self.imgs_5 = {}
        for img in os.listdir(self.path_5):
            self.imgs_5[img.split('.')[0].upper()] = self.path_5 + '/' + img
        self.imgs_6 = {}
        for img in os.listdir(self.path_6):
            self.imgs_6[img.split('.')[0].upper()] = self.path_6 + '/' + img
        self.IMAGES = [self.imgs_3, self.imgs_4, self.imgs_5, self.imgs_6]
        self.words_3 = list(self.imgs_3.keys())
        self.words_4 = list(self.imgs_4.keys())
        self.words_5 = list(self.imgs_5.keys())
        self.words_6 = list(self.imgs_6.keys())
        random.shuffle(self.words_3)
        random.shuffle(self.words_4)
        random.shuffle(self.words_5)
        random.shuffle(self.words_6)
        self.WORDS = [self.words_3, self.words_4, self.words_5, self.words_6]

    # метод, где происходит вызов классов, отвечающих за уровни сложности, где передается выбранный язык, алфавит, список картинок и слов
    def set_level(self):
        # если количество загруженных слов меньше, чем три, то вызывается метод с ошибкой
        if len(self.WORDS[self.len_word-3]) < 3:
            self.errorCreate()

        # вызов первого уровня
        elif self.cur_level == 1:
            self.first = First(self, self.language, self.all_letters, self.IMAGES, self.WORDS)
            self.first.show()
            self.menu.hide()

        # вызов второго уровня
        elif self.cur_level == 2:
            self.second = Second(self, self.language, self.all_letters, self.IMAGES, self.WORDS)
            self.second.show()
            self.first.hide()

        # вызов третьего уровня
        elif self.cur_level == 3:
            self.third = Third(self, self.language, self.all_letters, self.IMAGES, self.WORDS)
            self.third.show()
            self.second.hide()

    # метод с ошибкой количества загруженных слов
    def errorCreate(self):
        error = QMessageBox()
        error.setWindowTitle('Ошибка')
        error.setText('Количество загруженных слов выбранной длины должно быть не меньее 3')
        error.setIcon(QMessageBox.Warning)
        error.setStandardButtons(QMessageBox.Ok)
        error.exec_()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    win = First()
    win.show()
    sys.exit(app.exec_())

