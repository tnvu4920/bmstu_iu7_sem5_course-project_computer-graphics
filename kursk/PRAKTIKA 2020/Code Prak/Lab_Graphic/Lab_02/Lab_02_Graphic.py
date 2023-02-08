# Lab 02 Graphic
#Nguyen Phuoc Sang
#IU7-46B

import math
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
pi = 3.14

step = []
x_t = []
y_t = []
x_x = []
f_x = []
minn = 0
maxx = 0

'''
*****************************
Function
y = b * cos(t) ^ 3
x = b * sin(t) ^ 3
t = [0 .. 2pi]
*****************************
'''
def y(t):
    return np.cos(t) ** 3
def x(t):
    return np.sin(t) ** 3

def f(x):
    return x

def fx(x_t, b):
    n = len(x_t)
    h = int(n / 4)
    f = [-x - b for x in x_t[0 : h]]
    f.extend([x + b for x in x_t[h : 2 * h]])
    f.extend([-x + b for x in x_t[2 * h : 3 * h]])
    f.extend([x - b for x in x_t[3 * h: 4 * h]])
    return f

'''
*****************************
Draw Graphic
*****************************
'''

# draw line
def draw_line(A, B, color):
    plt.plot([A[0], B[0]], [A[1], B[1]], color, linewidth = 0.8)

# draw point
def draw_point(A, color, text, k):
    plt.plot([A[0]], [A[1]], color + 'o')
    plt.text(A[0] + k, A[1] + k, '{}.({}, {})'.format(text, round(A[0], 2), round(A[1], 2)), fontsize = 7)

# draw graph
def draw_graph():
    plt.clf()
    plt.axis("scaled")
    global minn, maxx

    k = (maxx - minn) * 0.01
    if (maxx * minn < 0):
        # ve Ox
        draw_line([0, minn + 5*k], [0, maxx - 5*k], 'k')
        plt.plot([maxx - 5*k], [0], 'k>')
        plt.text(maxx - 5*k, k, 'X')
        # ve Oy
        draw_line([minn + 5*k, 0], [maxx - 5*k, 0], 'k')
        plt.plot([0], [maxx - 5*k], 'k^')
        plt.text(k, maxx - 5*k, 'Y')
        # ve O
        draw_point([0, 0], 'k', "O", k)
    else:
        # ve Ox
        draw_line([minn + 5*k, minn + 5*k], [minn + 5*k, maxx - 5*k], 'k')
        plt.plot([maxx - 5*k], [minn + 5*k], 'k>')
        plt.text(maxx - 5*k, minn + 5*k + k, "X")
        # ve Oy
        draw_line([minn + 5*k, minn + 5*k], [maxx - 5*k, minn + 5*k], 'k')
        plt.plot([minn + 5*k], [maxx - 5*k], 'k^')
        plt.text(minn  + 5*k + k, maxx - 5*k, "Y")
        # ve O
        draw_point([minn + 5*k, minn + 5*k], 'k', "O", k)
    
    plt.axis([minn, maxx, minn ,maxx])
    plt.grid()
    plt.plot(x_t, y_t)
    plt.plot(x_x, f_x)
    for i in range(5, len(x_t), 10):
        plt.plot([x_x[i], x_t[i]], [f_x[i], y_t[i]], 'b')

    plt.show()

# Solution

def draw_init():
    global x_t, y_t
    global f_x, x_x
    global minn, maxx
    b = float(bString.get())
    t = np.linspace(start=-pi, stop=pi, num= 500)
    x_t = b * x(t)
    y_t = b * y(t)
    x_t = list(x_t)
    y_t = list(y_t)
    f_x = list(fx(x_t, b))
    x_x = list([i for i in x_t])
    minn = min(x_t + y_t + x_x + f_x) * 6
    maxx = max(x_t + y_t + x_x + f_x) * 6
    
    draw_graph()

'''
*****************************

Move Graph

*****************************
'''
def move(A, dx, dy):
    return [A[0] + dx, A[1] + dy]

def move_graph(atr):
    dx = atr[0]
    dy = atr[1]
    global x_t
    global y_t
    global f_x
    global x_x
    points = [move([x, y], dx, dy) for x, y in zip(x_t, y_t)]
    y_t = [p[1] for p in points]
    x_t = [p[0] for p in points]
    points = [move([x, y], dx, dy) for x, y in zip(x_x, f_x)]
    f_x = [p[1] for p in points]
    x_x = [p[0] for p in points]
    draw_graph()

def move_function():
    try:
        dx = float(dxString.get())
        dy = float(dyString.get())
    except:
        return
    step.append(['move', [-dx, -dy]])
    move_graph([dx, dy])
    
'''
****************************

Scale Graph

****************************
'''

