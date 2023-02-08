import sys
import numpy as np
import matplotlib.pyplot as plt
from math import *
EPS = 10e-7
def f(x):
 return sin(x) + 2*cos(x)
class Point:
 def __init__(self, x, y, p):
 self.x = x;
 self.y = y;
 self.p = p; #the weight of the point(x, y)
 def setP(self, newP):
 self.p = newP
def initPoints(num):
 start = 0
 stop = 5
 points = []
 for x in np.linspace(start, stop, num):
 points.append(Point(x, f(x), 1))
 return points
def printTable(points):
 print("ID X Y P")
 iter = 1
 for p in points:
 print('{:2}'.format(iter), end='')
 iter += 1
 print('{:8.3f}'.format(p.x), end='')
 print('{:8.3f}'.format(p.y), end='')
 print('{:8.3f}'.format(p.p), end='')
 print()
#System of linear equations is represented as a matrix of coefficients
def initCoeffMatrix(points, deg):
 num = len(points)
 matrix = [[0 for j in range(deg+2)] for i in range(deg+1)] # matrix[deg+1]*[deg+2]
 for i in range(deg+1):
 for j in range(deg+2):
 coeff = 0
 for k in range(num):
 coeff += points[k].p * points[k].x ** (i+j)
 matrix[i][j] = coeff
 augmentedCoeff = 0
 for k in range(num):
 augmentedCoeff += points[k].p * points[k].y * points[k].x ** i
 matrix[i][deg+1] = augmentedCoeff
 return matrix
#Using Gaussian elimination method
#matrix n * (n + 1)
def solve(matrix):
 n = len(matrix)
 res = [0 for i in range(n)]
 #row swapping to shape a "loose" row echelon form
 #the pivot of a non zero row is to the right OR UNDER the pivot of the row above it
 for i in range(n-1):
 for j in range(i+1, n):
 if abs(matrix[i][i]) < abs(matrix[j][i]):
 tmp = matrix[i]
 matrix[i] = matrix[j]
 matrix[j] = tmp
 #performing Gaussian elimination
 #matrix is shaped into the "strict" row echelon form
 for i in range(n-1):
 for j in range(i+1, n):
 if abs(matrix[i][i]) < EPS:
 return res, False
 scalar = matrix[j][i] / matrix[i][i]
 for k in range(n+1):
 matrix[j][k] -= scalar * matrix[i][k]
 print(matrix[n-1])
 #Backward substitutions
 for i in range(n-1, -1, -1):
 res[i] = matrix[i][n]
 for j in range(i+1, n):
 res[i] -= matrix[i][j] * res[j]
 res[i] /= matrix[i][i]

 print(res)
 return res, True
def phi(res, x):
 val = 0
 for i in range(len(res)):
 val += res[i] * (x ** i)
 return val
def plotData(points):
 x = [p.x for p in points]
 y = [p.y for p in points]
 plt.plot(x, y, "ko", label="data")
 plt.ylabel('y')
 plt.xlabel('x')
def plotApproximationFunc(points, res, deg, mode=0):
 x = np.linspace(points[0].x, points[len(points) - 1].x, 100)
 y = [phi(res, i) for i in x]
 #the degree of the polynomial is recommended <= 6
 fmt1 = ["-b", "--g", "-.r", ":c", "-m", "--y", "-.b"]
 fmt2 = ["-g", "--r", "-.c", ":m", "-y", "--b", "-.g"]
 if mode == 0:
 plt.plot(x, y, fmt1[deg%7], label="n={:d}".format(deg))
 elif mode == 1:
 plt.plot(x, y, fmt1[deg%7], label="n={:d}".format(deg) + " original")
 elif mode == 2:
 plt.plot(x, y, fmt2[deg%7], label="n={:d}".format(deg) + " modified")
def initTable():
 num = int(input("Input the number of points : "))
 #Init points
 points = initPoints(num)
 printTable(points)
 return points
def modifyTable(points):
 num = len(points)
 while True:
 print("Please choose an option")
 print("0 - I'm fine with the current table")
 print("1 - Changing a weight value")
 option = int(input())
 if option == 0 :
 break;
 elif option == 1 :
 id = int(input("Input the id of the point you want to change : "))
 new_p = float(input("Input the new weight value : "))
 if 1 <= id <= num :
 points[id-1].setP(new_p)
 print("Success!")
 else :
 print("Failed!")
 print("The final table ")
 printTable(points)
 return points
def approximationProcess(points, mode = 0):
 degreeOfPolynomial = int(input("Input the degree of the polynomial : "))
 if degreeOfPolynomial < 0:
 print("The degree of the polynomial must be non negative")
 return False
 if degreeOfPolynomial > len(points):
 printf("The degree of the polynomial <= the number of points")
 return False
 matrix = initCoeffMatrix(points, degreeOfPolynomial)
 res, status = solve(matrix)
 if not status:
 print("The solution of SOLE is not unique!")
 return False
 plotApproximationFunc(points, res, degreeOfPolynomial, mode)
 return True
def process1():
 points = initTable()
 points = modifyTable(points)
 plotData(points)
 approximationProcess(points)
 plt.legend()
 plt.show()
def process2():
 points = initTable()
 plotData(points)
 while approximationProcess(points):
 print("Input -1 if you want to stop")
 plt.legend()
 plt.show()
def process3():
 points = initTable()
 plotData(points)
 approximationProcess(points, mode = 1)
 points = modifyTable(points)
 approximationProcess(points, mode = 2)
 plt.legend()
 plt.show()
if __name__ == "__main__":
 process1()
