
from PyQt5.QtGui import QPixmap, QImage
import math

from Point3D import *
from Model import *
from Color import *
from ZBuffer import *
from Static_Func import *
from Const import *
from Light import *

class MyScene:
	def __init__(self, size  = {'width': 600, 'height':600 }):
		self.M = [] #Model[]
		self.staticModel = []
		self.dinamicModel = []
		self.size = size
		self.goc_quay = pi / 5
		self.staticBuf = None
		self.staticImg = None
		self.staticBufSun = None
		self.staticImgSun = None
		self.sunTranform = MatrixE()
		self.image = None
		self.buf = None
		self.updateZBuf = False
		self.sun = Light()
		self.updateStatic = True
		self.updateDinamic = True
		self.carPositionZ = 320
		self.carSpeed = 0
		self.carDirec = 1
		self.matrixTranform = getMatrixRotateX(self.goc_quay, center)
		self.groundLight = False
		self.updateSun = False
		self.withSadow = False

	def show(self, ):

		if (self.withSadow and self.staticBufSun == None):
			self.updateSun = True

		if self.updateSun:
			self.groundLight = True

		#if (self.updateDinamic):
		#	self.withSadow = False

		if (self.updateDinamic):
			for model in self.dinamicModel:
				model.addMatrixTranform(getMatrixShift(0, 0, self.carSpeed * self.carDirec))	

		# Ánh Sánh Xung Quanh
		# Khong Quay Hinh
		# Phu Thuoc Vao Vi tri mat troi
		if (not self.groundLight or self.updateSun):
			self.addGroundLight()
			self.groundLight = True
			self.updateStatic = True
		# Sun Buffer
		# Đưa về trạng thái ban đầu
		if (self.updateSun and self.withSadow):
			self.staticImgSun, self.staticBufSun = self.getBufSun(self.staticModel, None, None)
		
		# Zbuffer
		
		if self.updateStatic:
			self.staticImg, self.staticBuf =  self.getBufImg(self.staticModel, None, None) # Khong Quay Hinh

		# get dinamic:
		img = [ i.copy() for i in self.staticImg]
		buf = [i.copy() for i in self.staticBuf]
		if (self.staticImgSun == None):
			imgSun = None
		else:
			imgSun = [i.copy() for i in self.staticImgSun]
		if (self.staticBufSun == None):
			bufSun = None
		else:
			bufSun = [i.copy() for i in self.staticBufSun]

		if (self.updateStatic == True):
			self.updateDinamic = True
		# Zbuffer Dinamic
		if (self.updateDinamic or 1):
			img, buf = self.getBufImg(self.dinamicModel, img, buf)

		if self.withSadow and (self.updateDinamic or self.updateSun):
			imgSun, bufSun = self.getBufSun(self.dinamicModel, imgSun, bufSun)
		
		if (self.withSadow):
			print("Update shdoww")
			img = self.addShadow(buf, bufSun, img)

		#self.updateDinamic = False
		self.updateStatic = False
		self.updateSun = False

		image = self.toImg(img)
		return image

	def addGroundLight(self,):
		M = self.sunTranform
		print(M)
		M1 = np.linalg.inv(M)
		for model in self.M:
			#model.addMatrixTranform(M)
			model.tranform()
			model.findPolygonColor(self.sun)
			#model.addMatrixTranform(M1)
			#model.tranform()


	def getMatrixTranformSun(self,):
		if (self.sun.direction.z > 0):
			X = getMatrixRotateY(pi / 2 + self.sun.beta, centerSun)
		else:
			X = getMatrixRotateY(pi / 2 - self.sun.beta, centerSun)

		if (self.sun.direction.x > 0):
			Y = getMatrixRotateX(self.sun.alpha, centerSun)
		else:
			Y = getMatrixRotateX(self.sun.alpha, centerSun)
		
		M = X @ Y
		return M

	def toImg(self, img_matrix):
		size = self.size#{'width': len(img_matrix[0]), 'height': len(img_matrix) }
		image = QImage(size['width'], size['height'], QImage.Format_RGB32)
		for x in range(size['width']):
			for y in range(size['height']):
				color = img_matrix[x][y]
				if (color == None):
					color = skyBlue
				image.setPixelColor(x, y, color)
		return image

	def getBufImg(self,Model_Arr = None, img = None, buf = None):
		if (Model_Arr == None):
			return
		size = self.size
		if (img == None):
			img = [[None for i in range(size['height'])] for j in range(size['width'])]
		if buf == None:
			buf = [[zBack for i in range(size['height'])] for j in range(size['width'])]
		

		M = self.matrixTranform 
		M1 = np.linalg.inv(M)

		for model in Model_Arr:
			model.addMatrixTranform(M)
			model.tranform()
			img, buf = self.processZbuf(model, buf, img)
			model.addMatrixTranform(M1)

		return img, buf

	def getBufSun(self,Model_Arr = [], imgSun = None, bufSun = None):
		if (Model_Arr == None):
			return
		size = self.size

		if (imgSun == None):
			imgSun = [[None for i in range(size['height'] * 2)] for j in range(size['width'] * 2)]

		if (bufSun == None):
			bufSun = [[zBack for i in range(size['height'] * 2)] for j in range(size['width'] * 2)]
		
		M =  self.getMatrixTranformSun()
		M1 = np.linalg.inv(M)

		for modelSun in Model_Arr:
			# đưa về trạng thái ban đầu
			modelSun.addMatrixTranform(M)
			modelSun.tranform()
			imgSun, bufSun = self.processZbuf(modelSun, bufSun, imgSun, 1)
			modelSun.addMatrixTranform(M1)

		return imgSun, bufSun

	def addModel(self, model):
		self.staticModel.append(model)
		self.M.append(model)

	def addDinamicModel(self, model):
		self.dinamicModel.append(model)
		self.M.append(model)

	def createTree(self, x, y, width = 20, height = 20, hight = 250, dinamic = False):
		z1 = int(hight * 0.3)
		z2 = hight - z1
		if (dinamic):
			addFunc = self.addDinamicModel
		else:
			addFunc = self.addModel

		# Than Cay
		p1 = Point3D(x, y, z1 // 2)
		t1 = Cube(p1, width, height, z1, brown.copy())
		addFunc(t1)

		#Ngon
		w = width * 4
		h = height * 4
		z = z2 # Chieu cao cua mot tan la

		top1 = 4 * z / 6
		top2 = 5 * z / 6
		top3 = z
		h1 = 4 * z / 6
		h2 = 3 * z / 6
		h3 = 2.5 * z / 6

		p2 = Point3D(x, y, z1 + top1 - h1 / 2)
		t2 = Chop(p2, w, h, h1, forestgreen.copy())
		addFunc(t2)

		p3 = Point3D(x, y, z1 + top2 - h2 / 2)
		t3 = Chop(p3, w / 1.3, h / 1.3,  h2, forestgreen.copy())
		addFunc(t3)

		p4 = Point3D(x, y, z1 + top3 - h3 / 2)
		t4 = Chop(p4, w / 1.6, h / 1.6, h3, forestgreen.copy())
		addFunc(t4)

	def createGround(self, ):
		size = self.size
		ground = Ground(Point3D(size['width'] // 2, size['height'] // 2, 0), size['width'], size['height'],  ground_color.copy())
		self.addModel(ground)

	def createHouse(self, x, y, width = 100, height = 150, hight = 150):
		z1 = int(hight * 0.5)
		z2 = hight - z1
		# Phan than:

		p1 = Point3D(x, y, z1 // 2)
		t1 = Cube(p1, width, height, z1, RGBColor())
		#Mai
		p2 = Point3D(x, y, z1 + z2 // 2)
		t2 = Chop(p2, int(width * 1.2), int(height * 1.2), z2, RGBColor())
		self.addModel(t1)
		self.addModel(t2)

	def createCar(self, x, y):

		M = Model()
		M.loadFrom('car2.obj')
		M.fromReal()
		M.addMatrixTranform(getMatrixScale(0.5, 0.5, 0.5))

		M.addMatrixTranform(getMatrixShift(300, 30, 200))
		self.addDinamicModel(M)

	def default(self,):
		self.createGround()
		
		# Vung I
		
		self.createHouse(x = 150, y = 100, width = 100, height = 150, hight = 150)
		self.createHouse(x = 100, y = 300, width = 75, height = 150, hight = 200)
		
		self.createTree(x = 50, y = 200, width = 20, height = 20, hight = 250)
		
		self.createTree(x = 100, y = 450, width = 15, height = 15, hight = 150)
		self.createTree(x = 75, y = 525, width = 15, height = 15, hight = 225)
		self.createTree(x = 150, y = 550, width = 15, height = 15, hight = 250)
		
		
		#Vung II
		#self.createTree(x = 350, y = 350, width = 15, height = 15, hight = 150, dinamic = True)
		self.createCar(x = 350, y = 350)

		#Vung III
		
		self.createTree(x = 550, y = 100, width = 15, height = 15, hight = 175)
		self.createTree(x = 550, y = 150, width = 15, height = 15, hight = 225)
		self.createTree(x = 500, y = 215, width = 15, height = 15, hight = 180)
		self.createTree(x = 580, y = 250, width = 15, height = 15, hight = 200)
		
		
		self.createHouse(x = 550, y = 400, width = 100, height = 150, hight = 250)
		self.createTree(x = 500, y = 550, width = 15, height = 15, hight = 200)
		self.createTree(x = 575, y = 400, width = 15, height = 15, hight = 180)
		
			
	def processZbuf(self, model, buf, img = None, fl = 0):
		size = {'width': len(buf), 'height':len(buf[0]) }
		V = model.V
		color_arr = model.polygonColor
		for i in range(len(model.P)):
		#for p in model.P:
			#color = model.color#RGBColor()#polygon.color
			color = color_arr[i]
			p = model.P[i]
			point_Arr = self.PointZBuf([V[p[0]], V[p[1]], V[p[2]]])
			# 
			for p in point_Arr:
				if (0 < p.x and p.x < size['width'] and 0 < p.y and p.y < size['height'] ) or fl:
					if p.z > buf[p.x][p.y]:
						buf[p.x][p.y] = p.z
						if (img != None):
							img[p.x][self.size['height'] - p.y] = color

		return img, buf

	def addShadow(self, buf = None, bufSun = None, img = None):
		size = self.size
		red = RGBColor(255, 0, 0)
		i = 0
		
		Mreset  = np.linalg.inv(self.matrixTranform)
		M = Mreset @ self.getMatrixTranformSun()
		
		for x in range(size['width']):
			for y in range(size['height']):
				z = buf[x][y]
				if z > zBack:
					pointSun = Point3D(x, y, z)
					pointSun.tranform(M)
					if (pointSun.x > 0 and pointSun.x < size['width'] and pointSun.y > 0 and pointSun.y < size['height']) or 1:
						if (abs(pointSun.z  - bufSun[int(round(pointSun.x))][int(round(pointSun.y))]) > eps):# không nhìn thây từ mặt trời
							#img.setPixelColor(x, self.size['height'] - y, black.mix(img.pixelColor(x, self.size['height'] - y), 0.8))
							img[x][self.size['height'] - y] = black.mix(img[x][self.size['height'] - y], 0.8)
		return img				
	
	def setImage(self, img, x, y, color):
		new_x = x
		new_y = self.size['height'] - y
		img.setPixelColor(x, self.size['height'] - y, color)
		return img
			
	def PointZBuf(self, triangle = None):
		V = triangle

		x = [p.x for p in V]
		y = [p.y for p in V]
		z = [p.z for p in V]
		point_Arr = []

		if triangle == None:
			return point_Arr
		yMax = int(max(y))
		yMin = int(min(y))

		x1, x2 = 0, 0
		z1, z2 = 0, 0

		for y_now in range(yMin, yMax + 1):
			fl = 1
			for n in range(3):
				if n == 2:
					n1 = 0
				else:
					n1 = n+1
				if y_now >= max(y[n], y[n1]) or y_now < min(y[n], y[n1]):
					continue
				m = (y[n] - y_now) / (y[n] - y[n1])
				if fl == 1:
					x2 = x[n] + m * (x[n1] - x[n])
					z2 = z[n] + m * (z[n1] - z[n])
					fl = 0
				else:
					x1 = x[n] + m * (x[n1] - x[n])
					z1 = z[n] + m * (z[n1] - z[n])



			if (x2 < x1):
				x1, x2 = x2, x1
				z1, z2 = z2, z1
			
			xstart = int(round(x1))
			xend = int(round(x2))
			delX = xend  - xstart
			delZ = z2 - z1

			for x_now in range(xstart, xend, 1):
				m = (x_now - xstart) / delX
				z_now = int(round(z1 + m * delZ))
				point_Arr.append(Point3D(x_now, y_now, z_now))
		
		return point_Arr
	
	def reset(self,):
		for model in self.M:
			model.reset()
		self.matrixReturn = MatrixE()

	'''
	def tranform(self,):
		for model in self.M:
			model.addMatrixTranform(self.matrixTranform)
			model.tranform()
		self.matrixTranform = MatrixE()
	'''
	def addTranform(self, M):
		self.matrixTranform = self.matrixTranform @ M