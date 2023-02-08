from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter, QTransform
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPointF


red = Qt.red
blue = Qt.blue
black = Qt.black
now = None


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = Scene(0, 0, 651, 680)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(651, 680, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)
        self.bars.clicked.connect(lambda : set_bars(self, 1))
        self.erase.clicked.connect(lambda: clean_all(self))
        self.paint.clicked.connect(lambda: clipping(self))
        self.rect.clicked.connect(lambda: set_rect(self))
        #self.ect.clicked.connect(lambda: add_bars(self))
        self.lock.clicked.connect(lambda: lock(self))
        self.horizontal.clicked.connect(lambda: set_bars(self, 2))
        self.vertical.clicked.connect(lambda:set_bars(self, 3))
        self.lines = []
        self.edges = []
        self.clip = None
        self.point_now_rect = None
        self.point_now_bars = None
        self.point_lock = None
        self.input_bars = False
        self.input_rect = False
        self.pen = QPen(black)


class Scene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        add_point(event.scenePos())


def sign(x):
    if not x:
        return 0
    else:
        return x / abs(x)


def set_bars(win, code):
    if win.input_bars:
        win.input_bars = 0
        win.rect.setDisabled(False)
        win.erase.setDisabled(False)
        win.paint.setDisabled(False)
        #win.ect.setDisabled(False)
        win.lock.setDisabled(False)
    else:
        win.input_bars = code
        win.rect.setDisabled(True)
        win.erase.setDisabled(True)
        win.paint.setDisabled(True)
        #win.ect.setDisabled(True)
        win.lock.setDisabled(True)


def set_rect(win):
    if win.input_rect:
        win.input_rect = False
        win.bars.setDisabled(False)
        win.erase.setDisabled(False)
        win.paint.setDisabled(False)
        #win.ect.setDisabled(False)
        win.lock.setDisabled(False)
    else:
        win.input_rect = True
        win.bars.setDisabled(True)
        win.erase.setDisabled(True)
        win.paint.setDisabled(True)
        #win.ect.setDisabled(True)


def lock(win):
    win.edges.append(win.point_lock)
    win.scene.addLine(win.point_now_rect.x(), win.point_now_rect.y(), win.point_lock.x(), win.point_lock.y(), w.pen)
    win.point_now_rect = None


def add_bars(win):
    if len(win.edges) == 0:
        QMessageBox.warning(win, "Внимание!", "Не введен отсекатель!")
        return
    win.pen.setColor(red)
    w.lines.append([[win.edges[0].x() - 15, win.edges[0].y() - 15],
                    [win.edges[1].x() - 15, win.edges[1].y() - 15]])
    add_row(w.table_bars)
    i = w.table_bars.rowCount() - 1
    item_b = QTableWidgetItem("[{0}, {1}]".format(win.edges[0].x() - 15 , win.edges[0].y() - 15))
    item_e = QTableWidgetItem("[{0}, {1}]".format(win.edges[1].x() - 15, win.edges[1].y() - 15))
    w.table_bars.setItem(i, 0, item_b)
    w.table_bars.setItem(i, 1, item_e)
    w.scene.addLine(win.edges[0].x() - 15, win.edges[0].y() - 15, win.edges[1].x() - 15, win.edges[1].y() - 15, w.pen)

    win.pen.setColor(red)
    w.lines.append([[win.edges[0].x() + 15, win.edges[0].y() + 15],
                    [win.edges[1].x() + 15, win.edges[1].y() + 15]])
    add_row(w.table_bars)
    i = w.table_bars.rowCount() - 1
    item_b = QTableWidgetItem("[{0}, {1}]".format(win.edges[0].x() + 15, win.edges[0].y() + 15))
    item_e = QTableWidgetItem("[{0}, {1}]".format(win.edges[1].x() + 15, win.edges[1].y() + 15))
    w.table_bars.setItem(i, 0, item_b)
    w.table_bars.setItem(i, 1, item_e)
    w.scene.addLine(win.edges[0].x() + 15, win.edges[0].y() + 15, win.edges[1].x() + 15, win.edges[1].y() + 15, w.pen)


