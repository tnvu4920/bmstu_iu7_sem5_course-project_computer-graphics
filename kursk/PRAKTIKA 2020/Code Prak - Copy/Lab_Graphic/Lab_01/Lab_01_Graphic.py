#Nguyen Phuoc Sang
#IU7-46B
# Lab 01 - Graphic

from math import *
import matplotlib.pyplot as plt

'''
***************
input
***************
'''
EPS = 1e-10
data = []

#input points
def point_input(notif):
    while (1):
        try:
            point = list(map(float,input(notif).split()))
            if (len(point) < 2):
                print("\n!!! Wrong Input, please input again\n")
            else:
                return point[0:2]
        except:
            print("\n!!!Coordinates must be float, pleas input again !!!\n")
        
    

def data_input():

    n = int(input("Input Number of point: "))
    if (n < 0):
        print("\n!!! Number must be greater than 0\n")
        return n
    else:
        if (n <= 2):
            print("\n!!! Notice: Number must be greater than 2 \n")
    print("Input Data: ")
    for i in range(n):
        point = point_input("Input New Point: ")
        while (point in data):
            print("\n!!! Point was in List, please input again")
            point = point_input("Input New Point: ")
        data.append(point)
    return n


def print_menu():
    print("0. Continue")
    print("1. Delete all points")
    print("2. Delete 1 point")
    print("3. Insert 1 point")
    print("4. Change point")
    print("5. Print All Points")
# delete point
def del_point():
    point = point_input("Input Delete Point: ")
    if (point in data):
        data.pop(data.index(point))
    else:
        print("\n!!! Point not in List\n")

# insert new point
def insert_point():
    point = point_input("Input New Point: ")
    if (point in data):
        print("\n!!! Point was n List\n")
    else:
        data.append(point)

# change a point
def change_point():
    point1 = point_input('Input Old Point: ')
    if (point1 not in data):
        print("\n!!! Point not in list\n")
        return
    point2 = point_input("Input New Point: ")
    if (point2 not in data):
        data[data.index(point1)] = point2
    else:
        data.pop(data.index(point1))

#output all point
def print_point():
    if (len(data) == 0):
        print("\n Empty!!!\n")
        return
    print()
    for i in range(len(data)):
        print("Point {}: ({}, {})".format( i, data[i][0], data[i][1]))
    print()

def data_change():
    ch = 1
    while (ch != 0):
        print_menu()
        while (1):
            try:
                ch = int(input("Input your choise: "))
                if (ch in range(0, 6)):
                    break
                else:
                    print("\n!!! ERR: Your choise must be in range [0..5]")
            except:
                print("\n!!! ERR: Not an Interger")
                
        if (ch == 1):
            data = []
        elif (ch == 2):
            del_point()
        elif (ch == 3):
            insert_point()
        elif (ch == 4):
            change_point()
        elif (ch == 5):
            print_point()
        else:
            break
        
#*****************************************************************************************************************************
'''
***************
Process
***************
'''

#check data

def check_data(data):
    n = len(data)
    if (n <= 2):
        return -1
    
    l = line(data[0], data[1])
    for i in range(2, n, 1):
        if (check_in_line(data[i], l) == False):
            return 0
    return -2

# a,b - 2 points
def distance(a, b):
    return sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))

# a, b - 2 point
def vector_n(a, b):
    return list([a[1] - b[1], b[0] - a[0]]) 

# a, b - 2 points
def line(a, b):
    vec_n = vector_n(a, b)
    return [vec_n[0], vec_n[1], -1 * (vec_n[0] * a[0] + vec_n[1] * a[1])]

# a - point
# l - line
def check_in_line(a, l):
    if (l[0] * a[0] + l[1] * a[1] + l[2] != 0):
        return False
    return True

# find point I ( median)
def mid_point(a, b):
    return [ (a[0] + b[0]) / 2, (a[1] + b[1]) / 2]

#fie point D (bisector)
def bisector(A, B, C):
    vecAC = [C[0] - A[0], C[1] - A[1]]
    AB = distance(A, B)
    BC = distance(B, C)
    k = AB / BC + 1
    xD = C[0] - vecAC[0] / k
    yD = C[1] - vecAC[1] / k
    return [xD, yD]

# find angle ABC
def angle_ABC(A, B, C):
    AB = distance(A, B)
    BC = distance(B, C)
    AC = distance(A, C)
    try:
        cosB = (BC**2 + AB**2 - AC**2) / (2 * BC * AB)
    except:
        return 4
    return acos(cosB)

# ABC - Triangle
# BI - Median from B
# BD - Bisector from B
def find_angle(A, B, C):
    D = bisector(A, B, C)
    I = mid_point(A, C)
    IBD = angle_ABC(I, B, D)
    return [IBD, D, I]

def min_angle(A, B, C):
    angle_B = find_angle(A, B, C)
    angle_C = find_angle(B, C, A)
    angle_A = find_angle(C, A, B)
    minn = min(angle_A[0], angle_B[0], angle_C[0])
    if (fabs(angle_A[0] - minn) < EPS):
        return angle_A + [C, A, B]
    if (fabs(angle_B[0] - minn) < EPS):
        return angle_B + [A, B, C]
    if (fabs(angle_C[0] - minn) < EPS):
        return angle_C + [B, C, A]

