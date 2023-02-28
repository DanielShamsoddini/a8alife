import pybullet as p
import pyrosim.pyrosim as pyrosim
from sensor import SENSOR
from motor import MOTOR
import constants as c
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os
import math
import numpy

class ROBOT:
	def __init__(self, brainnn):
		self.robotId = p.loadURDF("body"+brainnn+".urdf")
		pyrosim.Prepare_To_Simulate(self.robotId)
		self.Prepare_To_Sense()
		self.Prepare_To_Act()
		self.nn = NEURAL_NETWORK("brain"+ brainnn+".nndf")
		#print(brainnn)
		os.system("rm brain"+brainnn+".nndf")
		self.brainval = brainnn
		self.ifHit = 0
		self.bigblock = [5,10]


	def Prepare_To_Sense(self):
		self.sensors = {}
		for linkName in pyrosim.linkNamesToIndices:
			self.sensors[linkName] = SENSOR(linkName)

	def Sense(self):
		for sensorss in self.sensors:
			self.sensors[sensorss].Get_Value()
		#print(self.sensors)
		self.isCol()

	def Prepare_To_Act(self):
		self.motors = {}
		self.amplitude = c.amplitudeB
		self.frequency = c.frequencyB
		self.offset = c.phaseOffsetB
		for jointName in pyrosim.jointNamesToIndices:
			self.motors[jointName] = MOTOR(jointName,self.robotId, self.amplitude, self.frequency, self.offset)
		#print(self.motors)

	def Act(self):
		for neuronName in self.nn.Get_Neuron_Names():
			if self.nn.Is_Motor_Neuron(neuronName):
				jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
				desiredAngle = self.nn.Get_Value_Of(neuronName)
				self.motors[jointName].Act(desiredAngle)


	def Think(self):
		self.nn.Update()

		#self.nn.Print()
	def isCol(self):
		stateOfLinkZero = p.getBasePositionAndOrientation(self.robotId)[0]
		#rint(p.getBasePositionAndOrientation(self.robotId))
		positionOfLinkZero =  stateOfLinkZero
		if round(math.dist(self.bigblock, positionOfLinkZero[0:2]), 2) == 0.0 :
			for a in range(0,100):
				print("HIT \n HIT \n HIT HIT HIT HIT\n")
				#exit()
			self.ifHit = 50
	def Get_Fitness(self):
		#stateOfLinkZero = p.getLinkState(self.robotId, pyrosim.linkNamesToIndices['Head'])
		#print(p.getBasePositionAndOrientation(self.robotId))
		stateOfLinkZero = p.getBasePositionAndOrientation(self.robotId)[0]
		#rint(p.getBasePositionAndOrientation(self.robotId))
		positionOfLinkZero =  stateOfLinkZero
		#print(positionOfLinkZero)
		#$print
		fit = positionOfLinkZero[0]
  
        #-numpy.sqrt(numpy.sum(( numpy.array(self.bigblock) - numpy.array(positionOfLinkZero[:2]))**2)) + self.ifHit
		#print(pyrosim.linkNamesToIndices)
		#fit = numpy.sqrt(numpy.sum((numpy.array(self.bigblock) - numpy.array(p.getBasePositionAndOrientation("Box4")[0]))))


		#print("finalposition:" + str(positionOfLinkZero))
		#print()
		f = open("tmp" + self.brainval +".txt", "w")
		f.write(str(fit))
		f.close()
		os.system("mv "+"tmp" + self.brainval +".txt " +"fitness" + self.brainval +".txt")
		#print(stateOfLinkZero)
		#print(positionOfLinkZero)
		#exit()
