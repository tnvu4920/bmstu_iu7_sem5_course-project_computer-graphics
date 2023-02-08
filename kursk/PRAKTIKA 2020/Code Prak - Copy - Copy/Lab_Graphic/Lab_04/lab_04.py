import random
from math import *
from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
import time

line_color = 'black'
bg_color = 'white'

def plot_4_point(x, y, xc, yc):
    x, y, xc, yx = int(x), int(y), int(xc), int(yc)
    try:
        img.put(line_color, (xc + x, yc + y))
        img.put(line_color, (xc + x, yc - y))
        img.put(line_color, (xc - x, yc - y))
        img.put(line_color, (xc - x, yc + y))
    except:
        print()
    return
        
'''
**********************************************
Draw circle
**********************************************
'''
def circle_bresenham(xc, yc, R):
    x = 0
    y = R
    deli = 2 * (1 - R)
    while (y >= 0):
        plot_4_point(x, y, xc, yc)
        if (deli < 0):
            err1 = 2 * deli + 2 * y - 1
            if (err1 <= 0): #gorizontal
                x += 1
                deli += 2 * x + 1
            else: #diag
                x += 1
                y -= 1
                deli += 2 * (x - y + 1)
        elif (deli > 0):
            err2 = 2 * deli - 2 * x - 1
            if (err2 <=0): # diag
                x += 1
                y -= 1
                deli += 2 * (x - y + 1)
            else: # vertical
                y -= 1
                deli += 1 - 2 * y
        else: #diag
            x += 1
            y -= 1
            deli += 2 * (x - y + 1)

def circle_bresenham_test(xc, yc, R):
    x = 0
    y = R
    deli = 2 * (1 - R)
    while (y >= 0):
        #plot_4_point(x, y, xc, yc)
        if (deli < 0):
            err1 = 2 * deli + 2 * y - 1
            if (err1 <= 0): #gorizontal
                x += 1
                deli += 2 * x + 1
            else: #diag
                x += 1
                y -= 1
                deli += 2 * (x - y + 1)
        elif (deli > 0):
            err2 = 2 * deli - 2 * x - 1
            if (err2 <=0): # diag
                x += 1
                y -= 1
                deli += 2 * (x - y + 1)
            else: # vertical
                y -= 1
                deli += 1 - 2 * y
        else: #diag
            x += 1
            y -= 1
            deli += 2 * (x - y + 1)

def circle_midpoint(xc, yc, R):
    x = 0
    y = R
    plot_4_point(x, y, xc, yc)
    plot_4_point(y, x, xc, yc)
    f = int(5/4 - R) # f = (0 + 1)**2 + (R - 1/2) **2 - R**2 = -R + 5/4 
    while (x < y):
        x += 1
        if (f < 0): # gorizontal M in circle
            f += 2 * x + 1
        else:
            y -= 1
            f += 2 * (x - y) + 1
        plot_4_point(x, y, xc, yc)
        plot_4_point(y, x, xc, yc)

def circle_midpoint_test(xc, yc, R):
    x = 0
    y = R
    #plot_4_point(x, y, xc, yc)
    #plot_4_point(y, x, xc, yc)
    f = int(5/4 - R) # f = (0 + 1)**2 + (R - 1/2) **2 - R**2 = -R + 5/4 
    while (x < y):
        x += 1
        if (f < 0): # gorizontal M in circle
            f += 2 * x + 1
        else:
            y -= 1
            f += 2 * (x - y) + 1
        #plot_4_point(x, y, xc, yc)
        #plot_4_point(y, x, xc, yc)


def circle_canon(xc, yc, R):
    r2 = R * R
    x_M = round(R / sqrt(2))

    x = 0
    while x <= x_M:
        y = round(sqrt(r2 - x * x))
        plot_4_point(x, y, xc, yc)
        x += 1

    y = round(sqrt(r2 - x_M * x_M))
    while (y >= 0):
        x = round(sqrt(r2 - y * y))
        plot_4_point(x, y, xc, yc)
        y -= 1

def circle_canon_test(xc, yc, R):
    r2 = R * R
    x_M = round(R / sqrt(2))

    x = 0
    while x <= x_M:
        y = round(sqrt(r2 - x * x))
        #plot_4_point(x, y, xc, yc)
        x += 1

    y = round(sqrt(r2 - x_M * x_M))
    while (y >= 0):
        x = round(sqrt(r2 - y * y))
        #plot_4_point(x, y, xc, yc)
        y -= 1

