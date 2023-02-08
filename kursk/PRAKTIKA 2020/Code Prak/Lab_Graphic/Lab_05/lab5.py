from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint
import time

fill_color = Qt.black
font_color = Qt.white


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = myScene(0, 0, 670, 570)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(680, 580, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(font_color)
        self.lock.clicked.connect(lambda: lock(self))
        self.erase.clicked.connect(lambda: clean_all(self))
        self.paint.clicked.connect(lambda: filling_by_edges(self))
        self.addpoint.clicked.connect(lambda: add_point_by_btn(self))
        self.edges = []
        self.point_now = None
        self.point_lock = None
        self.pen = QPen(fill_color)
        self.isDelay.setChecked(False)


class myScene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        add_point(event.scenePos())




def add_row(win):
    win.table.insertRow(win.table.rowCount())


def add_point(point):
    global w
    if w.point_now is None:
        w.point_now = point
        w.point_lock = point
        add_row(w)
        i = w.table.rowCount() - 1
        item_x = QTableWidgetItem("{0}".format(point.x()))
        item_y = QTableWidgetItem("{0}".format(point.y()))
        w.table.setItem(i, 0, item_x)
        w.table.setItem(i, 1, item_y)
    else:
        w.edges.append([[w.point_now.x(), w.point_now.y()],
                        [point.x(), point.y()]])
        w.point_now = point
        add_row(w)
        i = w.table.rowCount() - 1
        item_x = QTableWidgetItem("{0}".format(point.x()))
        item_y = QTableWidgetItem("{0}".format(point.y()))
        w.table.setItem(i, 0, item_x)
        w.table.setItem(i, 1, item_y)
        item_x = w.table.item(i-1, 0)
        item_y = w.table.item(i-1, 1)
        w.scene.addLine(point.x(), point.y(), float(item_x.text()), float(item_y.text()), w.pen)

        
def add_point_by_btn(win):
    x = win.x.value()
    y = win.y.value()
    p = QPoint()
    p.setX(x)
    p.setY(y)
    add_point(p)

def lock(win):
    win.edges.append([[win.point_now.x(), win.point_now.y()], [win.point_lock.x(), win.point_lock.y()]])
    win.scene.addLine(win.point_now.x(), win.point_now.y(), win.point_lock.x(), win.point_lock.y(), w.pen)
    win.point_now = None


def clean_all(win):
    #win.scene.clear()
    win.table.clear()
    win.edges = []
    win.point_now = None
    win.point_lock = None
    win.image.fill(font_color)
    win.timelabel.setText("0")
    r = win.table.rowCount()
    for i in range(r, -1, -1):
        win.table.removeRow(i)


def draw_edges(image, edges):
    global w
    pix = QPixmap() 
    p = QPainter()
    p.begin(image)
    p.setPen(QPen(fill_color))
    for ed in edges:
        p.drawLine(edge[0][0], edge[0][1], edge[1][0], edge[1][1])
    p.end()
    pix.convertFromImage(image)
    w.scene.addPixmap(pix)


def delay():
    QtWidgets.QApplication.processEvents(QEventLoop.AllEvents, 100)
    
    return

def max_x(edges):
    x_max = None
    for i in range(len(edges)):
        if x_max is None or edges[i][0][0] > x_max:
            x_max = edges[i][0][0]

        if x_max is None or edges[i][1][0] > x_max:
            x_max = edges[i][1][0]

    return x_max


def get_pixel_color():
    return

def filling_by_edges(win):
    start = time.time()
    pix = QPixmap() 
    painter = QPainter()
    #Найти самую правую точку области
    x_max = int(max_x(win.edges))
    
    for edge in win.edges:  # edge = [ [xA, yA], [xB, yB] ]
        painter.begin(win.image)
        
        # если горизонтальное ребро - пропустить это ребро
        if edge[0][1] == edge[1][1]:
            continue

        #Если точка B выше, чем A, поменять местами
        if edge[0][1] > edge[1][1]:
            edge[0][1], edge[1][1] = edge[1][1], edge[0][1]
            edge[0][0], edge[1][0] = edge[1][0], edge[0][0]
            
        dx = (edge[1][0] - edge[0][0])
        dy = (edge[1][1] - edge[0][1])

        #смещение по х (при dy = 1)
        m = dx * 1.0 / dy 

        y = edge[0][1]
        y_end = edge[1][1]
        x_st = edge[0][0] + m * 1 / 2.0 # T.(x_st, y +  1/2) - пересечение
        while y < y_end:
            x = int(x_st)
            if (x + 0.5 <= x_st):  
                x += 1
            # (x, y) - Самая левая точка находится справа от ребра

            #активизировать, подсветить все пиксели,у которых
            #центры лежат справа от Пересечения
            while x <= x_max:
                pixel_color = QColor(win.image.pixel(x, y))
                if pixel_color == font_color:
                    painter.setPen(QPen(fill_color))
                else:
                    painter.setPen(QPen(font_color))
                painter.drawPoint(x, y)
                x += 1
                
            # перейти к следующей строке
            x_st += m
            y += 1
            
            # с задержкой 
            if win.isDelay.isChecked():
                #delay()
                pix.convertFromImage(win.image)
                win.scene.addPixmap(pix)
            
        painter.end()
        
    # без задержки
    if not win.isDelay.isChecked():
        end = time.time()
        t = end - start
        print("Time: ", t)
        win.timelabel.setText("{}".format(t))
        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)
        

import sys
app = QtWidgets.QApplication(sys.argv)
w = Window()
w.show()
sys.exit(app.exec_())