def clean_all(win):
    win.scene.clear()
    win.table_rect.clear()
    win.table_bars.clear()
    win.lines = []
    win.edges = []
    win.point_now_rect = None
    win.point_now_bars = None
    win.point_lock = None
    win.image.fill(Qt.white)
    r = win.table_rect.rowCount()
    for i in range(r, -1, -1):
        win.table_rect.removeRow(i)

    r = win.table_bars.rowCount()
    for i in range(r, -1, -1):
        win.table_bars.removeRow(i)


def add_row(win_table):
    win_table.insertRow(win_table.rowCount())


def add_point(point):
    global w
    if w.input_rect:
        w.pen.setColor(black)
        if w.point_now_rect is None:
            w.point_now_rect = point
            w.point_lock = point
            add_row(w.table_rect)
            i = w.table_rect.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_rect.setItem(i, 0, item_x)
            w.table_rect.setItem(i, 1, item_y)
        else:
            w.edges.append(point)
            w.point_now_rect = point
            add_row(w.table_rect)
            i = w.table_rect.rowCount() - 1
            item_x = QTableWidgetItem("{0}".format(point.x()))
            item_y = QTableWidgetItem("{0}".format(point.y()))
            w.table_rect.setItem(i, 0, item_x)
            w.table_rect.setItem(i, 1, item_y)
            item_x = w.table_rect.item(i-1, 0)
            item_y = w.table_rect.item(i-1, 1)
            w.scene.addLine(point.x(), point.y(), float(item_x.text()), float(item_y.text()), w.pen)
    if w.input_bars:
        w.pen.setColor(red)
        if w.point_now_bars is None:
            w.point_now_bars = point
        else:
            point1 = point
            if (w.input_bars == 2): # horizontal
                point1.setY(w.point_now_bars.y())
            if (w.input_bars == 3): # vertical
                point1.setX(w.point_now_bars.x())

            w.lines.append([[w.point_now_bars.x(), w.point_now_bars.y()],
                            [point1.x(), point1.y()]])

            add_row(w.table_bars)
            i = w.table_bars.rowCount() - 1
            item_b = QTableWidgetItem("[{0}, {1}]".format(w.point_now_bars.x(), w.point_now_bars.y()))
            item_e = QTableWidgetItem("[{0}, {1}]".format(point1.x(), point1.y()))
            w.table_bars.setItem(i, 0, item_b)
            w.table_bars.setItem(i, 1, item_e)
            w.scene.addLine(w.point_now_bars.x(), w.point_now_bars.y(), point1.x(), point1.y(), w.pen)
            w.point_now_bars = None


def clipping(win):
    fl = isPolygonConvex(win.edges)
    for i in win.edges:
        print(i)
    if fl == 0:
        QMessageBox.warning(win, "Error", "Input Polygon is not convex")
        return
    for b in win.lines:
        win.pen.setColor(blue)
        cyrus_beck_lineClipping(b, win.edges, fl, win.scene, win.pen)
    win.pen.setColor(red)


