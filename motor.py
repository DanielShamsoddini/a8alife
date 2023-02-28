import numpy
import pyrosim.pyrosim as pyrosim
import pybullet as p

class MOTOR:
	def __init__(self, jname,rid, amp,freq, phofs):
		self.jointName = jname
		self.robotId = rid
		self.amplitude = amp
		self.frequency = freq
		self.phaseOffset =phofs
		self.a = 0


	def Act(self,t):
		pyrosim.Set_Motor_For_Joint(bodyIndex = self.robotId, jointName = self.jointName, controlMode = p.POSITION_CONTROL, targetPosition = t, maxForce = 40)
		self.a = self.a + 1

	def Save_Values(self):
		pass
