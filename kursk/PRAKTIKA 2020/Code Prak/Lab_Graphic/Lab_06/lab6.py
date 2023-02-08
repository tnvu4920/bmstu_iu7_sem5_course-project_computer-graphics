from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPointF
import time

font_color = QColor(255, 255, 255)
boder_color = QColor(0, 0, 0)
fill_color = QColor(0, 0, 0)
point_zat = False
circle = False

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = myScene(0, 0, 675, 635)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(680, 650, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(font_color)
        self.lock.clicked.connect(lambda: lock(self))
        self.erase.clicked.connect(lambda: clean_all(self))
        self.paint.clicked.connect(lambda: fill_with_seed(self))
        self.addpoint.clicked.connect(lambda: add_point_by_btn(self))
        self.pixel.clicked.connect(lambda: set_flag_zat(self))
        self.timelabel.setText("0")
        self.edges = []
        self.point_now = None
        self.point_lock = None

        self.pen = QPen(fill_color)
        self.delay.setChecked(False)


class myScene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        if point_zat:
            get_pixel(event.scenePos())
        else:
            add_point(event.scenePos())


def set_flag_zat(win):
    global point_zat
    point_zat = True

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
        w.edges.append([w.point_now.x(), w.point_now.y(),
                        point.x(), point.y()])
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
    #print(w.edges)


def lock(win):
    win.edges.append([win.point_now.x(), win.point_now.y(), win.point_lock.x(), win.point_lock.y()])
    win.scene.addLine(win.point_now.x(), win.point_now.y(), win.point_lock.x(), win.point_lock.y(), w.pen)
    win.point_now = None
    #print(win.edges)


def clean_all(win):
    win.scene.clear()
    win.table.clear()
    win.edges = []
    win.point_now = None
    win.point_lock = None
    point_zat = False
    win.image.fill(font_color)
    win.timelabel.setText("0")
    r = win.table.rowCount()
    for i in range(r, -1, -1):
        win.table.removeRow(i)


def draw_edges(image, edges):
    p = QPainter()
    p.begin(image)
    #p.setPen(QPen(QColor(255, 255, 0)))
    p.setPen(QPen(boder_color))
    for ed in edges:
        p.drawLine(ed[0], ed[1], ed[2], ed[3])
    p.end()



def delay():
    QtWidgets.QApplication.processEvents(QEventLoop.AllEvents, 1)


def add_point_by_btn(win):
    x = win.x.value()
    y = win.y.value()
    p = QPoint()
    p.setX(x)
    p.setY(y)
    add_point(p)


def get_pixel(point):
    global w, point_zat, circle
    pix = QPixmap()
    if circle:
        r = w.rad.value()
        draw_circle(w.image, r, point)
        circle = False
    if point_zat:
        w.p_x.setValue(point.x())
        w.p_y.setValue(point.y())
        draw_edges(w.image, w.edges)
        point_zat = False
    pix.convertFromImage(w.image)
    w.scene.addPixmap(pix)


def get_start_point(win):
    return QPointF(win.p_x.value(), win.p_y.value())

def fill_with_seed(win):
    start = time.time()
    pixmap = QPixmap()
    painter = QPainter()
    painter.begin(win.image)

    
    boder = boder_color.rgb()    
    fill = fill_color.rgb()
    # инициализируем стек
    stack = []
    p = get_start_point(win)
    stack.append(p)

    # пока стек не пуст
    while stack:
        # извлечение пикселя (х,у) из стека
        pixel = stack.pop()
        x = pixel.x()
        y = pixel.y()
        
        # присваиваем ему новое значение
        win.image.setPixel(x, y, fill)
        
        # сохраняем x-координату затравочного пиксела
        xt = x
        
        # заполняем интервал слева от затравки
        x = x - 1
        while win.image.pixel(x, y) != boder:
            win.image.setPixel(x, y, fill)
            x = x - 1

        # сохраняем крайний слева пиксел
        xl = x + 1
        x = xt
        
        # заполняем интервал справа от затравки
        x = x + 1
        while win.image.pixel(x, y) != boder:
            win.image.setPixel(x, y, fill)
            x = x + 1
            
        # сохраняем крайний справа пиксел
        xr = x - 1

        # ищем затравку на строке выше
        y = y + 1
        x = xl
        f = 0
        
        while x <= xr:
            f = 0
            while win.image.pixel(x, y) != boder and  win.image.pixel(x, y) != fill and  x <= xr:
                if f == 0:
                    f = 1
                x = x + 1

            # помещаем в стек крайний справа пиксел
            if f == 1:
                if x == xr and win.image.pixel(x, y) != fill and win.image.pixel(x, y) != boder:
                    stack.append(QPointF(x, y))
                else:
                    stack.append(QPointF(x - 1, y))
                f = 0

            # продолжим проверку, если интервал был прерван
            xt = x
            while (win.image.pixel(x, y) == boder or win.image.pixel(x, y) == fill) and x < xr:
                x = x + 1
            # удостоверимся, что координата пиксела увеличена
            if x == xt:
                x = x + 1

        # ищем затравку на строке ниже
        y = y - 2
        x = xl
        while x <= xr:
            f = 0
            while win.image.pixel(x, y) != boder and win.image.pixel(x, y) != fill and x <= xr:
                if f == 0:
                    f = 1
                x = x + 1

            if f == 1:
                if x == xr and win.image.pixel(x, y) != fill and win.image.pixel(x, y) != boder:
                    stack.append(QPointF(x, y))
                else:
                    stack.append(QPointF(x - 1, y))
                f = 0

            xt = x
            while (win.image.pixel(x, y) == boder or win.image.pixel(x, y) == fill) and x < xr:
                x = x + 1

            if x == xt:
                x = x + 1
        # с задержкой
        if win.delay.isChecked():
            delay()
            pixmap.convertFromImage(win.image)
            win.scene.addPixmap(pixmap)
    # без задержки
    if not win.delay.isChecked():
        end = time.time()
        t = end - start
        win.timelabel.setText("{}".format(t))
        pixmap.convertFromImage(win.image)
        win.scene.addPixmap(pixmap)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
