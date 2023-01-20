from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.Qt import *
from words import *
import random
from words import *

class Game():
    def __init__(self, parent=None):
        super().__init__()
        self.menu = parent

        self.curr_word = 0
        self.curr_col = -1
        self.cur_level = 1

        self.one = True
        self.two = False
        self.three = False

        self.len_word = 3


        self.set_level()

    def set_level(self):
        if self.cur_level == 1:
            self.first = First(self)
            self.first.show()
            self.menu.hide()
        else:
            self.third = Third(self)
            self.third.show()
            self.first.hide()


    def set_color(self):
        self.curr_col += 1
        if self.curr_col > 2:
            self.curr_col = 0
        return BG[self.curr_col]





class First(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('game.ui', self)
        self.parent = parent

        self.need_word = []

        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(60, 30, 320, 240))
        self.image.setText("")
        self.image.setObjectName("image")

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_end)

        self.load_True_image()
        self.load_False_image()
        self.hide_F_T()

        self.help.setText('Подсказка')

        self.set_letters_first_level()
        self.set_new_word()
        self.set_ans_squares()

        for but in self.all_buttons:
            but.clicked.connect(self.press)
        self.help.clicked.connect(self.show_help)

    def press(self):
        letter = self.sender().text()
        name = self.sender().objectName()
        index = self.copy_word.find(letter)
        show = False
        if letter in self.right_word and index == 0:
            getattr(self, name).setStyleSheet(BUT_BG[self.parent.curr_col])
            getattr(self, name).setEnabled(False)
            for i in range(len(self.right_word)):
                if self.need_word[i].text() == '' and not show:
                    self.show_True()
                    self.timer.start(2000)

                    self.need_word[i].setText(self.copy_word[0])
                    self.copy_word = self.copy_word[1:]

                    self.help.setText('Подсказка')
                    show = True
        else:
            self.show_False()
            self.timer.start(2000)

        self.checking_word_ending()

    def show_help(self):
        if self.help.text() == self.copy_word[0]:
            self.help.setText('Подсказка')
        else:
            self.help.setText(self.copy_word[0])

    def show_True(self):
        self.Right.show()
        self.Right_fr.show()
        self.False_fr.hide()
        self.False_.hide()

    def show_False(self):
        self.Right_fr.hide()
        self.Right.hide()
        self.False_fr.show()
        self.False_.show()

    def but_clear(self):
        for but in self.all_buttons:
            but.setText('')
            but.setEnabled(True)
            but.setStyleSheet(WHITE_BUT)

    def checking_word_ending(self):
        if len(self.copy_word) == 0:
            self.parent.curr_word += 1

            self.but_clear()
            self.set_new_word()

    def timer_end(self):
        self.Right.hide()
        self.Right_fr.hide()
        self.False_fr.hide()
        self.False_.hide()

    def set_new_word(self):
        if self.parent.curr_word == 1:
            self.parent.cur_level += 1
            self.parent.set_level()
        self.level_name.setText(f' Уровень {self.parent.cur_level}')

        self.setStyleSheet(self.parent.set_color())

        self.hide_F_T()

        self.right_word = WORDS[self.parent.len_word-3][self.parent.curr_word]
        self.copy_word = self.right_word

        for i in self.need_word:
            i.setText('')

        self.new_image()

        self.show_choose_letters()

    def set_ans_squares(self):
        x0 = 10
        font = QtGui.QFont()
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

    def show_choose_letters(self):
        letters_for_choose = self.make_letters_for_choosing()
        for i in range(len(letters_for_choose)):
            self.all_buttons[i].setText(letters_for_choose[i])

    def make_letters_for_choosing(self):
        list_right_word = [i for i in self.right_word]
        letters_for_choose = [i for i in self.right_word]
        btw = len(self.all_buttons) - len(letters_for_choose)

        i = 0
        while btw != 0:
            if all_letters[i] not in list_right_word:
                letters_for_choose.append(all_letters[i])
                btw -= 1
                i += 1
            else:
                i += 1
        random.shuffle(letters_for_choose)
        return letters_for_choose

    def new_image(self):
        pixmap = QPixmap(IMAGES[self.parent.len_word - 3][self.right_word])
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)

    def set_letters_first_level(self):
        self.all_buttons = []
        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(44)
        font.setBold(False)
        font.setWeight(50)

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

    def closeEvent(self, event):
        self.parent.menu.show()
        event.accept()

    def load_False_image(self):
        False_pixmap = QPixmap(FALSE_IMG)
        self.False_.setPixmap(False_pixmap)
        self.False_.setScaledContents(True)

    def load_True_image(self):
        Right_pixmap = QPixmap(RIGHT_IMG)
        self.Right.setPixmap(Right_pixmap)
        self.Right.setScaledContents(True)

    def hide_F_T(self):
        self.False_.hide()
        self.Right.hide()
        self.Right_fr.hide()
        self.False_fr.hide()


