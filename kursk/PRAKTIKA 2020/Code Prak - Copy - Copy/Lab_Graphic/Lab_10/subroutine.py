from PyQt5.QtCore import Qt

from math import fabs


def sign(x):
    if not x:
        return 0
    else:
        return x / abs(x)


def add_line(x1, y1, x2, y2, top, bottom, image):
    # на самом деле это брезенхем
    check = 0
    if (x1 == x2):
        check = 1
        print(x1, y1, y2, top[x1], bottom[x1])
    x = x1
    y = y1
    dx = x2 - x1
    dy = y2 - y1
    sx = sign(dx)
    sy = sign(dy)
    dx = abs(dx)
    dy = abs(dy)

    try:

        # если точка
        if dx == 0 and dy == 0 and 0 <= x < image.width():
            if y >= top[x]:
                top[x] = y
                image.setPixel(x, image.height() - y, Qt.red)

            if y <= bottom[x]:
                bottom[x] = y
                image.setPixel(x, image.height() - y, Qt.red)

            return top, bottom

        #  Нужно ли менять местами х и у
        change = 0
        if dy > dx:
            dx, dy = dy, dx
            change = 1

        y_max_curr = top[x]
        y_min_curr = bottom[x]
        e = 2 * dy - dx

        while (x != x2 or y != y2):
            if 0 <= x < image.width():
                if y >= top[x]:
                    if y >= y_max_curr:
                        y_max_curr = y
                    image.setPixel(x, image.height() - y, Qt.red)

                if y <= bottom[x]:
                    if y <= y_min_curr:
                        y_min_curr = y
                    image.setPixel(x, image.height() - y, Qt.red)
    
            if e > 0:
                if change:
                    if (check):
                        print("\t Update: TOp = ", x, top[x], end = ' ')
                    top[x] = y_max_curr
                    bottom[x] = y_min_curr
                    if (check):
                        print(top[x])
                    x += sx
                    y_max_curr = top[x]
                    y_min_curr = bottom[x]
                else:
                    y += sy
                e -= 2 * dx
            else:
                if not change:
                    if (check):
                        print("\t Update: TOp = ", x, top[x], end = ' ')
                    top[x] = y_max_curr
                    bottom[x] = y_min_curr
                    if (check):
                        print(top[x])
                    x += sx
                    y_max_curr = top[x]
                    y_min_curr = bottom[x]
                else:
                    y += sy
                e += 2 * dy
    except:
        print("***************************")
        
    if (check):
        print("\t Update: TOp = ", x, top[x], end = ' ')
        top[x] = y_max_curr
        bottom[x] = y_min_curr
    if (check):
        print(top[x])
    return top, bottom


if __name__ == "__main__":
    pass
