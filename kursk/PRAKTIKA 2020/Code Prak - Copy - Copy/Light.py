
from math import *
from Vector3D import *

class Light:

	def __init__(self, pos = Vector3D(-cos(-pi / 8), -1, sin(-pi / 8))):
		self.direction = pos
		vec = Vector3D(pos.x, pos.y, pos.z)
		vecOxz = Vector3D(vec.x, 0, vec.z)
		Ox = Vector3D(1, 0, 0)
		self.beta = Ox.angleWith(vecOxz)
		self.alpha = vec.angleWith(vecOxz)

		
