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

def float_horizon(scene_width, scene_hight, x_min, x_max, x_step, z_min, z_max, z_step,
                  tx, ty, tz, func, image):

    # инициализация массивов горизонтов
    top = {x: 0 for x in range(1, int(scene_width) + 1)}
    bottom = {x: scene_hight  for x in range(1, int(scene_width) + 1)}
    
    z = z_max


    # duyet theo chiều từ gần ra xa
    while z >= z_min:
        #print("z = ", z)
        # mặt phẳng toạ độ Z
        x = x_min
        y = func(x, z)
        # phép quay theo X, Y, Z
        x, y, z_buf = tranform(x, y, z, tx, ty, tz)

        # Обрабатываем левое ребро(смотрим предыдущее с текущим)
        #если точка является первой точкой на первой кривой
        if fabs(z - z_max)< eps:
            P = QPoint(x, y)
        else:
            top, bottom = add_line(P.x(), P.y(), x, y, top, bottom, image)
            P = QPoint(x,y)

        # điểm bắt đầu trong mặt phẳng z = const
        x = x_min
        while x <= x_max:
            #print("\t x = ", x)
            # xác định điểm tiếp theo
            y = func(x, z)
            x_curr, y_curr, z_curr = tranform(x, y, z, tx, ty, tz)
            p_curr = QPoint(x_curr, y_curr)
            isVis_curr= isVisable(p_curr, top, bottom)
            
            if fabs(x - x_min) > eps:
                isVis_curr = isVisable(p_curr, top, bottom)
                if (isVis_curr * isVis_prev == 0 and isVis_curr + isVis_prev):
                    if (isVis_curr + isVis_prev == 1):
                        try:
                            if (p_prev.x() == p_curr.x()):
                                
                                I = QPoint(p_prev.x(), min(p_curr.y(), p_prev.y()))
                                top[I.x()] = I.y()
                                print("check", p_prev, p_curr, I, top[I.x()], isVis_curr ,isVis_prev)
                            else:
                                I = intersection(p_prev, p_curr, top[p_prev.x()], top[p_curr.x()])
                        except:
                            print("err")
                    else:
                        if (p_prev.x() == p_curr.x()):
                            I = QPoint(p_prev.x(), max(p_curr.y(), p_prev.y()))
                            bottom[I.x()] = I.y()
                        else:
                            y1 = bottom[p_prev.x()]
                            y2 = bottom[p_curr.x()]
                            I = intersection(p_prev, p_curr, y1, y2)
                        
                    if (isVis_curr == 0):
                        top, bottom = add_line(p_prev.x(), p_prev.y(), I.x(), I.y(), top, bottom, image)
                        if (p_prev.x() == p_curr.x()):
                            print('----',top[p_prev.x()], bottom[p_prev.x()])
                    else:
                        top, bottom = add_line(I.x(), I.y(), p_curr.x(), p_curr.y(), top, bottom, image)
                elif isVis_curr * isVis_prev != 0:
                    top, bottom = add_line(p_prev.x(), p_prev.y(), p_curr.x(), p_curr.y(), top, bottom, image)
            p_prev = p_curr
            isVis_prev = isVis_curr + 0
            x += x_step

        # Обрабатываем правое ребро(смотрим текущее со следующим)
        if fabs(z - z_max) < eps:
            Q = p_curr
        else:
            top, bottom = add_line(Q.x(), Q.y(), p_curr.x(), p_curr.y(), top, bottom, image)
            Q = p_curr
        z -= z_step

    return image


