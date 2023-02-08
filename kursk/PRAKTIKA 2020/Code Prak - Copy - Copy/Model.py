
from Point3D import *
from Color import *
from Polygon import *
from math import *
from Static_Func import *
from Vector3D import *
from Color import *
import numpy as np
from Const import *

def distance(x1, y1, x2, y2):
	return ((x1 -x2)**2 + (y1-y2)**2) ** 0.5

class Model:
	
	def __init__(self, color = RGBColor()):
		self.V = [] #Point3D
		self.P = [] # Polygons
		self.color = color
		self.polygonColor = None
		self.polygonNomal = None
		self.center = None
		self.matrixTranform = MatrixE()
		self.matrixReturn = MatrixE()
		return

	def show(self,):
		for v in self.V:
			v.show()
		for p in self.P:
			print('f ', p)

	def addMatrixTranform(self, M):
		self.matrixTranform = self.matrixTranform @ M 

	def copy(self, ):
		new = Model()
		new.V = [v.copy() for v in self.V]
		new.P = [p.copy() for p in self.P]
		new.color = self.color.copy()
		new.polygonColor =  self.polygonColor
		new.polygonNomal = self.polygonNomal
		new.matrixTranform = self.matrixTranform.copy()
		return new

	def getCenter(self, ):
		if self.center:
			return self.center
		x = [v.x for v in self.V]
		y = [v.y for v in self.V]
		z = [v.z for v in self.V]
		xAvg =int( round(sum(x) / len(x)))
		yAvg = int(round(sum(y) / len(y)))
		zAvg = int(round(sum(z) / len(z)))
		return Point3D(xAvg, yAvg, zAvg)

	def addVertex(self, v):
		self.V.append(v)
		return

	def addPolygon(self, p):
		self.P.append(p)
		return

	def createPolygon(self, V_index):
		l = len(V_index)
		if (l < 3):
			return
		if (l == 3):
			self.P.append(V_index)
			return
		if ( l > 3):
			new = []
			u = V_index[0]
			for i in range(1, l-1):
				s = V_index[i]
				v = V_index[i+1]
				new.append([u, s, v])
			self.P.extend(new)

	def findPolygonColor(self, Sun):
		self.findPolygonNomal()
		new = []
		for i in range(len(self.P)):
			new.append(self.findColor(i, Sun))
		self.polygonColor = new
			
	def findColor(self, pIndex, Sun):
		nomal = self.polygonNomal[pIndex]
		direc = Sun.direction.copy()
		cos = nomal.scalarMult(direc) / (nomal.length * direc.length)
		if (cos < 0 - 1e-4):
			return self.color.mix(black, 0.8)
		return self.color.mix(black, (1 - cos) / 2)

	def rotate(self, tetax = 0, tetay = 0, tetaz = 0, C = None):
		if C == None:
			C = self.getCenter()
		self.addMatrixTranform(getMatrixRotate(tetax, tetay, tetaz, C))

	def tranform(self,):
		M = self.matrixTranform
		for v in self.V:
			v.tranform(M)
		self.matrixReturn = self.matrixReturn @ np.linalg.inv(self.matrixTranform)
		self.matrixTranform = MatrixE()

	def reset(self,):
		self.matrixTranform = self.matrixTranform @ self.matrixReturn
		self.matrixReturn = MatrixE()

	def findPolygonNomal(self, ):
		new  = []
		for p in self.P:
			new.append(self.findNomal(p))
		self.polygonNomal = new
		return new
		
	def findNomal(self, p):
		lenn = len(p)
		a, b, c = 0, 0, 0
		V = [self.V[i] for i in p]
		V.append(self.V[0])
		vec = []
		C = self.getCenter()
		tvec = Vector3D(x = C.x - V[0].x, y = C.y - V[0].y, z = C.z - V[0].z)
		for i in range(lenn):
			x = V[i].x - V[i+1].x
			y = V[i].y - V[i+1].y
			z = V[i].z - V[i+1].z
			vec.append(Vector3D(x, y, z))
		vec.append(vec[0])
		res = vec[0].vectorMult(vec[1])
		return res

	def fromReal(self, ):
		for v in self.V:
			v.y, v.z = v.z, v.y

	def loadFrom(self, path = None):
		color = RGBColor(255, 0, 0)
		self.V = []
		self.P = []
		f = open(path, "r")
		for line in f:
			if (line == "" or line.startswith('#')):
				continue
			arr = line.split(' ')
			if arr[0] == 'v':
				v = list(map(lambda x: x, list(map(float, arr[1:4]))))
				self.V.append(Point3D(v[0], v[2], v[1]))

			if arr[0] == 'f':
				polygon = []
				for v in arr[1:]:
					w = int(v.split('/')[0].replace(',', '.'))
					polygon.append(w - 1)
				polygon.reverse()
				self.createPolygon(polygon)
		self.color = color
		