def isPolygonConvex(edges):
    fl = 1
    
    # начальные вершины
    v0 = edges[0]  # iая вершина
    v1 = edges[1]  # i+1 вершина
    v2 = edges[2]  # i+2 вершина

    # векторное произведение двух векторов
    x1, y1 = v1.x() - v0.x(), v1.y() - v0.y()
    x2, y2 = v2.x() - v1.x(), v2.y() - v1.y()
    r = x1 * y2 - x2 * y1
    
    # определяем знак ординаты
    prev = sign(r)

    for i in range(2, len(edges) - 1):
        if fl == 0:
            break
        v0 = edges[i - 1]
        v1 = edges[i]
        v2 = edges[i + 1]

        # векторное произведение двух векторов
        x1, y1 = v1.x() - v0.x(), v1.y() - v0.y()
        x2, y2 = v2.x() - v1.x(), v2.y() - v1.y()
        r = x1 * y2 - x2 * y1
        curr = sign(r)

        if curr != prev:
            fl = 0
        prev = curr

    # проверить последнюю с первой вершины
    v0 = edges[len(edges) - 1]
    v1 = edges[0]
    v2 = edges[1]

    # векторное произведение двух векторов
    x1, y1 = v1.x() - v0.x(), v1.y() - v0.y()
    x2, y2 = v2.x() - v1.x(), v2.y() - v1.y()
    r = x1 * y2 - x2 * y1
    curr = sign(r)

    if curr != prev:
        fl = 0

    return fl * curr


def scalar_mult(v1, v2):
    return v1.x() * v2.x() + v1.y() * v2.y()


def P_t(line, t):
    print(line, t)
    p = QPointF()
    P1 = QPointF(line[0][0], line[0][1])
    P2 = QPointF(line[1][0], line[1][1])
    print(P1.x(), P1.y())
    print(P2.x(), P2.y())
    print("chekc 9")
    p.setX(P1.x() + (P2.x() - P1.x()) * t)
    p.setY(P1.y() + (P2.y() - P1.y()) * t)
    print(p.x(), p.y())

    
    return p


def cyrus_beck_lineClipping(line, edges, n, scene, pen):
    # Инициализация пределов значений параметра t 
    tb = 0
    te = 1
    #Вычисление вектора ориентации отрезка D = P2 - P1.
    D = QPointF()
    D.setX(line[1][0] - line[0][0])
    D.setY(line[1][1] - line[0][1])
    # цикл по всем сторонам отсекающего окна 
    for i in range(len(edges)):
        print(i)
        # Вычисление вектора внутренней нормали к очередной i-ой стороне 
        N = QPointF()
        if i == len(edges) - 1:
            N.setX(-n * (edges[0].y() - edges[i].y()))
            N.setY(n * (edges[0].x() - edges[i].x()))
            print(edges[0], edges[i]);
        else:
            N.setX(-n * (edges[i + 1].y() - edges[i].y()))
            N.setY(n * (edges[i + 1].x() - edges[i].x()))
            print(edges[i], edges[i + 1])

        # Определение граничной точки fi 
        F = QPointF(edges[i].x(), edges[i].y())
        
        # Вычисление вектора Wi = P1 - fi 
        W = QPointF()
        W.setX(line[0][0] - F.x())
        W.setY(line[0][1] - F.y())
        # Вычисление скалярного произведения векторов Wскi= Wi nвi   
        Dsc = scalar_mult(D, N)

        # Вычисление скалярного произведения векторов Dск i= Dnвi . 
        Wsc = scalar_mult(W, N)

        print("Dsc = ",Dsc)
        # Проверка на равенство нулю скалярного произведения Dск

        if Dsc == 0:
            # отрезок (точка) невидим 
            if Wsc < 0:
                print("return Wsc < 0 canh {}".format(i));
                return
        else:
            #Вычисление параметра t
            t = - Wsc / Dsc

            # Поиск нижней границы параметра t            
            if Dsc > 0:
                # отрезок невидим
                if t > 1:
                    print("return Dsc > 0 t > 1 canh {}".format(i));
                    return
                else:
                    tb = max(tb, t)

            # Поиск верхней границы параметра t
            elif Dsc < 0:
                # отрезок невидим
                if t < 0:
                    print("return Dsc < 0 t < 0 canhj {} ".format(i))
                    return
                else:
                    te = min(te, t)
        # Конец цикла по сторонам отсекателя

    # проверка фактической видимости отрезка
    if tb <= te:
        R1 = P_t(line, te)
        R2 = P_t(line, tb)
        scene.addLine(R1.x(), R1.y(), R2.x(), R2.y(), pen)
    else:
        print("return tb < te")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
