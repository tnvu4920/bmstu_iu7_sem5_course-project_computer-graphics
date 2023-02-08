'''
import numpy as np
from math import pi, sin, cos, fabs
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem, QMessageBox
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter, QTransform
from PyQt5.QtCore import Qt, QTime, QCoreApplication, QEventLoop, QPointF, QPoint
from math import *

from Point3D import *
from Light import *
from Color import *
from Static_Func import *

size = {'width': 700, 'height':700 }
groundSize = {'width': 700, 'height':700 }
skyBlue = RGBColor(0, 127, 255)
black = RGBColor(0, 0, 0)
zBack = -10000
centerSun = Point3D(size['width'] // 2, 0, size['height'] // 2)
center = Point3D(size['width'] // 2, 0, size['height'])
eps = 5
goc_quay = pi / 5



class Zbuffer:
	def __init__(self, size = None):
		self.x = 1
		self.size = size
		if self.size == None:
			self.size = {'width': 700, 'height':700 }
		self.teta = pi / 4
		
	def Zbuffer(self, Model_Arr):
		size = self.size
		img = QImage(size['width'], size['height'], QImage.Format_RGB32)
		imgSun = QImage(size['width'], size['height'], QImage.Format_RGB32)
		sun = Light()

		img.fill(skyBlue)
		imgSun.fill(skyBlue)
		# Tạo Buffer
		buf = [[zBack for i in range(size['width'])] for j in range(size['height'])]
		bufSun = [[zBack for i in range(size['width'])] for j in range(size['height'])]

		for i in range(0, len(Model_Arr)):
			# khu mặt khuất
			model = Model_Arr[i]
			modelSun = model.copy()
			model.addMatrixTranform(getMatrixRotateX(goc_quay, center))
			model.tranform()

			modelSun.addMatrixTranform(getMatrixRotateY(pi / 2, centerSun))
			modelSun.addMatrixTranform(getMatrixRotateX(self.teta, center))
			#modelSun.addMatrixTranform(getMatrixRotateY(self.teta, center))
			modelSun.tranform()
			img, buf = self.processZbuf(buf, model, img)
			imgSun, bufSun = self.processZbuf(bufSun, modelSun, imgSun)
		
		#img = self.addShadow(sun, buf, bufSun, img)
		return img

	def processZbuf(self, buf, model, img):
		size = {'width': len(buf), 'height':len(buf[0]) }
		V = model.V
		for p in model.P:
			color = model.color#RGBColor()#polygon.color
			point_Arr = self.PointZBuf([V[p[0]], V[p[1]], V[p[2]]])
			# 
			for p in point_Arr:
				if (0 < p.x and p.x < size['width'] and 0 < p.y and p.y < size['height'] ):
					try:
						if p.z > buf[p.x][p.y]:
							buf[p.x][p.y] = p.z
							img.setPixelColor(p.x, self.size['height'] - p.y, color)
					except:
						print("Err: processZbuf")
						return img, buf
		return img, buf

	def addShadow(self, sun = None, buf = None, bufSun = None, img = None):
		size = self.size
		tetax = sun.tetax
		tetay = sun.tetay
		tetaz = sun.tetaz
		red = RGBColor(255, 0, 0)
		i = 0
		
		A1 = getMatrixRotateX(-goc_quay, center) # khôi phục lại ban đầu
		A2 = getMatrixRotateY(pi / 2, centerSun) # Quay 90 độ
		A3 = getMatrixRotateX(self.teta, center) # Quay Hướng mặt trời
		A4 = matrixMult(A1, A2)
		M = matrixMult(A4, A3)
		
		for x in range(size['width']):
			for y in range(size['height']):
				z = buf[x][y]
				if z > zBack:
					pointSun = Point3D(x, y, z)
					pointSun.tranform(M)
					if (pointSun.x > 0 and pointSun.x < size['width'] and pointSun.y > 0 and pointSun.y < size['height']):
						if (abs(pointSun.z  - bufSun[pointSun.x][pointSun.y]) > eps):# không nhìn thây từ mặt trời
							img.setPixelColor(x, self.size['height'] - y, black.mix(img.pixelColor(x, self.size['height'] - y), 0.8))
					
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
'''