def circle_param(xc, yc, R):
    dt = 1 / R
    m = pi / 2 * 1.01
    alpha = 0
    while alpha <= m:
        x = round(R * cos(alpha))
        y = round(R * sin(alpha))
        plot_4_point(x, y, xc, yc)
        alpha += dt

def circle_param_test(xc, yc, R):
    dt = 1 / R
    m = pi / 2 * 1.01
    alpha = 0
    while alpha <= m:
        x = round(R * cos(alpha))
        y = round(R * sin(alpha))
        #plot_4_point(x, y, xc, yc)
        alpha += dt

def circle_stand(xc, yc, R):
    return


    

'''
Draw Elip
'''

def elip_bresenham(xc, yc, a, b):
    x = 0
    y = b

    b2 = b * b
    a2 = a * a
    bd = 2 * b2
    ad = 2 * a2

    deli = b2 + a2 -ad * b

    while (y >= 0):
        plot_4_point(x, y, xc, yc)
        if (deli < 0):
            err1 = 2 * deli + ad * y - a2
            if (err1 < 0): # gorizontal
                x += 1
                deli += bd * x + b2
            else: #diag
                x += 1
                y -= 1
                deli += bd * x + b2 + a2 - ad * y
        elif (deli > 0):
            err2 = 2 * deli - bd * x - b2
            if (err2 <= 0): #diag
                y -= 1
                x += 1
                deli += bd * x + b2 + a2 - ad * y
            else: # vertical
                y -= 1
                deli += a2 - ad * y
        else:
            y -= 1
            x += 1
            deli += bd * x + b2 + a2 - ad * y

def elip_canon(xc, yc, a, b):
    a2 = a * a
    b2 = b * b
    c = b / a
    x_C = round(a2 / sqrt(a2 + b2))
    x = 0
    while x <= x_C:
        y = round(b * 1.0 / a * sqrt(a2 - x*x))
        plot_4_point(x, y, xc, yc)
        x += 1
    y = round(c * sqrt(a2 - x_C * x_C))
    c = a / b
    while (y >= 0):
        x = round(a * 1.0 / b * sqrt(b2 - y * y))
        plot_4_point(x, y, xc, yc)
        y -= 1

def elip_midpoint(xc, yc, a, b):
    b2 = b*b
    a2 = a*a
    bd = 2 * b2
    ad = 2 * a2

    x = 0
    y = b
    dx = 0

    f = b2 - a2 * y + a2 / 4 # = (b2 * (0 + 1)**2 + a2 * (b - 1/2)**2 - a2*b2
    delf = -ad * y
    
    x_C = int(a2 / sqrt(a2 + b2))
    y_C = int(b2 / sqrt(a2 + b2))

    while (x <= x_C):
        plot_4_point(x, y, xc, yc)
        if (f > 0):
            y -= 1
            delf += ad
            f += delf
        dx += bd
        x += 1
        f += dx + b2

    f += 0.75 * (a2 - b2) - (b2 * x + a2 * y)
    delf = bd * x
    dy = -ad * y

    while y >= 0:
        plot_4_point(x, y, xc, yc)
        if (f < 0):
            x += 1
            delf += bd
            f += delf
        dy += ad
        f += dy + a2
        y -= 1


def elip_param(xc, yc, a, b):
    alpha = pi / 2
    dx = 1 / a
    dy = 1 / b
    a2 = a * a
    b2 = b * b

    t_x_C = acos(a2 / (a2 + b2))

    while alpha >= t_x_C:
        x = round(a * cos(alpha))
        y = round(b * sin(alpha))
        plot_4_point(x, y, xc, yc)
        alpha -= dx

    alpha = t_x_C
    while alpha >= -1:
        x = round(a * cos(alpha))
        y = round(b * sin(alpha))
        plot_4_point(x, y, xc, yc)
        alpha -= dy
        
def elip_stand(xc, yc, a, b):
    return




'''
******************************************************

Elip Time Test

******************************************************

'''