def draw_line(A, B, color):
    plt.plot([A[0], B[0]], [A[1], B[1]], color, linewidth = 0.8)

def draw_point(A, color, text, k):
    plt.plot([A[0]], [A[1]], color + 'o')
    plt.text(A[0] + k, A[1] + k, '{}.({}, {})'.format(text, round(A[0], 2), round(A[1], 2)), fontsize = 7)

data = []
n = data_input()
#print(data)
#data = list([[13.0, -10.0], [-5.0, 17.0], [8, 13], [-3.0, 23.0], [25.0, 27.0]])
#n = len(data)
if ( n >= 0):
    ch = 1
    while (ch != 0):
        print_menu()
        while (1):
            try:
                ch = int(input("Input your choise: "))
                if (ch in range(0, 6)):
                    break
                else:
                    print("\n!!! ERR: Your choise must be in range [0..5]")
            except:
                print("\n!!! ERR: Not an Interger")
                
        if (ch == 1):
            data = []
        elif (ch == 2):
            del_point()
        elif (ch == 3):
            insert_point()
        elif (ch == 4):
            change_point()
        elif (ch == 5):
            print_point()
        else:
            break

    n = len(data)
    if (n >= 2):
        X = [data[i][0] for i in range(n)] 
        Y = [data[i][1] for i in range(n)]

        minX = min(X)
        maxX = max(X)
        minY = min(Y)
        maxY = max(Y)
        minn = min(minX, minY)
        maxx = max(maxX, maxY)
        k = (maxx - minn) * 0.01
    
    
err = check_data(data)
if (err == -1):
    print("\n!!!ERR: Number of point must be > 2")
    
elif (err == -2):
    print("\n!!!ERR: All Points in a line\n")
    for i in range(n):
        draw_point(data[i], 'b', i, k)
    draw_line([minX, minY], [maxX, maxY], 'r')
    
else:
    result = []
    minrc = 5.0
    for i in range(n - 2):
        for j in range(i + 1, n - 1, 1):
            for t in range(j + 1, n, 1):
                if (check_data([data[i], data[j], data[t]]) == 0):
                    rc = min_angle(data[i], data[j], data[t])
                    if (minrc > rc[0]):
                        minrc = rc[0]
                        result = [i, j, t] + rc
    A = result[6]
    B = result[7]
    C = result[8]
    D = result[4]
    D = [round(i, 2) for i in D]
    I = result[5]
    I = [round(i, 2) for i in I]

    print("\nInput Point: ")
    print_point()
    print("\nResult: \n")
    print('Points:')
    print("Point {} ({}, {})".format(data.index(A), A[0], A[1]))
    print("Point {} ({}, {})".format(data.index(B), B[0], B[1]))
    print("Point {} ({}, {})".format(data.index(C), C[0], C[1]))
    print("Min Angle: {} (Rad)(from point {})".format(round(result[3], 2), data.index(B)))
    print("Point I ( median )() ({}, {})".format(I[0], I[1]))
    print("Point D (Bisector) ({}, {})".format(D[0], D[1]))



    '''
    *************************
    Phần Đồ Hoạ
    *************************
    '''

    plt.figure(num=None, figsize=(8, 8), dpi=100, facecolor='w', edgecolor='k')
    for i in range(n):
        draw_point(data[i], 'b', i, k)

    if ( I == D):
        draw_point(I, 'g', 'I=D', k)
    else:
        draw_point(I, 'y', 'I', k)
        draw_point(D, 'r', 'D', k)    
    plt.axis([minn - 3, maxx + 3, minn - 3, maxx + 3])
    if (maxx * minn < 0):
        # ve Ox
        draw_line([0, minn - 2], [0, maxx + 2], 'k')
        plt.plot([maxx + 2], [0], 'k>')
        plt.text(maxx + 1, k, 'X')
        # ve Oy
        draw_line([minn - 2, 0], [maxx + 2, 0], 'k')
        plt.plot([0], [maxx + 2], 'k^')
        plt.text(k, maxx + 1, 'Y')
        # ve O
        draw_point([0, 0], 'k', "O", k)
    else:
        # ve Ox
        draw_line([minn - 1, minn - 2], [minn - 1, maxx + 2], 'k')
        plt.plot([maxx + 2], [minn - 1], 'k>')
        plt.text(maxx + 1, minn - 1 + k, "X")
        # ve Oy
        draw_line([minn - 2, minn - 1], [maxx + 2, minn - 1], 'k')
        plt.plot([minn - 1], [maxx + 2], 'k^')
        plt.text(minn - 1 + k, maxx + 1, "Y")
        # ve O
        draw_point([minn - 1, minn - 1], 'k', "O", k)
    # draw ABCDI
    plt.grid()
    draw_line(A, B, 'r')
    draw_line(B, C, 'b')
    draw_line(A, C, 'g')
    draw_line(B, I, 'y')
    draw_line(B, D, 'k')

plt.axis("scaled")
plt.show()
        
        

