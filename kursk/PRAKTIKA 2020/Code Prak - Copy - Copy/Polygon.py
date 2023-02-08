'''
from Vector3D import *
from Point3D import *
from Color import *

class Polygon:
	def __init__(self, vertex_arr = [], vec_normal = None, color = RGBColor()):
		
		self.normal = Vector3D()
		self.V = vertex_arr
		self.V_num = len(self.V)
		self.color = color
		return

	def show(self,):
		print("Polygon: ")
		for i in self.V:
			i.show()

	def copy(self, ):
		new = Polygon([], None, self.color.copy())
		new.V = [v.copy() for v in self.V]
		return new


	def getNormal(self, ):
		return Vector3D()

	def setColor(self, newColor):
		self.color = newColor
		return

	def addVertex(self, v):
		self.V.append(v)
		self.V_num += 1
		return
		
	def split(self,):
		P_arr = []
		if self.V_num == 3:
			return [self, ]
		else:
			u = self.V[0]
			for i in range(1, self.V_num - 1):
				P_arr.append(Polygon([u.copy(), self.V[i].copy(), self.V[i+1].copy()], self.normal,))
		return P_arr

	def rotate(self, tetax = 0, tetay = 0, tetaz = 0, C = None):
		if C == None:
			return
		for p in self.V:
			p.rotate(tetax, tetay, tetaz, C)
	
	def tranform(self, matrix):
		new_Polygon = Polygon(vertex_arr = [], color = self.color)
		new_Polygon.V = [v.tranform(matrix) for v in self.V]
		return
'''			