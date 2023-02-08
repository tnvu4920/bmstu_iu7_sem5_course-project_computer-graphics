from subroutine import add_line
import numpy as np
from math import pi, sin, cos, fabs
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter, QTransform
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPointF, QPoint


M = 40
shx = 600 / 2 + 50
shy = 710 / 2 - 50

eps = 1e-6


def rotateX(x, y, z, teta):
    teta = teta * pi / 180
    buf = y
    y = cos(teta) * y - sin(teta) * z
    z = cos(teta) * z + sin(teta) * buf
    return x, y, z


def rotateY(x, y, z, teta):
    teta = teta * pi / 180
    buf = x
    x = cos(teta) * x - sin(teta) * z
    z = cos(teta) * z + sin(teta) * buf
    return x, y, z


def rotateZ(x, y, z, teta):
    teta = teta * pi / 180
    buf = x
    x = cos(teta) * x - sin(teta) * y
    y = cos(teta) * y + sin(teta) * buf
    return x, y, z


def tranform(x, y, z, tetax, tetay, tetaz):
    try:
        x, y, z = rotateX(x, y, z, tetax)
        x, y, z = rotateY(x, y, z, tetay)
        x, y, z = rotateZ(x, y, z, tetaz)
        x = x * M + shx
        y = y * M + shy
    except:
        print(x, y, z)
    #print("check out")
    return round(x), round(y), round(z)


def isVisable(p, top, bot):
    if p.y() > top[p.x()]:
        return 1
    if p.y() < bot[p.x()]:
        return 2 
    return 0

def intersection(pk_prev, pn_prev, y1, y2):
    pk_curr = QPointF(pk_prev.x(), y1)
    pn_curr = QPointF(pn_prev.x(), y2)
    if (pk_prev == pk_curr):
        return pk_prev
    if (pn_prev == pn_curr):
        return pn_curr
    dy_curr = pn_curr.y() - pk_curr.y()
    dy_prev = pn_prev.y() - pk_prev.y()
    dx = pn_curr.x() - pk_curr.x()
    if (dx == 0):
        return pn_prev
    m_prev = dy_prev * 1.0/ dx
    
    x = pk_prev.x() + (pk_curr.y() - pk_prev.y()) * 1.0 * dx / (-dy_curr + dy_prev)
    y = m_prev * (x - pk_prev.x()) + pk_prev.y()
    return QPoint(round(x)-1, round(y)-1)

def float_horizon(max_width, max_hight, x_min, x_max, x_step, z_min, z_max, z_step,
                  tx, ty, tz, func, image):

    # инициализация массивов горизонтов
    top = {x: 0 for x in range(1, int(max_width) + 1)}
    bottom = {x: max_hight  for x in range(1, int(max_width) + 1)}
    
    z = z_max
    # Поочередно для каждой из равноотстоящих друг от друга плоскостей z = const,
    # начиная с ближней от точки наблюдения
    while z >= z_min:
        # Обработать левое боковое ребро
        x = x_min
        y = func(x, z)
        x, y, z_buf = tranform(x, y, z, tx, ty, tz)

        # если точка является первой точкой на первой кривой
        if fabs(z - z_max)< eps:
            # запомнить ее в качестве P 
            P = QPoint(x, y)
        else:
            # соединит ее с P, и запомнит в качестве P
            top, bottom = add_line(P.x(), P.y(), x, y, top, bottom, image)
            P = QPoint(x,y)

        # для каждой точки текущей кривой:
        x = x_min
        while x <= x_max:
            
            y = func(x, z)
            x_curr, y_curr, z_curr = tranform(x, y, z, tx, ty, tz)
            p_curr = QPoint(x_curr, y_curr)

            # определить видимость точки
            isVis_curr= isVisable(p_curr, top, bottom)
            
            if fabs(x - x_min) > eps: # x <> x_min
                
                # Если видимость точки изменилась
                if (isVis_curr * isVis_prev == 0 and isVis_curr + isVis_prev):

                    # найти точку пересечения кривой с горизонтом
                    if (isVis_curr + isVis_prev == 1):
                        I = intersection(p_prev, p_curr, top[p_prev.x()], top[p_curr.x()])
                    else:
                        I = intersection(p_prev, p_curr, bottom[p_prev.x()], bottom[p_curr.x()])

                    # Если текущая точка не видима  
                    if (isVis_curr == 0):
                        # изобразить участок кривой от предыдущей точки до точки пересечения
                        # Заполнить массивы верхнего и нижнего горизонтов
                        top, bottom = add_line(p_prev.x(), p_prev.y(), I.x(), I.y(), top, bottom, image)
                    # Если текущая точка видима
                    else:
                        # изобразить участок кривой от точки пересечения  до текущей точки
                        # Заполнить массивы верхнего и нижнего горизонтов
                        top, bottom = add_line(I.x(), I.y(), p_curr.x(), p_curr.y(), top, bottom, image)
                elif isVis_curr * isVis_prev != 0:
                    # то изобразить его полностю
                    # Заполнить массивы верхнего и нижнего горизонтов
                    top, bottom = add_line(p_prev.x(), p_prev.y(), p_curr.x(), p_curr.y(), top, bottom, image)

            p_prev = p_curr
            isVis_prev = isVis_curr + 0
            x += x_step

            
        # Обработать правое боковое ребро

        # если точка является последней точкой на первой кривой
        if fabs(z - z_max) < eps:
            # запомнить в качестве Q
            Q = p_curr
        else:
            # соединит ее с Q и запомнит в качестве Q
            top, bottom = add_line(Q.x(), Q.y(), p_curr.x(), p_curr.y(), top, bottom, image)
            Q = p_curr
        z -= z_step

    return image


