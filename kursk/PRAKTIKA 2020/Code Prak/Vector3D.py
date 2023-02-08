
from math import *
from Static_Func import *
from Point3D import *

class Vector3D(Point3D):
	def __init__(self, x = 0, y = 0, z = 0):
		Point3D.__init__(self, x, y, z)
		self.length = self.findLength()
		return

	def findLength(self,):
		self.length = (self.x ** 2 + self.y ** 2 + self.z ** 2) ** 0.5
		return self.length

	def getLenght(self,):
		if self.length == None:
			self.findLength()
		return self.length

	def cosWith(self, v):
		try:
			return (self.scalarMult(v)) / (self.length * v.length)
		except:
			print('\t\t\tErr')
			return 0

	def angleWith(self, v):
		cos = self.cosWith(v)
		return acos(cos)
		

	def fromMatrix(self, M):
		mat = M.tolist()[0]
		self.x = mat[0]
		self.y = mat[1]
		self.z = mat[2]
		self.findLength()
		return

	def rotateX(self, teta):
		mat_vec = self.toMatrix()
		mat_rot = getMatrixRotateX(teta)
		mat_res = matrixMult(mat_vec, mat_rot)
		self.fromMatrix(mat_res)
		return

	def rotateY(self, teta):
		mat_vec = self.toMatrix()
		mat_rot = getMatrixRotateY(teta)
		mat_res = matrixMult(mat_vec, mat_rot)
		self.fromMatrix(mat_res)
		return

	def rotateZ(self, teta):
		mat_vec = self.toMatrix()
		mat_rot = getMatrixRotateZ(teta)
		mat_res = matrixMult(mat_vec, mat_rot)
		self.fromMatrix(mat_res)
		return

	def scalarMult(self, v):
		return self.x * v.x + self.y * v.y + self.z * v.z

	def vectorMult(self, v):
		res = Vector3D()
		res.x = self.y * v.z - self.z * v.y
		res.y = self.z * v.x - self.x * v.z
		res.z = self.x * v.y - self.y * v.x
		res.findLength()
		return res

	def numMult(self, fl = -1):
		self.x *= fl
		self.y *= fl
		self.z *= fl

	def copy(self,):
		return Vector3D(self.x, self.y, self.z)

	def getCosWith(self, v):
		return (self.scalarMult(v)) / (self.length * v.length)

	def minus(self, v):
		new = Vector3D(self.x - v.x, self.y - v.y, self.z - v.z)
