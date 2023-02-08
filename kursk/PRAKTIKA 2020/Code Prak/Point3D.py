
from Static_Func import *

class Point3D:
	def __init__(self, x = 0, y = 0, z = 0):
		self.x = x
		self.y = y
		self.z = z
		return

	def show(self,):
		print('Point ShowL ', self.toMatrix())

	def copy(self, ):
		return Point3D(self.x, self.y, self.z)

	def toMatrix(self,):
		return np.matrix([[self.x, self.y, self.z, 1],])

	def fromMatrix(self, M):
		mat = M.tolist()[0]
		self.x = mat[0]
		self.y = mat[1]
		self.z = mat[2]
		return self

	def convertY(self, ):
		self.y = -self.y

	'''
	def shift(self, dx = 0, dy = 0, dz = 0):
		self.x += dx
		self.y += dy
		self.z += dz 
		return

	def scale(self, kx, ky, kz, C = None):
		if C == None:
			C = Point3D(0, 0, 0)
		mat_rot = getMatrixScale(teta, C)

		mat_vec = self.toMatrix()
		mat_res = matrixMult(mat_vec, mat_rot)
		self.fromMatrix(mat_res)
		return

	def rotateX(self, teta,  C = None):
		if C == None:
			C = Point3D(0, 0, 0)
		dx, dy, dz = C.x, C.y, C.z
		mat_vec = self.toMatrix()
		mat_tran = getMatrixRotateX(teta, C)
		mat_vec = matrixMult(mat_vec, mat_tran)
		self.fromMatrix(mat_vec)
		return

	def rotateY(self, teta, C = None):
		if C == None:
			C = Point3D(0, 0, 0)
		dx, dy, dz = C.x, C.y, C.z
		mat_vec = self.toMatrix()
		mat_tran = getMatrixRotateY(teta, C)
		mat_vec = matrixMult(mat_vec, mat_tran)
		self.fromMatrix(mat_vec)
		return

	def rotateZ(self, teta, C = None):
		if C == None:
			C = Point3D(0, 0, 0)
		dx, dy, dz = C.x, C.y, C.z
		mat_vec = self.toMatrix()
		mat_tran = getMatrixRotateZ(teta, C)

		mat_vec = matrixMult(mat_vec, mat_tran)
		self.fromMatrix(mat_vec)
		return

	def rotate(self, tetaX = 0, tetaY = 0, tetaZ = 0, C = None):
		if C == None:
			C = Point3D(0, 0, 0)
		if (tetaX != 0):
			self.rotateX(tetaX, C)
		if (tetaY != 0):
			self.rotateY(tetaY, C)
		if (tetaZ != 0):
			self.rotateZ(tetaZ, C)
		return
		'''

	def tranform(self, matrix = None):
		#if (matrix == None):
		#	return

		A = self.toMatrix()
		res = A @ matrix
		return self.fromMatrix(res)





