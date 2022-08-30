from graphic import *
from vs_ai import *
from PyQt5.QtWidgets import *


class Stone(AStone):
    def __init__(self, parent, i, j, game):
        super(Stone, self).__init__(parent, i, j)
        self.game: Agent = game
        self.arr = self.game.game.board
        self.move(j*50, i*50)
        self.resize(50, 50)
        self.stones = None

    def init(self):
        self.setStyleSheet("background-image : url(empty.png);")

    def putEvent(self):
        res = self.game.put_human(self.i, self.j)
        self.set_color(self.arr[self.i, self.j])
        if res:
            return res

        res, r, c = self.game.put_ai()
        self.stones[c][r].set_color(self.arr[r][c])

        if res:
            return 2
        return res

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent) -> None:
        r = self.putEvent()
        print(r)
        if r == -1 or r == 0:
            return
        s = "LOSE" if r == 2 else "WIN"
        print(13)
        myWindow = WinLose(s)
        myWindow.exec_()
        self.parent().init()


class Gui(WindowClass):
    def __init__(self):
        self.game = Agent(19)
        self.game.load('fa')
        self.stones = []
        super(Gui, self).__init__()
        self.stones = [[Stone(self, y, x, self.game) for y in range(19)]for x in range(19)]
        for x in self.stones:
            for y in x:
                y.stones = self.stones

    def init(self):
        self.game.game.turn = 1
        for x in self.game.game.board:
            for y in range(19):
                x[y] = 0
        for x in self.stones:
            for y in x:
                y.init()
        super(Gui, self).init()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    gui = Gui()
    gui.show()
    app.exec_()