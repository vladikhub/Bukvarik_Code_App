from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.Qt import *
from words import *
import random

# класс Первого уровня сложности
class First(QMainWindow):
    # инициализация класса с чтением переадаемой ссылки на родителя,
    # языка, алфавитом, списком картинок и слов
    def __init__(self, parent=None, language=None,
                 all_letters=None, images=None, words=None):
        super().__init__()

        # загрузка окна Игрового процесса
        uic.loadUi('ui/game.ui', self)
        self.setWindowTitle('Игра')

        self.parent = parent
        self.language = language
        self.IMAGES = images
        self.WORDS = words
        self.alphabet = all_letters
        self.all_words = len(self.WORDS[self.parent.len_word-3])

        self.all_buttons = []
        self.need_word = []

        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(60, 30, 320, 240))
        self.image.setText("")
        self.image.setObjectName("image")

        # привязывание таймера timer1 к методу timer_end()
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.timer_end)

        # привязывание таймера timer2 к методу swipeToNewWord()
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.swipeToNewWord)

        self.load_True_image()
        self.load_False_image()
        self.hide_F_T()

        self.help.setText('Подсказка')

        self.set_letters_level()
        self.set_new_word()
        self.set_ans_squares()

        # привязка кнопок к методу press при нажатии
        for but in self.all_buttons:
            but.clicked.connect(self.press)

        self.help.clicked.connect(self.show_help)
        self.backMenu.clicked.connect(self.show_menu)

    # метод для устаноки цвета заднего фона
    def set_color(self):
        self.parent.curr_col += 1
        if self.parent.curr_col > 2:
            self.parent.curr_col = 0
        self.setStyleSheet(BG[self.parent.curr_col])

    # метод для обработки кнопок при нажатии
    def press(self):
        # считывание буквы на кнопке
        letter = self.sender().text()

        name = self.sender().objectName()
        index = self.copy_word.find(letter)
        show = False

        # проверка, есть ли такая буква в слове и правильный ли у нее порядок
        if letter in self.right_word and index == 0:
            getattr(self, name).setStyleSheet(BUT_BG[self.parent.curr_col])
            getattr(self, name).setEnabled(False)

            for i in range(len(self.right_word)):
                # если буква не показана, то показываем
                if self.need_word[i].text() == '' and not show:

                    # показывается картинка галочка на время
                    self.show_True()
                    self.timer1.start(1500)

                    # отображение отгаданной буквы
                    self.need_word[i].setText(self.copy_word[0])

                    self.copy_word = self.copy_word[1:]

                    self.help.setText('Подсказка')
                    show = True
        else:
            # если буква неправильная, показывается крестик на время
            self.show_False()
            self.timer1.start(1500)

        # проверка на конец слова
        self.checking_word_ending()

    # метод, где показывается подсказка
    def show_help(self):
        if self.help.text() == self.copy_word[0]:
            self.help.setText('Подсказка')
        else:
            self.help.setText(self.copy_word[0])

    # метод, где показывается галочка
    def show_True(self):
        self.Right.show()
        self.Right_fr.show()
        self.False_fr.hide()
        self.False_.hide()

    # Мметод, где показывается крестик
    def show_False(self):
        self.Right_fr.hide()
        self.Right.hide()
        self.False_fr.show()
        self.False_.show()

    # метод, где удаляются все буквы на кнопках
    def but_clear(self):
        for but in self.all_buttons:
            but.setText('')
            but.setEnabled(True)
            but.setStyleSheet(WHITE_BUT)

    # метод перехода на новое слово
    def swipeToNewWord(self):
        self.but_clear()
        self.set_new_word()

        self.timer2.stop()

    # метод для проверки на конец слова
    def checking_word_ending(self):
        if len(self.copy_word) == 0:
            self.timer2.start(700)
            self.parent.curr_word += 1

    # метод для того, чтобы скрыть картинки крестик и галочка
    def timer_end(self):
        self.Right.hide()
        self.Right_fr.hide()
        self.False_fr.hide()
        self.False_.hide()

    # метод при создании нового слова
    def set_new_word(self):

        # если счетчик прошедших слов равен количеству слов для перехода,
        # вызывается метод set_level() у родителя
        if self.parent.curr_word == self.parent.startSecondLevel:
            self.parent.cur_level += 1
            self.parent.set_level()

        self.level_name.setText(f' Уровень {self.parent.cur_level}')

        # установка цвета
        self.set_color()

        self.hide_F_T()

        # выбор правильного слова
        self.right_word = self.WORDS[self.parent.len_word-3][self.parent.curr_word]
        self.copy_word = self.right_word

        for i in self.need_word:
            i.setText('')

        # загрузка картинки
        self.new_image()

        # появление букв на кнопках для выбора
        self.show_choose_letters()

    # метод для отрисовка ячеек для правильного слова под картинкой
    def set_ans_squares(self):
        x0 = 10
        font = QtGui.QFont('Arial')
        font.setPointSize(36)
        for x in range(self.parent.len_word):
            a = 80
            w_count = 1
            if x != 0:
                x0 += a
            setattr(self, 'l' + str(w_count), QtWidgets.QLabel(self.centralwidget))
            getattr(self, 'l' + str(w_count)).setGeometry(QtCore.QRect(x0, 340, 60, 60))
            getattr(self, 'l' + str(w_count)).setFont(font)
            getattr(self, 'l' + str(w_count)).setStyleSheet("background-color: rgb(255, 255, 255);")
            getattr(self, 'l' + str(w_count)).setText("")
            getattr(self, 'l' + str(w_count)).setAlignment(QtCore.Qt.AlignCenter)
            getattr(self, 'l' + str(w_count)).setWordWrap(False)
            self.need_word.append(getattr(self, 'l' + str(w_count)))
            w_count += 1

    # метод для подписания кнопок буквой
    def show_choose_letters(self):
        # список букв для отрисовки
        letters_for_choose = self.make_letters_for_choosing()

        # отрисовка букв для выбора
        for i in range(len(letters_for_choose)):
            self.all_buttons[i].setText(letters_for_choose[i])

    # метод для создания списка букв для отрисовки
    def make_letters_for_choosing(self):
        # сначала буквы, которые есть в слове
        list_right_word = [i for i in self.right_word]
        letters_for_choose = [i for i in self.right_word]

        btw = len(self.all_buttons) - len(letters_for_choose)
        i = 0
        while btw != 0:
            # добавление букв в список
            if self.alphabet[i] not in list_right_word:
                letters_for_choose.append(self.alphabet[i])
                btw -= 1
                i += 1
            else:
                i += 1
        random.shuffle(letters_for_choose)
        return letters_for_choose

    # метод для загрузки картинки
    def new_image(self):
        pixmap = QPixmap(self.IMAGES[self.parent.len_word - 3][self.right_word])
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)

    # метод для расставления кнопок на свои места
    def set_letters_level(self):
        self.all_buttons = []
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(45)
        font.setBold(False)
        font.setWeight(60)
        w_count = 1
        a = 100
        b = 130
        for y in range(5):
            if y % 2 == 0:
                x0 = 150 - b
            else:
                x0 = 150
            for x in range(4):
                if x % 2 == 0:
                    x0 += b
                else:
                    x0 += a
                setattr(self, 'w' + str(w_count), QtWidgets.QPushButton(self.ButWidget))
                getattr(self, "w" + str(w_count)).setGeometry(QtCore.QRect(x0, 80 + y * 160, 80, 80))
                getattr(self, "w" + str(w_count)).setFont(font)
                getattr(self, "w" + str(w_count)).setStyleSheet("background-color: rgb(255, 255, 255);")
                getattr(self, "w" + str(w_count)).setText("")
                getattr(self, "w" + str(w_count)).setObjectName("w" + str(w_count))
                self.all_buttons.append(getattr(self, 'w' + str(w_count)))
                w_count += 1

    # при закрытии окна появление Меню
    def closeEvent(self, event):
        self.parent.menu.show()
        event.accept()

    # загрузка картинки крестик
    def load_False_image(self):
        False_pixmap = QPixmap(FALSE_IMG)
        self.False_.setPixmap(False_pixmap)
        self.False_.setScaledContents(True)

    # загрузка картинки галочка
    def load_True_image(self):
        Right_pixmap = QPixmap(RIGHT_IMG)
        self.Right.setPixmap(Right_pixmap)
        self.Right.setScaledContents(True)

    # скрытие картинок крести и галочка
    def hide_F_T(self):
        self.False_.hide()
        self.Right.hide()
        self.Right_fr.hide()
        self.False_fr.hide()

    # открытие окна Меню
    def show_menu(self):
        self.parent.menu.show()
        self.hide()