class Cube(Model):
	def __init__(self, C = Point3D(0, 0, 0), height = 50, width = 75, hight = 100, color = RGBColor()):
		Model.__init__(self, color)
		self.center = C
		p0 = Point3D(C.x - height // 2, C.y - width // 2, C.z - hight // 2)
		p1 = Point3D(C.x + height // 2, C.y - width // 2, C.z - hight // 2)
		p2 = Point3D(C.x + height // 2, C.y + width // 2, C.z - hight // 2)
		p3 = Point3D(C.x - height // 2, C.y + width // 2, C.z - hight // 2)

		p4 = Point3D(C.x - height // 2, C.y - width // 2, C.z + hight // 2)
		p5 = Point3D(C.x + height // 2, C.y - width // 2, C.z + hight // 2)
		p6 = Point3D(C.x + height // 2, C.y + width // 2, C.z + hight // 2)
		p7 = Point3D(C.x - height // 2, C.y + width // 2, C.z + hight // 2)

		self.addVertex(p0)
		self.addVertex(p1)
		self.addVertex(p2)
		self.addVertex(p3)
		self.addVertex(p4)
		self.addVertex(p5)
		self.addVertex(p6)
		self.addVertex(p7)

		self.fromReal()

		self.createPolygon([0, 1, 2, 3])
		self.createPolygon([4, 5, 6, 7])
		self.createPolygon([0, 1, 5, 4])
		self.createPolygon([1, 2, 6, 5])
		self.createPolygon([2, 3, 7, 6])
		self.createPolygon([3, 0, 4, 7])


class Chop(Model):
	def __init__(self, C = Point3D(0, 0, 0), height = 50, width = 75, hight = 100, color = RGBColor()):
		Model.__init__(self, color)
		self.center = C
		p0 = Point3D(C.x - height // 2, C.y - width // 2, C.z - hight // 2)
		p1 = Point3D(C.x + height // 2, C.y - width // 2, C.z - hight // 2)
		p2 = Point3D(C.x + height // 2, C.y + width // 2, C.z - hight // 2)
		p3 = Point3D(C.x - height // 2, C.y + width // 2, C.z - hight // 2)

		p4 = Point3D(C.x, C.y, C.z + hight // 2)


		self.addVertex(p0)
		self.addVertex(p1)
		self.addVertex(p2)
		self.addVertex(p3)
		self.addVertex(p4)

		self.fromReal()

		self.createPolygon([0, 1, 4])
		self.createPolygon([0, 1, 2, 3])
		self.createPolygon([1, 2, 4])
		self.createPolygon([2, 3, 4])
		self.createPolygon([3, 0, 4])


class Ground(Model):
	def __init__(self, C = None, height = 0, width = 0, color = RGBColor()):
		Model.__init__(self, color)
		if (C == None):
			C = Point3D(0, 0, 0)
		p0 = Point3D(C.x - height //2, C.y - width // 2, C.z)
		p1 = Point3D(C.x + height //2, C.y - width // 2, C.z)
		p2 = Point3D(C.x + height // 2, C.y + width // 2, C.z)
		p3 = Point3D(C.x - height // 2, C.y + width // 2, C.z)
		self.center = C 
		self.V = [p0, p1, p2, p3]
		self.fromReal()

		self.createPolygon([0, 1, 2])
		self.createPolygon([0, 2, 3])




		










