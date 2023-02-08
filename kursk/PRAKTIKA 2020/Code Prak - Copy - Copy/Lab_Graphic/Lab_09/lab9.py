from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter, QTransform, QPolygonF
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPointF, QPoint
import copy

red = Qt.red
blue = Qt.blue
black = Qt.black
now = None


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = Scene(0, 0, 561, 581)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.poly.clicked.connect(lambda : set_pol(self))
        self.erase.clicked.connect(lambda: clean_all(self))
        self.paint.clicked.connect(lambda: clipping(self))
        self.rect.clicked.connect(lambda: set_rect(self))
        self.ect.clicked.connect(lambda: add_bars(self))
        self.lock.clicked.connect(lambda: lock(self))
        self.pointInsert.clicked.connect(lambda: addpoint_btn(self))
        self.clip = []
        self.pol = []
        self.point_now_clip = None
        self.point_now_pol = None
        self.point_lock_pol = None
        self.point_lock_clip = None
        self.input_pol = False
        self.input_clip = False
        self.pen = QPen(black)


def addpoint_btn(win):
    x = win.xInput.value()
    y = win.yInput.value()
    
    p = QPointF()
    p.setX(x)
    
    p.setY(y)
    add_point(p)

class Scene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        add_point(event.scenePos())

    def mouseMoveEvent(self, event):
        global w
        x = event.scenePos().x()
        y = event.scenePos().y()
        w.x.setText("{0}".format(x))
        w.y.setText("{0}".format(y))


def sign(x):
    if not x:
        return 0
    else:
        return x / abs(x)


def set_pol(win):
    if win.input_pol:
        win.input_pol = False
        win.rect.setDisabled(False)
        win.erase.setDisabled(False)
        win.paint.setDisabled(False)
        win.ect.setDisabled(False)
    else:
        win.input_pol = True
        win.rect.setDisabled(True)
        win.erase.setDisabled(True)
        win.paint.setDisabled(True)
        win.ect.setDisabled(True)


def set_rect(win):
    if win.input_clip:
        win.input_clip = False
        win.poly.setDisabled(False)
        win.erase.setDisabled(False)
        win.paint.setDisabled(False)
        win.ect.setDisabled(False)
    else:
        win.input_clip = True
        win.poly.setDisabled(True)
        win.erase.setDisabled(True)
        win.paint.setDisabled(True)
        win.ect.setDisabled(True)


def add_point(point):
    global w
    if w.input_clip:
        w.pen.setColor(black)
        if w.point_now_clip is None:
            w.point_now_clip = point
            w.point_lock_clip = point
            add_row(w.table_rect)
            i = w.table_rect.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_rect.setItem(i, 0, item_x)
            w.table_rect.setItem(i, 1, item_y)
        else:
            w.clip.append(point)
            w.point_now_clip = point
            add_row(w.table_rect)
            i = w.table_rect.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_rect.setItem(i, 0, item_x)
            w.table_rect.setItem(i, 1, item_y)
            item_x = w.table_rect.item(i-1, 0)
            item_y = w.table_rect.item(i-1, 1)
            w.scene.addLine(point.x(), point.y(), float(item_x.text()), float(item_y.text()), w.pen)

    if w.input_pol:
        w.pen.setColor(blue)
        if w.point_now_pol is None:
            w.point_now_pol = point
            w.point_lock_pol = point
            add_row(w.table_pol)
            i = w.table_pol.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_pol.setItem(i, 0, item_x)
            w.table_pol.setItem(i, 1, item_y)
        else:
            w.pol.append(point)
            w.point_now_pol = point
            add_row(w.table_pol)
            i = w.table_pol.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_pol.setItem(i, 0, item_x)
            w.table_pol.setItem(i, 1, item_y)
            item_x = w.table_pol.item(i-1, 0)
            item_y = w.table_pol.item(i-1, 1)
            w.scene.addLine(point.x(), point.y(), float(item_x.text()), float(item_y.text()), w.pen)


def lock(win):
    if w.input_pol:
        win.pol.append(win.point_lock_pol)
        win.scene.addLine(win.point_now_pol.x(), win.point_now_pol.y(), win.point_lock_pol.x(), win.point_lock_pol.y(), w.pen)
        win.point_now_pol = None

    if w.input_clip:
        win.clip.append(win.point_lock_clip)
        win.scene.addLine(win.point_now_clip.x(), win.point_now_clip.y(), win.point_lock_clip.x(), win.point_lock_clip.y(), w.pen)
        win.point_now_clip = None


def add_row(win_table):
    win_table.insertRow(win_table.rowCount())


def clean_all(win):
    win.scene.clear()
    win.table_rect.clear()
    win.table_pol.clear()
    win.clip = []
    win.pol = []
    win.point_now_clip = None
    win.point_now_pol = None
    win.point_lock_clip = None
    win.point_lock_pol = None
    r = win.table_rect.rowCount()
    for i in range(r, -1, -1):
        win.table_rect.removeRow(i)

    r = win.table_pol.rowCount()
    for i in range(r, -1, -1):
        win.table_pol.removeRow(i)


