import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5 import uic


form_class = uic.loadUiType("winlose.ui")[0]


class WinLose(QDialog, form_class):
    def __init__(self, s):
        super().__init__()
        self.setupUi(self)
        self.label.setText(s)
        self.show()


class AStone(QLabel):
    def __init__(self, parent, i, j):
        super(AStone, self).__init__(parent)
        self.i, self.j = i, j

    def init(self):
        self.setStyleSheet("background-image : url(init.png);")

    def set_color(self, v):
        if v == 1:
            self.setStyleSheet("background-image : url(black.png);")
        elif v == 2:
            self.setStyleSheet("background-image : url(white.png);")


class WindowClass(QWidget):
    def __init__(self):
        super().__init__()
        self.btn = [[QLabel(self) for y in range(19)] for x in range(19)]
        for x in range(19):
            for y in range(19):
                p = self.btn[x][y]
                p.resize(50, 50)
                p.move(50 * x, 50 * y)
        self.init()

    def init(self):
        for x in range(1, 18):
            btn1 = self.btn[x][0]
            btn2 = self.btn[x][18]
            btn3 = self.btn[0][x]
            btn4 = self.btn[18][x]
            btn1.setStyleSheet("background-image : url(side2.png);")
            btn2.setStyleSheet("background-image : url(side4.png);")
            btn3.setStyleSheet("background-image : url(side1.png);")
            btn4.setStyleSheet("background-image : url(side3.png);")
        self.btn[0][0].setStyleSheet("background-image : url(corner2.png);")
        self.btn[18][0].setStyleSheet("background-image : url(corner3.png);")
        self.btn[0][18].setStyleSheet("background-image : url(corner1.png);")
        self.btn[18][18].setStyleSheet("background-image : url(corner4.png);")
        for x in range(1, 18):
            for y in range(1, 18):
                self.btn[x][y].setStyleSheet("background-image : url(img1.png);")
        self.btn[3][3].setStyleSheet("background-image : url(img2.png);")
        self.btn[3][15].setStyleSheet("background-image : url(img2.png);")
        self.btn[15][3].setStyleSheet("background-image : url(img2.png);")
        self.btn[15][15].setStyleSheet("background-image : url(img2.png);")
        self.btn[9][9].setStyleSheet("background-image : url(img2.png);")
        self.btn[3][9].setStyleSheet("background-image : url(img2.png);")
        self.btn[9][3].setStyleSheet("background-image : url(img2.png);")
        self.btn[15][9].setStyleSheet("background-image : url(img2.png);")
        self.btn[9][15].setStyleSheet("background-image : url(img2.png);")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()