def elip_bresenham_test(xc, yc, a, b):
    x = 0
    y = b

    b2 = b * b
    a2 = a * a
    bd = 2 * b2
    ad = 2 * a2

    deli = b2 + a2 -ad * b

    while (y >= 0):
        #plot_4_point(x, y, xc, yc)
        if (deli < 0):
            err1 = 2 * deli + ad * y - a2
            if (err1 < 0): # gorizontal
                x += 1
                deli += bd * x + b2
            else: #diag
                x += 1
                y -= 1
                deli += bd * x + b2 + a2 - ad * y
        elif (deli > 0):
            err2 = 2 * deli - bd * x - b2
            if (err2 <= 0): #diag
                y -= 1
                x += 1
                deli += bd * x + b2 + a2 - ad * y
            else: # vertical
                y -= 1
                deli += a2 - ad * y
        else:
            y -= 1
            x += 1
            deli += bd * x + b2 + a2 - ad * y

def elip_midpoint_test(xc, yc, a, b):
    b2 = b*b
    a2 = a*a
    bd = 2 * b2
    ad = 2 * a2

    x = 0
    y = b
    dx = 0

    f = b2 - a2 * y + a2 / 4 # = (b2 * (0 + 1)**2 + a2 * (b - 1/2)**2 - a2*b2
    delf = -ad * y
    
    x_C = int(a2 / sqrt(a2 + b2))
    y_C = int(b2 / sqrt(a2 + b2))

    while (x <= x_C):
        #plot_4_point(x, y, xc, yc)
        if (f > 0):
            y -= 1
            delf += ad
            f += delf
        dx += bd
        x += 1
        f += dx + b2

    f += 0.75 * (a2 - b2) - (b2 * x + a2 * y)
    delf = bd * x
    dy = -ad * y

    while y >= 0:
        #plot_4_point(x, y, xc, yc)
        if (f < 0):
            x += 1
            delf += bd
            f += delf
        dy += ad
        f += dy + a2
        y -= 1

def elip_canon_test(xc, yc, a, b):
    a2 = a * a
    b2 = b * b
    c = b / a
    x_C = round(a2 / sqrt(a2 + b2))
    x = 0
    while x <= x_C:
        y = round(b * 1.0 / a * sqrt(a2 - x*x))
        #plot_4_point(x, y, xc, yc)
        x += 1
    y = round(c * sqrt(a2 - x_C * x_C))
    c = a / b
    while (y >= 0):
        x = round(a * 1.0 / b * sqrt(b2 - y * y))
        #plot_4_point(x, y, xc, yc)
        y -= 1


def elip_param_test(xc, yc, a, b):
    alpha = pi / 2
    dx = 1 / a
    dy = 1 / b
    a2 = a * a
    b2 = b * b

    t_x_C = acos(a2 / (a2 + b2))

    while alpha >= t_x_C:
        x = round(a * cos(alpha))
        y = round(b * sin(alpha))
        #plot_4_point(x, y, xc, yc)
        alpha -= dx

    alpha = t_x_C
    while alpha >= -1:
        x = round(a * cos(alpha))
        y = round(b * sin(alpha))
        #plot_4_point(x, y, xc, yc)
        alpha -= dy

circle_method = [circle_bresenham, circle_midpoint, circle_canon, circle_param, circle_stand]
elip_method = [elip_bresenham, elip_midpoint, elip_canon, elip_param, elip_stand]

circle_method_test = [circle_bresenham_test, circle_midpoint_test, circle_canon_test, circle_param_test]
elip_method_test = [elip_bresenham_test, elip_midpoint_test, elip_canon_test, elip_param_test]

def circle_draw():
    print("Da Ve Circle")
    
    method_id = methods_list.curselection()

    if ( len(method_id) != 1):
        messagebox.showwarning('Error Input','Please, Choose Method!!!')       
    else:
        try:
            r  = int(float(rString.get()))
            print("check")
            xc = int(float(xcString.get()))
            print("check")
            yc = int(float(ycString.get()))
            print("check")
        except:
            messagebox.showwarning('Error Input','Error: Input Points')
        circle_method[method_id[0]](xc, yc, r)

    return

def elip_draw():
    print("Da Ve Circle")
    method_id = methods_list.curselection()
    if ( len(method_id) != 1):
        messagebox.showwarning('Error Input','Please, Choose Method!!!')       
    else:
        try:
            a = int(float(aString.get()))
            b = int(float(bString.get()))
            xc = int(float(xcString.get()))
            yc = int(float(ycString.get()))
        except:
            messagebox.showwarning('Error Input','Error: Input Points')
        elip_method[method_id[0]](xc, yc, a, b)

    return



'''
*******************************************

Analyze

*******************************************
'''

