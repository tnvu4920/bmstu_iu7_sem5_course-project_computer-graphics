
from random import randint
from PyQt5.QtGui import QColor

class RGBColor(QColor):

	def __init__(self, red = None, green = None, blue = None):
		if (red == None or green == None or blue == None):
			QColor.__init__(self, randint(0, 255), randint(0, 255), randint(0, 255))
		else:
			QColor.__init__(self, red, green, blue)

	def show(self, ):
		print("Color [{}, {}, {}]".format(self.red(), self.green(), self.blue()))

	def copy(self, ):
		return RGBColor(self.red(), self.green(), self.blue())

	def mix(self, color = None, a = 0.5):
		red = int(self.red() * (1 - a) + color.red() * a)
		green = int(self.green() * (1 - a) + color.green() * a)
		blue = int(self.blue() * (1 - a) + color.blue() * a)
		return RGBColor(red, green, blue)
		