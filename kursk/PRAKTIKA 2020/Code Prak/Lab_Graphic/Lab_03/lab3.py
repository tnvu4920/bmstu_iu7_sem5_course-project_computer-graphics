import random
from math import *
from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import time

count = 0

def ROUND(a):
  return int(a + 0.5)

line_color = 'black'
bg_color = 'white'

'''
******************************************
Thuật toán DDA

*****************************************
'''
def line_DDA(x1,y1,x2,y2):
  x,y = x1,y1
  global count
  dx = abs(x2 - x1)
  dy = abs(y2 - y1)
  length = dx if dx > dy else dy
  dx = dx/float(length)
  dy = dy/float(length)
  for i in range(int(length)):
    count += 1
    img.put(line_color, (ROUND(x),ROUND(y)))
    x += (x2 - x1) / float(length)
    y += (y2 - y1) / float(length)

def sign(n):
    if n > 0:
        return 1
    elif n == 0:
      return 0
    return -1

def line_DDA_t(x1,y1,x2,y2):
  x,y = x1,y1
  dx = abs(x2 - x1)
  dy = abs(y2 - y1)
  length = dx if dx > dy else dy
  dx = dx/float(length)
  dy = dy/float(length)
  for i in range(int(length)):
    #img.put(line_color, (ROUND(x),ROUND(y)))
    x += dx
    y += dy

def sign(n):
    if n > 0:
        return 1
    elif n == 0:
      return 0
    return -1
'''
*****************************************
Brezenham Int

*****************************************
'''
def line_Brezenham_int(x1, y1, x2, y2):
    x, y = x1, y1
    dx = (x2 - x1)
    dy = (y2 - y1)
    delx = sign(dx)
    dely = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    if dx > dy:
        obmen = 0
    else:
        obmen = 1
        t = dx
        dx= dy
        dy = t
    e = 2 * dy - dx
    while (x != x2 or y != y2):
        img.put(line_color, (int(x),int(y)))
        if e > 0:
            if obmen == 0:
                y += dely
            else:
                x += delx
            e -= 2 * dx
        else:
            if obmen == 0:
                x += delx
            else:
                y += dely

            e += 2 * dy

def line_Brezenham_int_t(x1, y1, x2, y2):
    x, y = x1, y1
    dx = (x2 - x1)
    dy = (y2 - y1)
    delx = sign(dx)
    dely = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    if dx > dy:
        obmen = 0
    else:
        obmen = 1
        t = dx
        dx= dy
        dy = t
    e = 2 * dy - dx
    while (x != x2 or y != y2):
        #img.put(line_color, (int(x),int(y)))
        if e > 0:
            if obmen == 0:
                y += dely
            else:
                x += delx
            e -= 2 * dx
        else:
            if obmen == 0:
                x += delx
            else:
                y += dely

            e += 2 * dy


'''
*********************************************************
Brezenham Float

*********************************************************

'''
def line_Brezenham_float(x1, y1, x2, y2):
    x, y = x1, y1
    global count
    dx = (x2 - x1)
    dy = (y2 - y1)
    delx = sign(dx)
    dely = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    if dx > dy:
        obmen = 0
    else:
        obmen = 1
        t = dx
        dx= dy
        dy = t
    m = dy / dx
    e = m - 1/2
    while (x != x2 or y != y2):
        count += 1
        img.put(line_color, (int(x),int(y)))
        if e > 0:
            if obmen == 0:
                y += dely
            else:
                x += delx
            e -= 1
        else:
            if obmen == 0:
                x += delx
            else:
                y += dely

            e += m

def line_Brezenham_float_t(x1, y1, x2, y2):
    x, y = x1, y1
    dx = (x2 - x1)
    dy = (y2 - y1)
    delx = sign(dx)
    dely = sign(dy)
    dx = abs(dx)
    dy = abs(dy)
    if dx > dy:
        obmen = 0
    else:
        obmen = 1
        t = dx
        dx= dy
        dy = t
    m = dy / dx
    e = m - 1/2
    while (x != x2 or y != y2):
        #img.put(line_color, (int(x),int(y)))
        if e > 0:
            if obmen == 0:
                y += dely
            else:
                x += delx
            e -= 1
        else:
            if obmen == 0:
                x += delx
            else:
                y += dely

            e += m
