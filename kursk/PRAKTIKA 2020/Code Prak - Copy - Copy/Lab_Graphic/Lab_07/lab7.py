from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter, QTransform
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPoint
import time

old_color = Qt.blue
new_color = Qt.red
font_color = Qt.white
now = None

eps = 1e-6

pos = ['left', 'right', 'bottom', 'top']

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = Scene(0, 0, 761, 741)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(761, 741, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(font_color)
        self.bars.clicked.connect(lambda : set_bars(self, 1))
        self.erase.clicked.connect(lambda: clean_all(self))
        self.paint.clicked.connect(lambda: clipping(self))
        self.rect.clicked.connect(lambda: set_rect(self))
        self.horizontal.clicked.connect(lambda: set_bars(self, 2))
        self.vertical.clicked.connect(lambda:set_bars(self, 3))
        self.lines = []
        self.clip = None
        self.point_now = None
        self.input_bars = False
        self.input_rect = False
        self.pen = QPen(old_color)


class Scene(QtWidgets.QGraphicsScene):

    def mousePressEvent(self, event):
        add_point(event.scenePos())

    def mouseMoveEvent(self, event):
        global now, w
        if w.input_rect:
            if now is None:
                now = event.scenePos()
            else:
                self.removeItem(self.itemAt(now, QTransform()))
                p = event.scenePos()
                self.addRect(now.x(), now.y(), abs(now.x() - p.x()), abs(now.y() - p.y()))



def set_bars(win, code):
    if win.input_bars:
        win.input_bars = 0
        win.rect.setDisabled(False)
        win.erase.setDisabled(False)
        win.paint.setDisabled(False)
        #win.horizontal.setDisabled(False)
        #win.vertical.setDisabled(False)
    else:
        win.input_bars = code
        win.rect.setDisabled(True)
        win.erase.setDisabled(True)
        win.paint.setDisabled(True)
        #win.horizontal.setDisabled(True)
        #win.vertical.setDisable(True)


def set_rect(win):
    if win.input_rect:
        win.input_rect = False
        win.bars.setDisabled(False)
        win.erase.setDisabled(False)
        win.paint.setDisabled(False)
        win.horizontal.setDisabled(False)
        win.vertical.setDisabled(False)
    else:
        win.input_rect = True
        win.bars.setDisabled(True)
        win.erase.setDisabled(True)
        win.paint.setDisabled(True)
        win.horizontal.setDisabled(True)
        win.vertical.setDisabled(True)


def add_row(win):
    win.table.insertRow(win.table.rowCount())


def add_point(p):
    global w
    print("chekc add point")
    if w.input_bars:
        if w.point_now is None:
            w.point_now = p
        else:
            point = p
            if (w.input_bars == 2): # horizontal
                print(p.x(), p.y(), w.input_bars)
                point.setY(w.point_now.y())
            if (w.input_bars == 3): # vertical
                point.setX(w.point_now.x())
            w.lines.append([[w.point_now.x(), w.point_now.y()],
                            [point.x(), point.y()]])

            add_row(w)
            i = w.table.rowCount() - 1
            item_b = QTableWidgetItem("[{0}, {1}]".format(w.point_now.x(), w.point_now.y()))
            item_e = QTableWidgetItem("[{0}, {1}]".format(point.x(), point.y()))
            w.table.setItem(i, 0, item_b)
            w.table.setItem(i, 1, item_e)
            w.scene.addLine(w.point_now.x(), w.point_now.y(), point.x(), point.y(), w.pen)
            w.point_now = None


def clean_all(win):
    win.scene.clear()
    win.table.clear()
    win.lines = []
    win.image.fill(Qt.white)
    r = win.table.rowCount()
    for i in range(r, -1, -1):
        win.table.removeRow(i)


def add_bars(win):
    global now
    if now is None:
        QMessageBox.warning(win, "Внимание!", "Не введен отсекатель!")
        return
    buf = win.scene.itemAt(now, QTransform())
    if buf is None:
        QMessageBox.warning(win, "Внимание!", "Не введен отсекатель!")
    else:
        buf = buf.rect()
        win.clip = [buf.left(), buf.right(), buf.top(),  buf.bottom()]

        t = abs(win.clip[2] - win.clip[3]) * 0.8
        k = abs(win.clip[0] - win.clip[1]) * 0.8
        # задаем граничные отрезки
        win.pen.setColor(old_color)
        w.lines.append([[win.clip[0], win.clip[2] + t],  [win.clip[0], win.clip[3] - t]])
        add_row(w)
        i = w.table.rowCount() - 1
        item_b = QTableWidgetItem("[{0}, {1}]".format(win.clip[0], win.clip[2] + t))
        item_e = QTableWidgetItem("[{0}, {1}]".format(win.clip[0], win.clip[3] - t))
        w.table.setItem(i, 0, item_b)
        w.table.setItem(i, 1, item_e)
        win.scene.addLine(win.clip[0], win.clip[2] + t,  win.clip[0], win.clip[3] - t, win.pen)

        w.lines.append([[win.clip[1], win.clip[2] + t],  [win.clip[1], win.clip[3] - t]])
        add_row(w)
        i = w.table.rowCount() - 1
        item_b = QTableWidgetItem("[{0}, {1}]".format(win.clip[1], win.clip[2] + t))
        item_e = QTableWidgetItem("[{0}, {1}]".format(win.clip[1], win.clip[3] - t))
        w.table.setItem(i, 0, item_b)
        w.table.setItem(i, 1, item_e)
        win.scene.addLine(win.clip[1], win.clip[3] - t,  win.clip[1], win.clip[2] + t, win.pen)

        w.lines.append([[win.clip[0] + k, win.clip[2]], [win.clip[1] - k, win.clip[2]]])
        add_row(w)
        i = w.table.rowCount() - 1
        item_b = QTableWidgetItem("[{0}, {1}]".format(win.clip[0] + k, win.clip[2]))
        item_e = QTableWidgetItem("[{0}, {1}]".format(win.clip[1] - k, win.clip[2]))
        w.table.setItem(i, 0, item_b)
        w.table.setItem(i, 1, item_e)
        win.scene.addLine(win.clip[0] + k, win.clip[2], win.clip[1] - k, win.clip[2], win.pen)

        w.lines.append([[win.clip[0] + k, win.clip[3]], [win.clip[1] - k, win.clip[3]]])
        add_row(w)
        i = w.table.rowCount() - 1
        item_b = QTableWidgetItem("[{0}, {1}]".format(win.clip[0] + k, win.clip[3]))
        item_e = QTableWidgetItem("[{0}, {1}]".format(win.clip[1] - k, win.clip[3]))
        w.table.setItem(i, 0, item_b)
        w.table.setItem(i, 1, item_e)
        win.scene.addLine(win.clip[0] + k, win.clip[3], win.clip[1] - k, win.clip[3], win.pen)


def get_code(a, rect):
    code = [0, 0, 0, 0]
    if a[0] < rect[0]:
        code[0] = 1
    if a[0] > rect[1]:
        code[1] = 1
    if a[1] < rect[2]:
        code[2] = 1
    if a[1] > rect[3]:
        code[3] = 1

    return code


'''
*****************************************

*****************************************
'''

def clipping(win):
    buf = win.scene.itemAt(now, QTransform()).rect()
    win.clip = {'left': buf.left(), 'right': buf.right(), 'top': buf.bottom(), 'bottom': buf.top()}
    for line in win.lines:
        res = line_clipping(win.clip, line)
        if res[0] == 1:# отрезок является целиком или частично видимым
            R = res[1]
            R1 = R[0]
            R2 = R[1]
            win.pen.setColor(new_color)
            win.scene.addLine(R1[0], R1[1], R2[0], R2[1], win.pen)
            win.pen.setColor(old_color)
        

def point_code(p, w):
    code = {'left':0, 'right': 0, 'bottom': 0, 'top': 0}
    if p[0] < w['left']:
        code['left'] = 1
    else:
        code['left'] = 0

    if p[0] > w['right']:
        code['right'] = 1
    else:
        code['right'] = 0

    if p[1] < w['bottom']:
        code['bottom'] = 1
    else:
        code['bottom'] = 0

    if p[1] > w['top']:
        code['top'] = 1
    else:
        code['top'] = 0

    return code

def sum_code(code):
    s = 0
    for i in pos:
        s += code[i]
    return s

def mult_code(code1, code2):
    s = 0
    for i in pos:
        s += code1[i] * code2[i]
    return s

def line_clipping(w, line):
    p1 = line[0]
    p2 = line[1]
    print(w, line)
    #Вычисление кодов концов отрезка T1, T2
    T1 = point_code(p1, w)
    T2 = point_code(p2, w)

    # Вычисление сумм кодов
    S1 = sum_code(T1)
    S2 = sum_code(T2)

    print(T1, T2)

    R = [p1, p2]
    #Установка признака видимости отрезка    
    pr = 1
    m = 1e30
    # Проверка полной видимости отрезка
    if (S1 == 0 and S2 == 0):
        R[0] = p1
        R[1] = p2
        return [pr, R]
    
    # Вычисление логического произведения кодов
    PL = mult_code(T1, T2)

    # отрезок невидим
    if (PL != 0):
        pr = -1
        return [pr,]

    # Проверка видимости первого конца отрезка
    if (S1 == 0):
        R[0] = p1
        i = 0

    elif (S2 == 0):
        R[0] = p2
        line[0], line[1] = line[1], line[0]
        i = 0
    else:
        i = -1


        
    while i < 1:
        i += 1
        Q = line[i]
        print(i)
        # отрезок вертикальный не может быть
        # пересечения с левой и правой границами отсекателя
        if (p1[0] != p2[0]):
            m = (p1[1] - p2[1]) * 1.0 / (p1[0] - p2[0])
            # Проверка возможности пересечения с левой границей отсекателя
            if (Q[0] <= w['left']):
                print("left")
                y = m * (w['left'] - Q[0]) + Q[1]
                if (y >= w['bottom'] and y <= w['top']):
                    R[i] = [w['left'], y]
                    continue
            print("check left")
            # Проверка возможности пересечения с правой границей отсекателя
            if (Q[0] >= w['right']):
                print("right")
                y = m * (w['right'] - Q[0]) + Q[1]
                if (y >= w['bottom'] and y <= w['top']):
                    R[i] = [w['right'], y]
                    continue
            print("check right")
        print("check left-right")
        
        # Проверка горизонтальности отрезка
        if (p1[1] != p2[1]):
            print("In Top-Bot")
            
            print('m = {}'.format(m))
            print(Q)
            # Проверка возможности пересечения с верхней границей отсекателя
            if (Q[1] >= w['top']):
                print("top")
                x = (w['top'] - Q[1]) / m + Q[0]
                if (x >= w['left'] and x <= w['right']):
                    R[i] = [x, w['top']]
                    print(R)
                    continue
            print("check top")
            #  Проверка возможности пересечения с нижней границей отсекателя
            if (Q[1] <= w['bottom']):
                print("bottom")
                x = (w['bottom'] - Q[1]) / m + Q[0]
                if (x >= w['left'] and x <= w['right']):
                    R[i] = [x, w['bottom']]
                    continue
            print("check bottom")
        print("check top-bottom")
            
        pr = -1
        return [pr, ]
    return [pr, R]
    
'''
*****************************************

*****************************************
'''   
    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