def isConvex(edges):
    flag = 1

    # начальные вершины
    vo = edges[0]  # iая вершина
    vi = edges[1]  # i+1 вершина
    vn = edges[2]  # i+2 вершина и все остальные

    # векторное произведение двух векторов
    x1 = vi.x() - vo.x()
    y1 = vi.y() - vo.y()

    x2 = vn.x() - vi.x()
    y2 = vn.y() - vi.y()

    # определяем знак ординаты
    r = x1 * y2 - x2 * y1
    prev = sign(r)

    for i in range(2, len(edges) - 1):
        if not flag:
            break
        vo = edges[i - 1]
        vi = edges[i]
        vn = edges[i + 1]

        # векторное произведение двух векторов
        x1 = vi.x() - vo.x()
        y1 = vi.y() - vo.y()

        x2 = vn.x() - vi.x()
        y2 = vn.y() - vi.y()

        r = x1 * y2 - x2 * y1
        curr = sign(r)

        # если знак предыдущей координаты не совпадает, то возможно многоугольник невыпуклый
        if curr != prev:
            flag = 0
        prev = curr

    # не забываем проверить последнюю с первой вершины
    vo = edges[len(edges) - 1]
    vi = edges[0]
    vn = edges[1]

    # векторное произведение двух векторов
    x1 = vi.x() - vo.x()
    y1 = vi.y() - vo.y()

    x2 = vn.x() - vi.x()
    y2 = vn.y() - vi.y()

    r = x1 * y2 - x2 * y1
    curr = sign(r)
    if curr != prev:
        flag = 0

    return flag * curr


def Intersection(line1, line2, n):
    print("check in Inter")
    vis1 = isVisiable(line1[0], line2, n)
    vis2 = isVisiable(line1[1], line2, n)
    if (vis1 and not vis2) or (not vis1 and vis2):
        # ищем пересечение

        p1 = line1[0]
        p2 = line1[1]

        q1 = line2[0]
        q2 = line2[1]

        delta =   (p2.x() - p1.x()) * (q1.y() - q2.y()) - (q1.x() - q2.x()) * (p2.y() - p1.y())
        delta_t = (q1.x() - p1.x()) * (q1.y() - q2.y()) - (q1.x() - q2.x()) * (q1.y() - p1.y())
        if abs(delta) <= 1e-6:
            return p2

        t = delta_t / delta

        I = QPointF()
        I.setX(line1[0].x() + (line1[1].x() - line1[0].x()) * t)
        I.setY(line1[0].y() + (line1[1].y() - line1[0].y()) * t)
        return I
    else:
        return False


def isVisiable(point, line, n):
    P1 = line[0]
    P2 = line[1]
    v = vector_mult([point, P1], [P2, P1])
    if n * v <= 0:
        return True
    else:
        return False


def vector_mult(v1, v2):
    x1 = v1[0].x() - v1[1].x()
    y1 = v1[0].y() - v1[1].y()

    x2 = v2[0].x() - v2[1].x()
    y2 = v2[0].y() - v2[1].y()

    return x1 * y2 - x2 * y1



def clipping(win):

    n = isConvex(win.clip)
    if not n:
        QMessageBox.warning(win, "Error", "Error Polygon")
    else:
        p = SutherlandHodgmanClipping(win.clip, win.pol, n)
        if p:
            win.pen.setWidth(2)
            win.pen.setColor(red)
            win.scene.addPolygon(p, win.pen)
            win.pen.setWidth(1)


def SutherlandHodgmanClipping(C, P, n):
    
    # первая вершина отсекателя заносится в конец массива
    C.append(C[0])

    S = None
    F = None
    
    # Цикл по всем ребрам отсекателя 
    for i in range(len(C) - 1):
        # Обнуление количества вершин результирующего многоугольника 
        new = []
        print("i = ", i)
        
        # Цикл по всем ребрам отсекаемого многоугольника 
        for j in range(len(P)):
            print("j = ", j)
            # Анализ номера обрабатываемой вершины многоугольника
            if j == 0: # если первая вершина
                F = P[j]
            else:

                # Определение факта пересечения ребра многоугольника SPj и ребра отсекателя CiCi+1
                l1 = [S, P[j]]
                l2 = [C[i], C[i + 1]]
                t = Intersection(l1, l2, n)
                # Если пересечение ребер многоугольников установлено
                if t:
                    print("t = ", t);
                    # Занесение в массив координат результирующего многоугольника координат найденной точки
                    new.append(t)
                    
            # Изменение начальной точки ребра многоугольника
            S = P[j]
            # Если вершина S видима относительно ребра CiCi+1
            if isVisiable(S,  [C[i], C[i + 1]], n):
                # занесение ее координат в массив
                new.append(S)
                print("Append S", S)
            print(new)
        # Конец цикла по переменной j 
        #Проверка ненулевого количества вершин в результирующем массиве
        if len(new) == 0: # многоугольник невидим относительно текущей границы отсекателя
            return False # он невидим относительно всего отсекателя
        else:

            # Проверка факта пересечения ребра многоугольника SF с ребром отсекателя CjCj+1.
            t = Intersection([S, F], [C[i], C[i + 1]], n)

            # Если пересечение ребер многоугольников установлено
            if t:
                print("Dau Cuoi ", t)
                # Занесение в массив найденной точки 
                new.append(t)
        P = new
        print("Hết i ", new)
    # Конец цикла по переменной i
    
    return QPolygonF(P)
    # Конец алгоритма.


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