'''
*******************************************
Brezenham 2
*******************************************
'''

def get_rgb_intensity(color, intensity):
    grad = []
    (r1, g1, b1) = canvas.winfo_rgb(color) # разложение цвета линни на составляющие ргб
    (r2, g2, b2) = canvas.winfo_rgb(bg_color) # разложение цвета фона на составляющие ргб
    r_ratio = float(r2 - r1) / intensity # получение шага интенсивности
    g_ratio = float(g2 - g1) / intensity
    b_ratio = float(b2 - b1) / intensity
    for i in range(intensity):
        nr = int(r1 + (r_ratio * i)) # заполнение массива разными оттенками
        ng = int(g1 + (g_ratio * i))
        nb = int(b1 + (b_ratio * i))
        grad.append("#%4.4x%4.4x%4.4x" % (nr, ng, nb))
    grad.reverse()
    return grad


def line_Brezenham(x1, y1, x2, y2):
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    I = 100
    colors = get_rgb_intensity(line_color, I)
    dx = x2 - x1
    dy = y2 - y1
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)
    if dy >= dx:
        dx, dy = dy, dx
        obmen = 1
    else:
        obmen = 0
    tg = dy / dx * I
    e = I / 2
    w = I - tg
    x = x1
    y = y1
    while x != x2 or y != y2:
        I1 = int(round(e) - 1)
        img.put(colors[I1], (int(x),int(y)))
        if e < w:
            if obmen == 0:
                x += sx
            else:
                y += sy
            e += tg
        elif e >= w:
            x += sx
            y += sy
            e -= w
            st = 0

def line_Brezenham_t(x1, y1, x2, y2):
    I = 100
    colors = get_rgb_intensity(line_color, I)
    dx = x2 - x1
    dy = y2 - y1
    sx = sign(dx)
    sy = sign(dy)
    dy = abs(dy)
    dx = abs(dx)
    if dy >= dx:
        dx, dy = dy, dx
        obmen = 1
    else:
        obmen = 0
    tg = dy / dx * I
    e = I / 2
    w = I - tg
    x = x1
    y = y1
    while x != x2 or y != y2:
        I1 = int(round(e) - 1)
        #img.put(colors[I1], (int(x),int(y)))
        if e < w:
            if obmen == 0:
                x += sx
            else:
                y += sy
            e += tg
        elif e >= w:
            x += sx
            y += sy
            e -= w

def ipart(x):
  return int(x)

def fpart(x):
  return x - int(x)

def rfpart(x):
  return 1 - fpart(x)
def line_Wu(x1, y1, x2, y2):

    I = 100
    colors = get_rgb_intensity(line_color, I)
    if x1 == x2 and y1 == y2:
      img.put(line_color, (int(x1),int(y1)))
    steep = abs(y2 - y1) > abs(x2 - x1)

    dx = x2 - x1
    dy = y2 - y1
    if (abs(dx) < abs(dy)):
      x1, y1 = y1, x1
      x2, y2 = y2, x2
      dx, dy = dy, dx
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        
    if dx == 0:
        m = 1
    else:
        m = dy / dx

    # first endpoint
    xend = round(x1)
    yend = y1 + m * (xend - x1)
    xgap = rfpart(x1 + 0.5)
    xpxl1 = xend
    ypxl1 = ipart(yend)
    I1 = int((I - 1) * (rfpart(yend) * xgap))
    img.put(colors[I1], (int(xpxl1),int(ypxl1))) # độ sáng: rfpart(yend) * xgap
    I1 = int((I - 1) * (fpart(yend) * xgap))
    img.put(colors[I1], (int(xpxl1),int(ypxl1 + 1))) # độ sáng: fpart(yend) * xgap

    y = yend + m

    # second endpoint
    xend = int(x2 + 0.5)
    yend = y2 + m * (xend - x2)
    xgap = fpart(x2 + 0.5)
    xpxl2 = xend
    ypxl2 = ipart(yend)
    I1 = int((I - 1) * rfpart (yend) * xgap)
    img.put(colors[I1], (int(xpxl2),int(ypxl2))) # độ sáng: rfpart(yend) * xgap
    I1 = int((I - 1) * fpart (yend) * xgap)
    img.put(colors[I1], (int(xpxl2),int(ypxl2 + 1))) # độ sáng: rfpart(yend) * xgap

    #main loop
    for x in range(xpxl1, xpxl2):
      if (steep == 0):
        I1 = int((I - 1) * rfpart(y))
        img.put(colors[I1], (int(x),int(ipart(y)))) # độ sáng: rfpart(yend) * xgap
        I1 = int((I - 1) * fpart(y))
        img.put(colors[I1], (int(x),int(ipart(y + 1)))) # độ sáng: rfpart(yend) * xgap
        y += m
      else:
        I1 = int((I - 1) * rfpart(y))
        img.put(colors[I1], (int(ipart(y)), int(x))) # độ sáng: rfpart(yend) * xgap
        I1 = int((I - 1) * fpart(y))
        img.put(colors[I1], (int(ipart(y + 1)), int(x))) # độ sáng: rfpart(yend) * xgap
        y += m
        
        