# Классы для создания уровней 2 и 3 практически не отличаются методами -
# - изменяются только методы set_letters_level(), set_new_word(), set_color().
# Поэтому здесь наследуются классы уровня 2 и 3 от класса уровня 1 и переписываются методы

# класс для уровня 2
class Second(First):
    # инициализация класса с чтением переадаемой ссылки на родителя,
    # языка, алфавитом, списком картинок и слов
    def __init__(self, parent=None, language=None,
                 all_letters=None, images=None, words=None):
        self.parent = parent
        self.language = language
        self.alphabet = all_letters
        self.IMAGES = images
        self.WORDS = words

        # инициализация класса, от которогонаследован класс 2
        First.__init__(self, parent=self.parent, language=self.language,
                       all_letters=self.alphabet, images=self.IMAGES, words=self.WORDS )

    # метод для расставления кнопок на свои места
    def set_letters_level(self):
        self.all_buttons = []
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(70)
        first_count = 0
        w_count = 1
        step_list = [50, 0, 50, 120]
        step_count = 0
        for y in range(11):
            start_point = 600
            x0 = start_point + step_list[step_count]
            a = 100
            step_count += 1
            if step_count > 3:
                step_count = 0
            for x in range(4):
                if y == 0 or y == 10:
                    first_count += 1
                    if first_count > 2:
                        break
                    b = 240
                    if x == 1:
                        x0 += 140
                elif y % 2 == 0:
                    a = 120
                    b = 120
                    first_count = 0
                else:
                    first_count = 0
                    b = 140
                    a = 100
                setattr(self, 'w' + str(w_count), QtWidgets.QPushButton(self.centralwidget))
                getattr(self, "w" + str(w_count)).setGeometry(QtCore.QRect(x0, 20 + y * 80, 60, 60))
                getattr(self, "w" + str(w_count)).setFont(font)
                getattr(self, "w" + str(w_count)).setStyleSheet("background-color: rgb(255, 255, 255);")
                getattr(self, "w" + str(w_count)).setText("")
                getattr(self, "w" + str(w_count)).setObjectName("w" + str(w_count))
                self.all_buttons.append(getattr(self, 'w' + str(w_count)))
                w_count += 1
                if x % 2 == 0:
                    x0 += a
                else:
                    x0 += b

    # метод при создании нового слова
    def set_new_word(self):
        # если счетчик прошедших слов равен количеству слов для перехода,
        # вызывается метод set_level() у родителя
        if self.parent.curr_word == self.parent.startThirdLevel:
            self.parent.cur_level += 1
            self.parent.set_level()

        self.level_name.setText(f' Уровень {self.parent.cur_level}')

        # загрузка цвета
        self.set_color()

        self.hide_F_T()

        # выбор слова
        self.right_word = self.WORDS[self.parent.len_word-3][self.parent.curr_word]
        self.copy_word = self.right_word

        # удаление прошлых букв
        for i in self.need_word:
            i.setText('')

        # загрузка картинки
        self.new_image()

        # появление букв на выбор
        self.show_choose_letters()

    # загрузка цвета
    def set_color(self):
        self.parent.curr_col += 1
        if self.parent.curr_col > 2:
            self.parent.curr_col = 0
        self.setStyleSheet(BG[self.parent.curr_col])

        # синхронизация цвета
        if self.parent.curr_word == self.parent.startSecondLevel:
            self.parent.curr_col -= 1

