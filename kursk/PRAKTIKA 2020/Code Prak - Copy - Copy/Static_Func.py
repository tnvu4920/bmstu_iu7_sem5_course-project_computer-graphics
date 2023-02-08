from math import *
import numpy as np

def MatrixE():
	return np.eye(4)
	return [[	1, 	0, 	0, 	0],
			[	0, 	1, 	0, 	0],
			[	0, 	0, 	1, 	0],
			[	0,	0,	0,	1]]

def getMatrixShift(dx, dy, dz):
	return np.matrix([[	1, 	0, 	0, 	0],
			[	0, 	1, 	0, 	0],
			[	0, 	0, 	1, 	0],
			[	dx, dy, dz, 1],
			])

def getMatrixScale(kx, ky, kz, C = None):
	M = np.matrix([[	kx, 0, 	0, 	0],
			[	0, 	ky, 0, 	0],
			[	0, 	0, 	kz, 0],
			[	0, 	0, 	0, 	1],
			])
	if C == None:
		return M
	A = getMatrixShift(C.x, C.y, C.z)
	B = getMatrixShift(-C.x, -C.y, -C.z)
	return B @ M @ A

	
	N = getMatrixShift(C.x, C.y, C.z)
	Q = getMatrixShift(-C.x, -C.y, -C.z)
	A = matrixMult(Q, M)
	B = matrixMult(A, N)
	return B

def getMatrixRotateX(teta, C = None):
	M =	np.matrix([	[	1,  0, 		   0, 		  0],
			[	0,  cos(teta), sin(teta), 0],
			[	0, -sin(teta), cos(teta), 0],
			[	0,  0, 		   0, 		  1],])

	if C == None:
		return M
	N = getMatrixShift(C.x, C.y, C.z)
	Q = getMatrixShift(-C.x, -C.y, -C.z)
	return Q @ M @ N

	A = matrixMult(Q, M)
	B = matrixMult(A, N)
	return B

def getMatrixRotateY(teta, C = None):
	M =  np.matrix([	[	cos(teta), 	0, 	-sin(teta), 0],
			[	0, 			1, 	0, 			0],
			[	sin(teta), 	0, 	cos(teta), 	0],
			[	0, 			0, 	0, 			1],])
	if C == None:
		return M

	N = getMatrixShift(C.x, C.y, C.z)
	Q = getMatrixShift(-C.x, -C.y, -C.z)
	return Q @ M @ N

	A = matrixMult(Q, M)
	B = matrixMult(A, N)
	return B

	
def getMatrixRotateZ(teta, C = None):
	M =  np.matrix([	[cos(teta), sin(teta), 0, 0],
						[-sin(teta), cos(teta), 0, 0],
						[0, 0, 1, 0],
						[0, 0, 0, 1]])
	if C == None:
		return M

	N = getMatrixShift(C.x, C.y, C.z)
	Q = getMatrixShift(-C.x, -C.y, -C.z)

	return Q @ M @ N

	A = matrixMult(Q, M)
	B = matrixMult(A, N)
	return B

def getMatrixRotate(tetaX = 0, tetaY = 0, tetaZ = 0, C = None):
	MX = getMatrixRotateX(tetaX, C)
	MY = getMatrixRotateY(tetaY, C)
	MZ = getMatrixRotateZ(tetaZ, C)
	return MX @ MY @ MZ
	return matrixMult(matrixMult(MX, MY), MZ)

def getMatrixChange(teta, phi, R):
	costeta = cos(teta)
	cosphi = cos(phi)
	sinteta = sin(teta)
	sinphi = sin(phi)

	return np.matrix([[-sinteta, -costeta * sinphi, -costeta * sinphi, 0],
			[ costeta, -sinteta * cosphi, -sinteta * cosphi, 0],
			[ 0, 		cosphi, 		  -sinphi, 			 0],
			[ 0, 		0, 				   R, 				 1],
			])

def getMatrixProek(point):
	return

def matrixFrom(p):
	return [p.x, p.y, p.z, 1]

def getSize(mat):
	return [len(mat), len(mat[0])]

def matrixMult1(A, B):
	M = len(A)
	N = len(A[0])
	Q = len(B[0])
	res = [[0 for i in range(Q)] for j in range(M)]
	for i in range(M):
		for j in range(Q):
			for k in range(N):
				res[i][j] += A[i][k] * B[k][j]
			res[i][j] = res[i][j]
	return res