def line_Wu_t(x1, y1, x2, y2):

    I = 100
    colors = get_rgb_intensity(line_color, I)
    #if x1 == x2 and y1 == y2:
      #img.put(line_color, (int(x1),int(y1)))
      
    steep = abs(y2 - y1) > abs(x2 - x1)

    dx = x2 - x1
    dy = y2 - y1
    if (abs(dx) < abs(dy)):
      x1, y1 = y1, x1
      x2, y2 = y2, x2
      dx, dy = dy, dx
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        
    if dx == 0:
        m = 1
    else:
        m = dy / dx

    # first endpoint
    xend = round(x1)
    yend = y1 + m * (xend - x1)
    xgap = rfpart(x1 + 0.5)
    xpxl1 = xend
    ypxl1 = ipart(yend)
    I1 = int((I - 1) * (rfpart(yend) * xgap))
    #img.put(colors[I1], (int(xpxl1),int(ypxl1))) # độ sáng: rfpart(yend) * xgap
    I1 = int((I - 1) * (fpart(yend) * xgap))
    #img.put(colors[I1], (int(xpxl1),int(ypxl1 + 1))) # độ sáng: fpart(yend) * xgap

    y = yend + m

    # second endpoint
    xend = int(x2 + 0.5)
    yend = y2 + m * (xend - x2)
    xgap = fpart(x2 + 0.5)
    xpxl2 = xend
    ypxl2 = ipart(yend)
    I1 = int((I - 1) * rfpart (yend) * xgap)
    #img.put(colors[I1], (int(xpxl2),int(ypxl2))) # độ sáng: rfpart(yend) * xgap
    I1 = int((I - 1) * fpart (yend) * xgap)
    #img.put(colors[I1], (int(xpxl2),int(ypxl2 + 1))) # độ sáng: rfpart(yend) * xgap

    #main loop
    for x in range(xpxl1, xpxl2):
      I1 = int((I - 1) * rfpart(y))
      #img.put(colors[I1], (int(x),int(ipart(y)))) # độ sáng: rfpart(yend) * xgap
      I1 = int((I - 1) * fpart(y))
      #img.put(colors[I1], (int(x),int(ipart(y + 1)))) # độ sáng: rfpart(yend) * xgap
      y += m


'''
Stand
'''
def line_stand(x1, y1, x2, y2):
  canvas.create_line(x1, y1, x2, y2)



methods_arr = (line_DDA, line_Brezenham_float, line_Brezenham_int, line_Brezenham, line_Wu, line_stand)
methods_analyze_arr = (line_DDA_t, line_Brezenham_float_t, line_Brezenham_int_t, line_Brezenham_t, line_Wu_t)


'''
'''
def draw_axes():
    color = 'gray'
    canv.create_line(0, 2, can_width, 2, fill="gray", arrow=LAST)
    canv.create_line(2, 0, 2, can_height, fill="gray", arrow=LAST)
    for i in range(50, can_width, 50):
        #canv.create_text(i, 10, text=str(abs(i)), fill=color)
        canv.create_line(i, 0, i, 5, fill=color)

    for i in range(50, can_height, 50):
        #canv.create_text(15, i, text=str(abs(i)), fill=color)
        canv.create_line(0, i, 5, i, fill=color)
        