def circle_time(method, xc, yc, r):
    tbeg = time.time()
    for i in range(500):
        method(xc, yc, r)
    tend = time.time()
    k = 1
    if method == circle_midpoint_test:
        k = 2
    return (tend - tbeg) * k

def circle_time_compare():
    close_plt()	

    names = ('Алгоритма Брезенхема',
             'Алгоритма средней точки',
             'Канонического уравнени',
             'Параметрического уравнения')
    plt.figure(1)
    plt.title("Time analysis")
    plt.xlabel("Radius")
    plt.ylabel("Time")
    plt.grid(True)
    #plt.legend(loc='best')

    radius = [i for i in range(10, 1000, 50)]
    xc = 500
    yc = 350
    start = 0
    end = 3
    for i in range(start, end, 1):#len(circle_method_test)):
        times = []

        for r in radius:
            times.append(circle_time(circle_method_test[i],xc, yc, r))
        #clear()
        plt.figure(1)
        plt.plot(radius, times, label=names[i])
        plt.legend()
    plt.show()    


def elip_time(method, xc, yc, a, b):
    tbeg = time.time()
    for i in range(0, 5, 1):
        method(xc, yc, a, b)
    tend = time.time()
    return (tend - tbeg)

def elip_time_compare():
    close_plt()	

    names = ('Алгоритма Брезенхема',
             'Алгоритма средней точки',
             'Канонического уравнени',
             'Параметрического уравнения')
    plt.figure(1)
    plt.title("Time analysis")
    plt.xlabel("A")
    plt.ylabel("Time")
    plt.grid(True)
    stepa = 200
    a = [i for i in range(10, 30000, stepa)]
    
    xc = 500
    yc = 350
    
    start = 0
    end = 4
    for i in range(start, end, 1):
        times = []
        b = 5
        stepb =  5 * stepa / 10

        for r in a:
            times.append(elip_time(elip_method_test[i],xc, yc, r, b))
            b += stepb
        #clear()
        plt.figure(1)
        plt.plot(a, times, label=names[i])
        plt.legend()
    plt.show() 


def circle_step_analyze():
    try:
        start = int(float(sString.get()))
        end = int(float(eString.get()))
        step = int(float(stepString.get()))
        xc = int(float(xcString.get()))
        yc = int(float(ycString.get()))
        method_id = methods_list.curselection()
        if (len(method_id) != 1):
            messagebox.showwarning('Error Input','Please, Choose Method!!!')
            return
    except:
      messagebox.showwarning('Error Input','Error: Input')

    while start <= end:
        circle_method[method_id[0]](xc, yc, start)
        start += step

def elip_step_analyze():
    try:
        start = int(float(sString.get()))
        end = int(float(eString.get()))
        step = int(float(stepString.get()))
        xc = int(float(xcString.get()))
        yc = int(float(ycString.get()))
        b = int(float(bString.get()))
        stepb = int(b * 1.0/ start * step)
        method_id = methods_list.curselection()
        if (len(method_id) != 1):
            messagebox.showwarning('Error Input','Please, Choose Method!!!')
            return
    except:
      messagebox.showwarning('Error Input','Error: Input')

    while start <= end:
        elip_method[method_id[0]](xc, yc, start, b)
        start += step
        b += stepb
    



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