def scale(A, kx, ky, M):
    x = kx * A[0] + (1 - kx) * M[0]
    y = ky * A[1] + (1 - ky) * M[1]
    return [x, y]

def scale_graph(atr):
    kx = atr[0]
    ky = atr[1]
    M = atr[2]
    global x_t
    global y_t
    global x_x
    global f_x
    points = [scale([x, y], kx, ky, M) for x, y in zip(x_t, y_t)]
    x_t = [p[0] for p in points]
    y_t = [p[1] for p in points]
    points = [scale([x, y], kx, ky, M) for x, y in zip(x_x, f_x)]
    x_x = [p[0] for p in points]
    f_x = [p[1] for p in points]
    plt.clf()
    draw_graph()

def scale_function():
    kx = float(kxString.get())
    ky = float(kyString.get())
    M = list(map(float, mString.get().split()))
    step.append(['scale', [1 / kx, 1 / ky, M]])
    scale_graph([kx, ky, M])

'''
***************************

Rotate Graph

***************************
'''

def rotation(A, alpha, C):
    cosa = np.cos(alpha)
    sina= np.sin(alpha)
    x = C[0] + (A[0] - C[0]) * cosa + (A[1] - C[1]) * sina
    y = C[1] - (A[0] - C[0]) * sina + (A[1] - C[1]) * cosa
    return [x, y]
    

def rotate_graph(atr):
    angle = atr[0]
    C = atr[1]
    global x_t
    global y_t
    global x_x
    global f_x
    points = [rotation([x, y], angle, C) for x, y in zip(x_t, y_t)]
    x_t = [p[0] for p in points]
    y_t = [p[1] for p in points]
    points = [rotation([x, y], angle, C) for x, y in zip(x_x, f_x)]
    x_x = [p[0] for p in points]
    f_x = [p[1] for p in points]
    
    draw_graph()

def rotate_function():
    angle = - float(angleString.get()) / 180 * pi
    C = list(map(float, cString.get().split()))
    step.append(['rotation', [-angle, C]])
    rotate_graph([angle, C])

'''
**************************

Returrn Back

*************************
'''
    
def back():
    global step
    n = len(step)
    if (n == 0):
        return
    else:
        s = step.pop(n - 1)
        if (s[0] == "rotation"):
            rotate_graph(s[1])
        elif (s[0] == "move"):
            move_graph(s[1])
        elif (s[0] == "scale"):
            scale_graph(s[1])
            
            

'''
***************************

Tkinter

***************************
'''

root = Tk()
root.title("Lab 02")
root.minsize(height = 150, width = 200)


# input function
bString = StringVar()
Label(root, text = "Input Graph: ",).grid(column = 0, row = 0, columnspan = 2)
Label(root, text = "B = ",).grid(column = 0, row = 1)
Entry(root, textvariable = bString,).grid(column = 1, row = 1)
Button(root, text = "Add", command = draw_init).grid(column = 0, row = 2, columnspan = 2) 


# Move Graph
dxString = StringVar()
dyString = StringVar()
# input Dx
Label(root, text = "Dx = ",).grid(column = 0, row = 3)
Entry(root, textvariable = dxString,).grid(column = 1, row = 3)

# input Dy
Label(root, text = "Dy = ",).grid(column = 0, row = 4)
Entry(root, textvariable = dyString,).grid(column = 1, row = 4)
Button(root, text = "Move Graph", command = move_function).grid(column = 0, row = 5, columnspan = 2)


# Rotation

angleString = StringVar()
cString = StringVar()

# Input Angle
Label(root, text = "Angle = ",).grid(column = 0, row = 6)
Entry(root, textvariable = angleString,).grid(column = 1, row = 6)

# Input Point C - Center
Label(root, text = "C = ",).grid(column = 0, row = 7)
Entry(root, textvariable = cString,).grid(column = 1, row = 7)

Button(root, text = "Rotation", command = rotate_function).grid(column = 0, row = 8, columnspan = 2)

# Scale
kxString = StringVar()
kyString = StringVar()
mString = StringVar()
#Input Kx
Label(root, text = "Kx = ",).grid(column = 0, row = 9)
Entry(root, textvariable = kxString,).grid(column = 1, row = 9)

# input Dy
Label(root, text = "Ky = ",).grid(column = 0, row = 10)
Entry(root, textvariable = kyString,).grid(column = 1, row = 10)

# Input Point M
Label(root, text = "M = ",).grid(column = 0, row = 11)
Entry(root, textvariable = mString,).grid(column = 1, row = 11)

Button(root, text = "Scale", command = scale_function).grid(column = 0, row = 12, columnspan = 2)

# Return Back

Button(root, text = "<< Back", command = back).grid(column = 0, row = 13, columnspan = 2)


root.mainloop()