# класс для уровня 3
class Third(First):
    # если счетчик прошедших слов равен количеству слов для перехода,
    # вызывается метод set_level() у родителя
    def __init__(self, parent=None, language=None,
                 all_letters=None, images=None, words=None):
        self.parent = parent
        self.language = language
        self.alphabet = all_letters
        self.IMAGES = images
        self.WORDS = words

        # инициализация класса, от которогонаследован класс 2
        First.__init__(self, parent=self.parent, language=self.language,
                       all_letters=self.alphabet, images=self.IMAGES, words=self.WORDS)

    # метод для расставления кнопок на свои места
    def set_letters_level(self):
        self.all_buttons = []
        w_count = 1
        petal_count = 1
        horizontLayout = 1
        petal_y0 = 50
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(80)
        for y in range(4):
            y_step = 180 * y
            if y % 2 != 0:
                petal_x0 = 100
            else:
                petal_x0 = 0
            for x in range(3):
                x_step = 260 * x
                setattr(self, 'Petal' + str(petal_count), QtWidgets.QWidget(self.ButWidget))
                getattr(self, 'Petal' + str(petal_count)).setGeometry(
                    QtCore.QRect(petal_x0 + x_step, petal_y0 + y_step, 201, 141))
                setattr(self, 'gridPetal' + str(petal_count),
                        QtWidgets.QGridLayout(getattr(self, 'Petal' + str(petal_count))))
                getattr(self, 'gridPetal' + str(petal_count)).setSpacing(20)
                for h in range(3):
                    if h % 2 != 0:
                        margin = 25
                        space = 20
                        but_kolvo = 3
                    else:
                        margin = 50
                        space = 10
                        but_kolvo = 2
                    setattr(self, 'HorizontLayout' + str(horizontLayout), QtWidgets.QHBoxLayout())
                    getattr(self, 'HorizontLayout' + str(horizontLayout)).setContentsMargins(margin, -1, margin, -1)
                    getattr(self, 'HorizontLayout' + str(horizontLayout)).setSpacing(space)
                    for b in range(but_kolvo):
                        setattr(self, 'w' + str(w_count),
                                QtWidgets.QPushButton(getattr(self, 'Petal' + str(petal_count))))
                        getattr(self, 'w' + str(w_count)).setFont(font)
                        getattr(self, 'HorizontLayout' + str(horizontLayout)).addWidget(
                            getattr(self, 'w' + str(w_count)))
                        getattr(self, "w" + str(w_count)).setStyleSheet("background-color: rgb(255, 255, 255);")
                        getattr(self, "w" + str(w_count)).setObjectName('w' + str(w_count))
                        self.all_buttons.append(getattr(self, 'w' + str(w_count)))
                        w_count += 1

                    getattr(self, 'gridPetal' + str(petal_count)).addLayout(
                        getattr(self, 'HorizontLayout' + str(horizontLayout)), 2 - h, 0, 1, 1)
                    horizontLayout += 1
                petal_count += 1

    # загрузка цвета
    def set_color(self):
        self.parent.curr_col += 1
        if self.parent.curr_col > 2:
            self.parent.curr_col = 0
        self.setStyleSheet(BG[self.parent.curr_col])

        # синхронизация цвета
        if self.parent.curr_word == self.parent.startThirdLevel:
            self.parent.curr_col -= 1

    # метод при создании нового слова
    def set_new_word(self):
        # если слова закончились - выход в меню
        if self.parent.curr_word == self.all_words:
            self.parent.menu.show()
            self.hide()
        else:
            self.level_name.setText(f' Уровень {self.parent.cur_level}')

            # загрузка цвета
            self.set_color()
            self.hide_F_T()

            # выбор слова
            self.right_word = self.WORDS[self.parent.len_word-3][self.parent.curr_word]
            self.copy_word = self.right_word

            # удаление прошлых букв
            for i in self.need_word:
                i.setText('')

            # загрузка картинки
            self.new_image()

            # появление букв на выбор
            self.show_choose_letters()