def clear():
  canv.delete("all")
  draw_axes()
  global img

  img = PhotoImage(file = bg_color+'.png', width=can_width, height=can_height)
  canv.create_image((can_width//2, can_height//2), image=img, state="normal")
  print("Clear")

def close_plt():
    plt.figure(1)
    plt.close()
    plt.figure(2)
    plt.close()

def set_line_color(color):
  global line_color
  line_color = color

def set_bg_color(color):
  global bg_color
  bg_color = color            

  
'''
/***************************************************************

Phần Đồ Hoạ

/***************************************************************
'''




#Khởi tạo GUI
root = Tk()
root.geometry('1200x750')
root.title("Lab 03 Graphic")
root.resizable(0, 0)


row = 0

# Phần Input

row = 0
#Input Tạo Độ
aString = StringVar()
bString = StringVar()
rString = StringVar()
xcString = StringVar()
ycString = StringVar()

#Input a, b, R, xc, yc
Label(root, text = "a:",).grid(column = 0, row = row)
Entry(root, textvariable = aString,).grid(column = 1, row = row)

row += 1
Label(root, text = "b:",).grid(column = 0, row = row)
Entry(root, textvariable = bString,).grid(column = 1, row = row)

row += 1
Label(root, text = "R:",).grid(column = 0, row = row)
Entry(root, textvariable = rString,).grid(column = 1, row = row)

row += 1
Label(root, text = "xc",).grid(column = 0, row = row)
Entry(root, textvariable = xcString,).grid(column = 1, row = row)

row += 1
Label(root, text = "yc",).grid(column = 0, row = row)
Entry(root, textvariable = ycString,).grid(column = 1, row = row)

#Chose Method
row += 1
Label(root, text = "Please Choose Method:",).grid(column = 0, row = row, columnspan = 2)

row += 1
methods_list = Listbox(root, selectmode = EXTENDED, height = 5)
methods_list.grid(column = 0, row = row, columnspan = 2, )
methods_list.insert(END, "Bresenham")
methods_list.insert(END, "MidPoint")
methods_list.insert(END, "Canon")
methods_list.insert(END, "Para")
methods_list.insert(END, "Standart")

row += 1
color_arr = ('Red', 'Blue', 'Black', 'While', 'Yellow', 'Green')
Label(root, text = "Choise Line Color",).grid(column = 0, row = row, columnspan = 2)

row += 1
Button(root, bg="red", activebackground="red", width = 10, command=lambda: set_line_color("red")).grid(column = 0, row = row)
Button(root, bg="blue", activebackground="blue", width = 10, command=lambda: set_line_color("blue")).grid(column = 1, row = row)

row += 1
Button(root, bg="yellow", activebackground="yellow", width = 10, command=lambda: set_line_color("yellow")).grid(column = 0, row = row)
Button(root, bg="black", activebackground="black", width = 10, command=lambda: set_line_color("black")).grid(column = 1, row = row)

row += 1
Button(root, bg="green", activebackground="green", width = 10, command=lambda: set_line_color("green")).grid(column = 0, row = row)
Button(root, bg="white", activebackground="white", width = 10, command=lambda: set_line_color("white")).grid(column = 1, row = row)


row += 1
Label(root, text = "Choise Bg Color",).grid(column = 0, row = row, columnspan = 2)

row += 1
Button(root, bg="red", activebackground="red", width = 10, command=lambda: set_bg_color("red")).grid(column = 0, row = row)
Button(root, bg="blue", activebackground="blue", width = 10, command=lambda: set_bg_color("blue")).grid(column = 1, row = row)

row += 1
Button(root, bg="yellow", activebackground="yellow", width = 10, command=lambda: set_bg_color("yellow")).grid(column = 0, row = row)
Button(root, bg="black", activebackground="black", width = 10, command=lambda: set_bg_color("black")).grid(column = 1, row = row)

#Draw Button

row += 1
Button(root, text = "Draw Circle", command = circle_draw).grid(column = 0, row = row, columnspan = 2)

row += 1
Button(root, text = "Draw Elip", command = elip_draw).grid(column = 0, row = row, columnspan = 2)
row += 1
Button(root, text = "Clear", command = clear).grid(column = 0, row = row, columnspan = 2)

#COmpare
row += 1
Button(root, text = "Circle Time Compare", command = circle_time_compare).grid(column = 0, row = row, columnspan = 2)

row += 1
Button(root, text = "Circle Time Compare", command = elip_time_compare).grid(column = 0, row = row, columnspan = 2)

sString = StringVar()
eString = StringVar()
stepString = StringVar()
row += 1
Label(root, text = "start",).grid(column = 0, row = row)
Entry(root, textvariable = sString,).grid(column = 1, row = row)

row += 1
Label(root, text = "end",).grid(column = 0, row = row)
Entry(root, textvariable = eString,).grid(column = 1, row = row)

row += 1
Label(root, text = "Step:",).grid(column = 0, row = row)
Entry(root, textvariable = stepString,).grid(column = 1, row = row)

row += 1
Button(root, text = "Circle Step Analyze", command = circle_step_analyze).grid(column = 0, row = row, columnspan = 2)

row += 1
Button(root, text = "Elip Step Analyze", command = elip_step_analyze).grid(column = 0, row = row, columnspan = 2)


can_width = 1000
can_height = 700
center = (can_width / 2, can_height / 2)
canv = Canvas(root, width=can_width, height=can_height, bg= bg_color)
canvas = canv
canv.grid(row = 0, column = 2, rowspan = 30)
img = PhotoImage(width=can_width, height=can_height)
canv.create_image((can_width//2, can_height//2), image=img, state="normal")

draw_axes()
root.mainloop()