def line_draw():
  print("Da VE")
  method_id = methods_list.curselection()
  if ( len(method_id) != 1):
    messagebox.showwarning('Error Input','Please, Choose Method!!!')
  else:
    try:
      x1 = float(x1String.get())
      y1 = float(y1String.get())
      x2 = float(x2String.get())
      y2 = float(y2String.get())
    except:
      messagebox.showwarning('Error Input','Error: Input Points')
    methods_arr[method_id[0]](x1, y1, x2, y2)

      
  return

def clear():
  canv.delete("all")
  draw_axes()
  global img
  img = PhotoImage(width=can_width, height=can_height)
  canv.create_image((can_width//2, can_height//2), image=img, state="normal")
  print("Clear")

def rotation(A, alpha, C):
    alpha = alpha * pi / 180
    cosa = cos(alpha)
    sina= sin(alpha)
    x = C[0] + (A[0] - C[0]) * cosa + (A[1] - C[1]) * sina
    y = C[1] - (A[0] - C[0]) * sina + (A[1] - C[1]) * cosa
    return [x, y]


'''
************************************************
Step Analyze

************************************************
'''
def step_analyze():
  try:
    x = float(x3String.get())
    y = float(y3String.get())
    angle = float(angleString.get())
    method_id = methods_list.curselection()
    if (len(method_id) != 1):
      messagebox.showwarning('Error Input','Please, Choose Method!!!')
      return
    l = float(lenString.get())
  except:
      messagebox.showwarning('Error Input','Error: Input')
      return
  M= [x, y]
  N = [x + l, y]
  count1 = 0
  while (count1 < 360):
      methods_arr[method_id[0]](int(M[0]), int(M[1]), int(N[0]), int(N[1]))
      N = rotation(N, angle, M)
      count1 += angle
  global count
  print(count)
  count = 0


'''
******************************************
Time Analyze

******************************************
'''
def close_plt():
    plt.figure(1)
    plt.close()
    plt.figure(2)
    plt.close()

def time_cal(method, angle, x1, y1, x2, y2):
  summ = 0
  step = int(360 / angle)
  
  for i in range(step):
    tbeg = time.time()
    for i in range(1):
      method(x1, y1, x2, y2)
    tend = time.time()
    rotation([x1, y1], angle, [x2, y2])
    summ += tend - tbeg
  return summ / step

def draw_time():
    close_plt()
    plt.figure(2, figsize=(9, 7))
    times = []
    angle = 1
    length = 2000
    A = [center[0], center[1]]
    B = [center[0] + length, center[1]]
    for i in range(5):
        times.append(time_cal(methods_analyze_arr[i], 1, A[0], A[1], B[0], B[1]))
    clear()
    #times.sort(reverse = TRUE)
    if (times[1] < times[2]):
      times[1], times[2] = times[2], times[1]
    Y = range(len(times))
    L = ('DDA', 'Bresenham\nFloat',
         'Bresenham\n Int', 'Bresenham', 'Wu')
    plt.bar(Y, times, align='center')
    plt.xticks(Y, L)
    plt.ylabel("Work time in sec. (line len. " + str(length) + ")")
    plt.show()
  
def time_compare():
  print("Time COmpare")
  draw_time()

def set_line_color(color):
  global line_color
  line_color = color

def set_bg_color(color):
  global bg_color
  bg_color = color

'''
**********************************************
Phần đồ hoạ
Graphic
**********************************************
'''

#Khởi tạo GUI
root = Tk()
root.geometry('1000x750')
root.title("Lab 03 Graphic")
root.resizable(0, 0)


# Phần Input

#Input Tạo Độ
x1String = StringVar()
x2String = StringVar()
y1String = StringVar()
y2String = StringVar()

Label(root, text = "Input Lines",).grid(column = 0, row = 0, columnspan = 2)

#Input x1, y1
Label(root, text = "x1",).grid(column = 0, row = 1)
Entry(root, textvariable = x1String,).grid(column = 1, row = 1)
Label(root, text = "y1",).grid(column = 0, row = 2)
Entry(root, textvariable = y1String,).grid(column = 1, row = 2)
#Input x2, y2
Label(root, text = "x2",).grid(column = 0, row = 3)
Entry(root, textvariable = x2String,).grid(column = 1, row = 3)
Label(root, text = "y2",).grid(column = 0, row = 4)
Entry(root, textvariable = y2String,).grid(column = 1, row = 4)


#Chose Method
Label(root, text = "Please Choose Method:",).grid(column = 0, row = 5, columnspan = 2)
methods_list = Listbox(root, selectmode = EXTENDED, height=6)
methods_list.grid(column = 0, row = 6, columnspan = 2, )
methods_list.insert(END, "DDA")
methods_list.insert(END, "Brezenham (Float)")
methods_list.insert(END, "Brezenham (Integer)")
methods_list.insert(END, "Brezenham")
methods_list.insert(END, "Wu")
methods_list.insert(END, "Standart")

color_arr = ('Red', 'Blue', 'Black', 'While', 'Yellow', 'Green')
#Input Color
Label(root, text = "Choise Line Color",).grid(column = 0, row = 7, columnspan = 2)

Button(root, bg="red", activebackground="red", width = 10, command=lambda: set_line_color("red")).grid(column = 0, row = 8)
Button(root, bg="blue", activebackground="blue", width = 10, command=lambda: set_line_color("blue")).grid(column = 1, row = 8)
Button(root, bg="yellow", activebackground="yellow", width = 10, command=lambda: set_line_color("yellow")).grid(column = 0, row = 9)
Button(root, bg="black", activebackground="black", width = 10, command=lambda: set_line_color("black")).grid(column = 1, row = 9)

Label(root, text = "Choise Bg Color",).grid(column = 0, row = 10, columnspan = 2)
Button(root, bg="red", activebackground="red", width = 10, command=lambda: set_bg_color("red")).grid(column = 0, row = 11)
Button(root, bg="blue", activebackground="blue", width = 10, command=lambda: set_bg_color("blue")).grid(column = 1, row = 11)
Button(root, bg="yellow", activebackground="yellow", width = 10, command=lambda: set_bg_color("yellow")).grid(column = 0, row = 12)
Button(root, bg="black", activebackground="black", width = 10, command=lambda: set_bg_color("black")).grid(column = 1, row = 12)

'''color_list.grid(column = 0, row = 8, columnspan = 2, )
color_list.insert(END, "Red")
color_list.insert(END, "Blue")
color_list.insert(END, "Black")
color_list.insert(END, "White")
color_list.insert(END, "Yellow")
color_list.insert(END, "Green")'''
#Draw Button

Button(root, text = "Draw Line", command = line_draw).grid(column = 0, row = 13, columnspan = 2)
Button(root, text = "Clear", command = clear).grid(column = 0, row = 14, columnspan = 2)

#COmpare
Button(root, text = "Time Compare", command = time_compare).grid(column = 0, row = 15, columnspan = 2)

x3String = StringVar()
y3String = StringVar()
lenString = StringVar()
angleString = StringVar()
Label(root, text = "x3",).grid(column = 0, row = 16)
Entry(root, textvariable = x3String,).grid(column = 1, row = 16)
Label(root, text = "y3",).grid(column = 0, row = 17)
Entry(root, textvariable = y3String,).grid(column = 1, row = 17)
Label(root, text = "Length:",).grid(column = 0, row = 18)
Entry(root, textvariable = lenString,).grid(column = 1, row = 18)
Label(root, text = "Aggle",).grid(column = 0, row = 19)
Entry(root, textvariable = angleString,).grid(column = 1, row = 19)
Button(root, text = "Step Analyze", command = step_analyze).grid(column = 0, row = 20, columnspan = 2)

can_width = 750
can_height = 600
center = (can_width / 2, can_height / 2)
canv = Canvas(root, width=can_width, height=can_height, bg= bg_color)
canvas = canv
canv.grid(row = 0, column = 2, rowspan = 20)
img = PhotoImage(width=can_width, height=can_height)
canv.create_image((can_width//2, can_height//2), image=img, state="normal")

draw_axes()
root.mainloop()





























