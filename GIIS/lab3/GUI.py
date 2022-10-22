from cmath import sqrt
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
import enum


class LineMode(enum.Enum):
    simple_line = 0
    bresenham_line = 1
    bresenham_circle = 2

class Color(enum.Enum):
    red = 0
    green = 1
    black = 2
    

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.line_mode = LineMode
        self.color = Color
        self.click_counter = 0
        self.x0 = 0
        self.y0 = 0
        self.x1 = 0
        self.y1 = 0
        self.setFixedSize(QtCore.QSize(1200, 1000))
        self.layout = QtWidgets.QGridLayout()
        self.buttons_layout1 = QtWidgets.QVBoxLayout()
        self.buttons_layout2 = QtWidgets.QVBoxLayout()

        self.circle_button = QtWidgets.QPushButton('Bresenham circle')
        self.simple_line_button = QtWidgets.QPushButton('Simple line')
        self.bresenham_line_button = QtWidgets.QPushButton('Bresenham line')
        self.circle_button.setFixedWidth(250)
        self.simple_line_button.setFixedWidth(250)
        self.bresenham_line_button.setFixedWidth(250)

        self.green_button = QtWidgets.QPushButton('Green')
        self.red_button = QtWidgets.QPushButton('Red')
        self.black_button = QtWidgets.QPushButton('Black')
        self.green_button.setFixedWidth(250)
        self.red_button.setFixedWidth(250)
        self.black_button.setFixedWidth(250)

        self.label = QtWidgets.QLabel()
        self.label.setMouseTracking(True)
        self.label.setFixedSize(QtCore.QSize(1180, 600))
        canvas = QtGui.QPixmap(1165, 600)
        canvas.fill(QtGui.QColor("white"))
        self.label.setPixmap(canvas)

        self.simple_line_button.clicked.connect(self.simple_line_clicked)
        self.bresenham_line_button.clicked.connect(self.bresenham_line_clicked)
        self.circle_button.clicked.connect(self.bresenham_circle_clicked)
        self.black_button.clicked.connect(self.black_clicked)
        self.green_button.clicked.connect(self.green_clicked)
        self.red_button.clicked.connect(self.red_clicked)

        self.buttons_layout1.addWidget(self.circle_button)
        self.buttons_layout1.addWidget(self.simple_line_button)
        self.buttons_layout1.addWidget(self.bresenham_line_button)
        self.buttons_layout2.addWidget(self.black_button)
        self.buttons_layout2.addWidget(self.green_button)
        self.buttons_layout2.addWidget(self.red_button)

        self.layout.addWidget(self.label, 0, 0)
        self.layout.addLayout(self.buttons_layout1, 1, 2)
        self.layout.addLayout(self.buttons_layout2, 1, 3)

        self.widget = QtWidgets.QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        self.setWindowTitle("tinypaint")

    def green_clicked(self):
        self.color = Color.green

    def red_clicked(self):
        self.color = Color.red

    def black_clicked(self):
        self.color = Color.black
        
    def bresenham_line_clicked(self):
        self.line_mode = LineMode.bresenham_line

    def bresenham_circle_clicked(self):
        self.line_mode = LineMode.bresenham_circle

    def simple_line_clicked(self):
        self.line_mode = LineMode.simple_line

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(5)
        painter.setPen(pen)
        pos = self.label.mapFromParent(a0.pos())
        if self.click_counter == 1:  
            self.x1 = pos.x()
            self.y1 = pos.y()
            painter.drawPoint(self.x1, self.y1)
            painter.end()
            self.update()
            self.click_counter = 0

            if self.line_mode == LineMode.bresenham_circle:
                self.bresenham_circle()
            elif self.line_mode == LineMode.bresenham_line:
                self.bresenham_line()
            elif self.line_mode == LineMode.simple_line:
                self.simple_line()
            

        elif self.click_counter == 0:
            self.x0 = pos.x() 
            self.y0 = pos.y() 
            painter.drawPoint(self.x0, self.y0)
            painter.end()
            self.update()
            self.click_counter += 1    
        

    def simple_line(self):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(1)
        if self.color == Color.green:
            pen.setColor(QtGui.QColor("green"))
        elif self.color == Color.red:
            pen.setColor(QtGui.QColor("red"))
        painter.setPen(pen)

        k = (self.y1 - self.y0) / (self.x1 - self.x0)
        y = self.y0
        for x in range(self.x0, self.x1):
            painter.drawPoint(x, int(y))
            y += k

        painter.end()
        self.update()

    def plot_line_low(self, x0, y0, x1, y1):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(1)
        if self.color == Color.green:
            pen.setColor(QtGui.QColor("green"))
        elif self.color == Color.red:
            pen.setColor(QtGui.QColor("red"))
        painter.setPen(pen)

        dx = x1 - x0
        dy = y1 - y0
        yi = 1
        if dy < 0:
            yi = -1
            dy = -dy

        D = (2* dy) - dx
        y = y0

        for x in range(x0, x1):
            painter.drawPoint(x, y)
            if D > 0:
                y = y + yi
                D = D + (2 * (dy - dx))
            else:
                D = D + 2 * dy
        painter.end()
        self.update()


    def plot_line_high(self, x0, y0, x1, y1):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(1)
        if self.color == Color.green:
            pen.setColor(QtGui.QColor("green"))
        elif self.color == Color.red:
            pen.setColor(QtGui.QColor("red"))
        painter.setPen(pen)

        dx = x1 - x0
        dy = y1 - y0
        xi = 1
        if dx < 0:
            xi = -1
            dx = -dx

        D = (2 * dx) - dy
        x = x0

        for y in range(y0, y1):
            painter.drawPoint(x, y)
            if D > 0:
                x = x + xi
                D = D + (2 * (dx - dy))
            else:
                D = D + 2 * dx
        painter.end()
        self.update()


    def bresenham_line(self):
        x0 = self.x0
        x1 = self.x1
        y0 = self.y0
        y1 = self.y1
        if abs(y1 - y0) < abs(x1 - x0):
            if x0 > x1:
                self.plot_line_low(x1, y1, x0, y0)
            else:
                self.plot_line_low(x0, y0, x1, y1)
        else:
            if y0 > y1:
                self.plot_line_high(x1, y1, x0, y0)
            else:
                self.plot_line_high(x0, y0, x1, y1)
            

    def sign(self, x):
        sign = 0
        if x > 0:
            sign = 1
        elif x < 0:
            sign = -1
        return sign


    def draw_circle(self, x0, y0, x, y):
        painter = QtGui.QPainter(self.label.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(1)
        if self.color == Color.green:
            pen.setColor(QtGui.QColor("green"))
        elif self.color == Color.red:
            pen.setColor(QtGui.QColor("red"))
        painter.setPen(pen)

        painter.drawPoint(int(x0 + x), int(y0 + y))
        painter.drawPoint(int(x0 + x), int(y0 - y))
        painter.drawPoint(int(x0 - x), int(y0 + y))
        painter.drawPoint(int(x0 - x), int(y0 - y))
        painter.drawPoint(int(x0 + y), int(y0 + x))
        painter.drawPoint(int(x0 + y), int(y0 - x))
        painter.drawPoint(int(x0 - y), int(y0 + x))
        painter.drawPoint(int(x0 - y), int(y0 - x))

        painter.end()
        self.update()



    def bresenham_circle(self):
        x0 = self.x0
        x1 = self.x1
        y0 = self.y0
        y1 = self.y1
        r = abs(sqrt(abs((x0 - x1)**2) + abs((y0 - y1)**2)))

        x = 0
        y = r
        delta = 3 - 2 * r
        self.draw_circle(x0, y0, x, y)
        while(y >= x):
            x += 1
            
            if delta > 0:
                y -= 1
                delta = delta + 4 * (x - y) + 10
            else:
                delta = delta + 4 * x + 6
            
            self.draw_circle(x0, y0, x, y)
            


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()