class Third(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('game.ui', self)
        self.parent = parent

        self.all_buttons = []
        self.need_word = []

        self.parent.three = True

        self.image = QtWidgets.QLabel(self.centralwidget)
        self.image.setGeometry(QtCore.QRect(60, 30, 320, 240))
        self.image.setText("")
        self.image.setObjectName("image")

        self.timer = QTimer()
        self.timer.timeout.connect(self.timer_end)

        self.load_True_image()
        self.load_False_image()
        self.hide_F_T()

        self.help.setText('Подсказка')

        self.set_letters_third_level()
        self.set_new_word()
        self.set_ans_squares()

        for but in self.all_buttons:
            but.clicked.connect(self.press)
        self.help.clicked.connect(self.show_help)

    def press(self):
        letter = self.sender().text()
        name = self.sender().objectName()
        index = self.copy_word.find(letter)
        show = False
        if letter in self.right_word and index == 0:
            print(self.parent.curr_col)
            getattr(self, name).setStyleSheet(BUT_BG[self.parent.curr_col])
            getattr(self, name).setEnabled(False)
            for i in range(len(self.right_word)):
                if self.need_word[i].text() == '' and not show:
                    self.show_True()
                    self.timer.start(2000)

                    self.need_word[i].setText(self.copy_word[0])
                    self.copy_word = self.copy_word[1:]

                    self.help.setText('Подсказка')
                    show = True
        else:
            self.show_False()
            self.timer.start(2000)

        self.checking_word_ending()

    def show_help(self):
        if self.help.text() == self.copy_word[0]:
            self.help.setText('Подсказка')
        else:
            self.help.setText(self.copy_word[0])

    def show_True(self):
        self.Right.show()
        self.Right_fr.show()
        self.False_fr.hide()
        self.False_.hide()

    def show_False(self):
        self.Right_fr.hide()
        self.Right.hide()
        self.False_fr.show()
        self.False_.show()

    def but_clear(self):
        for but in self.all_buttons:
            but.setText('')
            but.setEnabled(True)
            but.setStyleSheet(WHITE_BUT)

    def checking_word_ending(self):
        if len(self.copy_word) == 0:
            self.parent.curr_word += 1

            self.but_clear()
            self.set_new_word()

    def timer_end(self):
        self.Right.hide()
        self.Right_fr.hide()
        self.False_fr.hide()
        self.False_.hide()

    def set_new_word(self):
        if self.parent.curr_word == 1 and not self.parent.three:
            self.parent.cur_level += 1
            self.parent.set_level()

        self.level_name.setText(f' Уровень {self.parent.cur_level}')

        self.setStyleSheet(self.parent.set_color())
        print(self.parent.curr_col)
        self.hide_F_T()

        self.right_word = WORDS[self.parent.len_word-3][self.parent.curr_word]
        self.copy_word = self.right_word

        for i in self.need_word:
            i.setText('')

        self.new_image()

        self.show_choose_letters()

    def set_ans_squares(self):
        x0 = 10
        font = QtGui.QFont()
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

    def show_choose_letters(self):
        letters_for_choose = self.make_letters_for_choosing()
        for i in range(len(letters_for_choose)):
            self.all_buttons[i].setText(letters_for_choose[i])

    def make_letters_for_choosing(self):
        list_right_word = [i for i in self.right_word]
        letters_for_choose = [i for i in self.right_word]
        btw = len(self.all_buttons) - len(letters_for_choose)

        i = 0
        while btw != 0:
            if all_letters[i] not in list_right_word:
                letters_for_choose.append(all_letters[i])
                btw -= 1
                i += 1
            else:
                i += 1
        random.shuffle(letters_for_choose)
        return letters_for_choose

    def new_image(self):
        pixmap = QPixmap(IMAGES[self.parent.len_word - 3][self.right_word])
        self.image.setPixmap(pixmap)
        self.image.setScaledContents(True)

    def set_letters_third_level(self):
        self.all_buttons = []
        w_count = 1
        petal_count = 1
        horizontLayout = 1
        petal_y0 = 50

        font = QtGui.QFont()
        font.setFamily("MS Reference Sans Serif")
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(100)

        for y in range(4):
            y_step = 180 * y
            if y % 2 != 0:
                petal_x0 = 100
            else:
                petal_x0 = 0
            for x in range(3):

                x_step = 260 * x
                setattr(self, 'Petal' + str(petal_count), QtWidgets.QWidget(self.ButWidget))
                getattr(self, 'Petal' + str(petal_count)).setGeometry(QtCore.QRect(petal_x0 + x_step, petal_y0 + y_step, 201, 141))

                setattr(self, 'gridPetal' + str(petal_count),QtWidgets.QGridLayout(getattr(self, 'Petal' + str(petal_count))))
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
                        setattr(self, 'w' + str(w_count),QtWidgets.QPushButton(getattr(self, 'Petal' + str(petal_count))))
                        getattr(self, 'w' + str(w_count)).setFont(font)
                        getattr(self, 'HorizontLayout' + str(horizontLayout)).addWidget(getattr(self, 'w' + str(w_count)))
                        getattr(self, "w" + str(w_count)).setStyleSheet("background-color: rgb(255, 255, 255);")
                        getattr(self, "w" + str(w_count)).setObjectName('w' + str(w_count))
                        self.all_buttons.append(getattr(self, 'w' + str(w_count)))
                        w_count += 1

                    getattr(self, 'gridPetal' + str(petal_count)).addLayout(getattr(self, 'HorizontLayout' + str(horizontLayout)), 2 - h, 0, 1, 1)
                    horizontLayout += 1
                petal_count += 1

    def closeEvent(self, event):
        self.parent.menu.show()
        event.accept()

    def load_False_image(self):
        False_pixmap = QPixmap(FALSE_IMG)
        self.False_.setPixmap(False_pixmap)
        self.False_.setScaledContents(True)

    def load_True_image(self):
        Right_pixmap = QPixmap(RIGHT_IMG)
        self.Right.setPixmap(Right_pixmap)
        self.Right.setScaledContents(True)

    def hide_F_T(self):
        self.False_.hide()
        self.Right.hide()
        self.Right_fr.hide()
        self.False_fr.hide()

if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = First()

    win.show()
    sys.exit(app.exec_())

