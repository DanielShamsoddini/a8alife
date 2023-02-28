import pybullet as p

class WORLD:
	def __init__(self,worldnum):
		p.loadSDF("world"+worldnum+".sdf")
		self.planeId = p.loadURDF("plane.urdf")
