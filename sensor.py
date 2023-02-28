import numpy
import pyrosim.pyrosim as pyrosim
class SENSOR:
	def __init__(self, nme):
		self.values = numpy.zeros(10000)
		self.linkName = nme
		self.a = 0
		
	def Get_Value(self):
		self.values[self.a] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)
		self.a = self.a + 1

	def Save_Values(self):
		pass

	
