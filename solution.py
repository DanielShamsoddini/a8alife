import numpy
import pyrosim.pyrosim as pyrosim
import os
import random
import time
import constants as c
import pybullet as p
import pybullet_data


class SOLUTION:
	def __init__(self, nextav):
		if c.randomSeed != None:
			random.seed(c.randomSeed)
		self.myID = nextav
		self.a = numpy.zeros((c.numSensorNeurons, c.numMotorNeurons))
		self.randlength = random.randint(8,c.randlen-1)
		self.weights = 2*numpy.random.rand(4*self.randlength, 4*self.randlength) - 1
		#self.sensorrandom = [random.randint(0, 5) for a in range(self.randlength+1)]
		self.blocks = [[self.randsize(), random.choice(("Green", "Blue")), self.randomdirgenerator()] for a in range(self.randlength*4)]
		self.jointnames = []
		self.cubename = []

	def Create_World(self):
		pyrosim.Start_SDF("world"+str(self.myID)+".sdf")
		l = 1
		w = 1
		h = 1
		# pyrosim.Send_Cube(name="Box", pos = [5,5,1.5], size = [l,w,h])
		# pyrosim.Send_Cube(name="Box2", pos = [10,15,1.5], size = [l,w,h])
		# pyrosim.Send_Cube(name="Box3", pos = [10,5,1.5], size = [l,w,h])
		# #pyrosim.Send_Cube(name="Box4", pos = [2,4,5.5], size = [1.5*l,1.5*w,5*h])
		# pyrosim.Send_Cube(name="Bo5", pos = [20,20,1.5], size = [l,w,h])
		pyrosim.End()

	def poscalculator(self, currentIndex, blocksize = [0,0,0]):
		if blocksize is [0,0,0]:
			return [0,0,1]
		else:
			return [0, blocksize[1], blocksize[2]/2]
		
	
	def randsize(self):
		return [random.uniform(c.minsize, c.maxsize), random.uniform(c.minsize, c.maxsize), random.uniform(c.minsize, c.maxsize)]

	def dirgetter(self, a, b, connect_choice):
		if connect_choice == "up":
			xyz = [0, 0, (self.blocks[a][0][2] + self.blocks[b][0][2])/2.0]
		elif connect_choice == "down":
			xyz = [0, 0, -1 * (self.blocks[a][0][2] + self.blocks[b][0][2])/2.0]
		elif connect_choice == "west":
			xyz = [(self.blocks[a][0][0] + self.blocks[b][0][0])/2.0, 0, 0]
		elif connect_choice == "east":
			xyz = [-1*(self.blocks[a][0][0] + self.blocks[b][0][0])/2.0, 0, 0]
		elif connect_choice == "north":
			xyz = [0, (self.blocks[a][0][1] + self.blocks[b][0][1])/2.0, 0]
		elif connect_choice == "south":
			xyz = [0, -1* (self.blocks[a][0][1] + self.blocks[b][0][1])/2.0, 0]

		return xyz


	def randomdirgenerator(self):
		num_connects = random.randint(2,4)
		connect_types =["up", "down", "west", "east", "north", "south"]
		random.shuffle(connect_types)
		for ccc in range(5-num_connects):
			connect_types.pop()

		return connect_types

	def Create_Body(self):
		pyrosim.Start_URDF("body"+str(self.myID)+".urdf")
		self.jointnames = []
		self.cubename = []
		self.absoluteposandsize = []
		l = 0.1
		w = 0.4
		h = 0.1
		#pyrosim.Send_Cube(name = "Box4", pos = [5,10,5], size = [1,1,5])
		
		pyrosim.Send_Cube(name = "Box0", pos = [0,0,1], size = self.blocks[0][0], color = self.blocks[0][1])

		# block has 6 faces, we need something that can potentially add to all 6,
		# strategy: forward and backwards randomize, then generate random chance to each
		# make sure! to prevent overlaps, store locations of each block as you add them

		#print(self.randlength)
		numblocks = 1
		a = 1
		
		parentgen = [("Box0",0)]
		parentgen2 = []
		self.cubename.append(("Box0", self.blocks[0][1]))
		self.absoluteposandsize.append((numpy.array([0,0,1]), numpy.array(self.blocks[0][0])))
		while numblocks < self.randlength and len(parentgen) > 0:
			for a in parentgen:
				#print(a)
				connect_types = self.blocks[a[1]][2]
				if len(connect_types) + numblocks >= self.randlength:
					connect_types = connect_types[:(self.randlength-numblocks)]
				for xyz in range(len(connect_types)):
					if self.doesnotoverlap(self.addArrSizes(a[1],self.dirgetter(a[1],numblocks, connect_types[xyz])), self.blocks[numblocks][0]):
						pyrosim.Send_Joint(name = a[0] +"_"+a[0]+str(xyz), parent = a[0] , child = a[0]+str(xyz), type = "revolute", position = self.dirgetter(a[1],numblocks, connect_types[xyz]), jointAxis = "0 0 1")
						pyrosim.Send_Cube(name = a[0]+str(xyz), pos = [0,0,1], size = self.blocks[numblocks][0], color = self.blocks[numblocks][1])
						parentgen2.append((a[0]+str(xyz),numblocks))
						self.jointnames.append(a[0] +"_"+a[0]+str(xyz))
						self.cubename.append((a[0]+str(xyz), self.blocks[numblocks][1]))
						self.absoluteposandsize.append((self.addArrSizes(a[1],self.dirgetter(a[1],numblocks, connect_types[xyz])),self.blocks[numblocks][0]))
						numblocks += 1
			parentgen = parentgen2
			parentgen2 = []
		
#		print(self.cubename)
#		print(self.jointnames)
		pyrosim.End()
			
	def addArrSizes(self, parentindex, jointloc):
		x = [0,0,0]
		y = [0,0,1]
		for a in range(0,3):
			x[a] += self.absoluteposandsize[parentindex][0][a] + jointloc[a] + y[a]
		return x

	def doesnotoverlap(self, jointpositionblocktobeadded, sizeblocktobeadded):
		
		for a in self.absoluteposandsize:
			counter = 0
			for b in range(0,3):
				distancecenters = abs(a[0][b]- jointpositionblocktobeadded[b])
				if distancecenters - (sizeblocktobeadded[b]/2.0) - (a[1][b]/2.0) < -0.05:
					counter+= 1
			
			if counter >2:
				return False
		return True

		# while numblocks < self.randlength:
		# 	num_num = 5
		# 	if self.randlength - a < 5:
		# 		num_num = 5 - (self.randlength - a) 
		# 	num_connects = random.randint(1,num_num) -1
		# 	connect_types = ["up", "down", "west", "east", "north", "south"]
		# 	pyrosim.Send_Cube(name = "Box"+str(a+numblocks), pos = [0,0,1], size = self.blocks[a+numblocks][0], color = self.blocks[a+numblocks][1])
		# 	numblocks+=1
		# 	for b in range(1,num_connects):
		# 		print(str(a-1) + "\n")
		# 		print(str(a+b) + "\n")
		# 		print(str(num_connects)+"\n")
		# 		print("randlen" + str(self.randlength))
		# 		connect_choice = random.choice(connect_types)
		# 		connect_types.remove(connect_choice)
		# 		
		# 		pyrosim.Send_Joint(name = "Box"+str(a-1)+"_Box"+str(a+b), parent = "Box"+str(a-1) , child = "Box"+str(a+b), type = "revolute", position = xyz, jointAxis = "0 0 1")
		# 		print("Box"+str(a-1)+"_Box"+str(a+b) + "\n")
		# 		pyrosim.Send_Cube(name = "Box"+str(a+numblocks), pos = [0,0,1], size = self.blocks[a+numblocks][0], color = self.blocks[a+b][1])
		# 		print("Box"+str(a+b))
		# 		numblocks = numblocks + 1
				
		# 	a = a + 1


		# pyrosim.Send_Cube(name = "Box0", pos = [0,0,1], size = tempsize)
		# pyrosim.Send_Joint(name = "Box0_Box1", parent = "Box0", child = "Box1", type = "revolute", position = [0, (tempsize[1] + tempsize2[1])/2.0, 0], jointAxis = "1 0 0")
		# pyrosim.Send_Cube(name = "Box1", pos = [0,0,1], size = tempsize2)
		# pyrosim.Send_Joint(name = "Box1_Box2", parent = "Box1", child = "Box2", type = "revolute", position = [0, (tempsize2[1] + tempsize3[1])/2.0, 0], jointAxis = "1 0 0")
		# pyrosim.Send_Cube(name = "Box2", pos = [0,0,1], size = tempsize3)
		# pyrosim.Send_Joint(name = "Box2_Box3", parent = "Box2", child = "Box3", type = "revolute", position = [0, (tempsize3[1] + tempsize4[1])/2.0, 0], jointAxis = "1 0 0")
		# pyrosim.Send_Cube(name = "Box3", pos = [0,0,1], size = tempsize4)
		# for a in range(1, self.randlength):
		# 	sizee = self.randsize()
			
		# 	pyrosim.Send_Joint(name = "Box"+str(a)+"_"+"Box"+str(a+1), parent = "Box"+str(a), child = "Box"+str(a+1), type = "revolute", position = self.poscalculator(a), jointAxis = "1 0 0")
		# 	pyrosim.Send_Cube(name = "Box"+str(a+1), pos = self.poscalculator(a, blocksize = sizee), size = sizee)
			
			
		
#       pyrosim.Send_Cube(name="Torso", pos = [0,0,1.4], size = [1,1,0.5])
#       pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position =[0.4,0.5,1], jointAxis = "1 0 0")
#       pyrosim.Send_Cube(name="FrontLeg", pos = [0,0,0], size= [l,h,w])
#       pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position =[0,-0.5,1], jointAxis = "1 0 0")
#       pyrosim.Send_Cube(name="BackLeg", pos = [-0.4,-0,0], size= [l,h,w])
#       pyrosim.Send_Joint( name = "Torso_UpLeg" , parent= "Torso" , child = "UpLeg" , type = "revolute", position =[0, 0.5,1], jointAxis = "1 0 0")
#       pyrosim.Send_Cube(name="UpLeg", pos = [-0.4, 0,0], size= [l,h,w])
#       pyrosim.Send_Joint( name = "Torso_DownLeg" , parent= "Torso" , child = "DownLeg" , type = "revolute", position =[0,-0.5,1], jointAxis = "1 0 0")
#       pyrosim.Send_Cube(name="DownLeg", pos = [0.4,0,0], size= [l,h,w])
#       pyrosim.Send_Cube(name="Head", pos = [-0.5,0.6, 0.5], size = [0.2,0.2,0.4])
#       pyrosim.Send_Joint(name = "Torso_Head", parent = "Torso", child = "Head", type = "revolute", position = [0.5,0,1], jointAxis = "0 1 0")
		pyrosim.End()

	def targnname(self, finalorno,x,y):
		if finalorno:
			z = int(random.randint(5,8))
			#print(self.a[x][y])
			self.a[x][y] = z
			return z
		else:
			return self.a[x][y]
   
   
	def Generate_Brain(self,finalorno):
		pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
		neurontracker = 0

		numofSensors = []
		numofJoints = []
		#sensors
		for a in self.cubename:
			if a[1] == "Green":
				numofSensors.append(neurontracker)
				pyrosim.Send_Sensor_Neuron(name = neurontracker, linkName = a[0])
				neurontracker+= 1
		#motors
		for b in self.jointnames:
			numofJoints.append(neurontracker)
			pyrosim.Send_Motor_Neuron(name = neurontracker, jointName = b)
			neurontracker+=1


		#synapses

		for currentRow in numofSensors:
			for currentColumn in numofJoints:
				pyrosim.Send_Synapse(sourceNeuronName = currentRow , targetNeuronName = currentColumn, weight = self.weights[currentRow][currentColumn])



		# neurontracker = 0
		# for a in range(0, self.randlength-1):
		# 	if self.blocks[a][1] == "Green":
		# 		pyrosim.Send_Sensor_Neuron(name = neurontracker, linkName = "Box"+str(a))
		# 		neurontracker = neurontracker + 1
		# 	pyrosim.Send_Motor_Neuron(name = neurontracker, jointName = "Box"+str(a)+"_"+"Box"+str(a+1))
		# 	neurontracker = neurontracker + 1
		
		# motorneurons = {}
		# abc = 0
		# for xyz in range(self.randlength):
		# 	if self.blocks[xyz][1] == "Green":
		# 		motorneurons[abc] = xyz
		# 		abc = abc + 1

		# print(motorneurons)
		# print(len(motorneurons))
		# for b in range(0,self.randlength):
		# 	if self.blocks[b][1] == "Green":
		# 		pyrosim.Send_Synapse(sourceNeuronName=b, targetNeuronName = motorneurons[random.randint(0,len(motorneurons.keys()) -1)], weight = 2*numpy.random.rand() - 1 )


#       pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")
#       pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")
#       pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
#       pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")
#       pyrosim.Send_Sensor_Neuron(name = 3, linkName = "UpLeg")
#       pyrosim.Send_Sensor_Neuron(name = 4, linkName = "DownLeg")
#       pyrosim.Send_Motor_Neuron(name = 5, jointName = "Torso_BackLeg")
#       pyrosim.Send_Motor_Neuron(name = 6, jointName = "Torso_FrontLeg")
#       pyrosim.Send_Motor_Neuron(name = 7, jointName = "Torso_UpLeg")
#       pyrosim.Send_Motor_Neuron(name = 8, jointName = "Torso_DownLeg")
#       #pyrosim.Send_Sensor_Neuron(name = 9, linkName = "Head")
#
#       for currentRow in range(0,c.numSensorNeurons):
#           for currentColumn in range (0,c.numMotorNeurons):
#               pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = random.randint(5,8), weight =self.weights[currentRow][currentColumn])
#       # pyrosim.Send_Synapse(sourceNeuronName = 0, targetNeuronName = 4, weight = 3.0)
#       # pyrosim.Send_Synapse(sourceNeuronName = 1, targetNeuronName = 4, weight = 15.0)
#       # pyrosim.Send_Synapse(sourceNeuronName = 2, targetNeuronName = 4, weight = 3.0)
#       # pyrosim.Send_Synapse(sourceNeuronName = 0, targetNeuronName = 3, weight = 0.2)
		pyrosim.End()

	#def Evaluate(self, dOrG):

	def Start_Simulation(self, dOrG):
		self.Create_World()
		#self.Create_Body()
		self.Create_Body()
		self.Generate_Brain(True)

		# while not os.path.exists("world.sdf"):
		#   time.sleep(0.01)
		# while not os.path.exists("body.urdf"):
		#   time.sleep(0.01)
		# while not os.path.exists("brain.nndf"):
		#   time.sleep(0.01)
		os.system("python3 simulate.py " + dOrG +" "+str(self.myID)+
						  #" 2&>1"+
						  " &")

	def Best_Simulation(self, dOrG):
		self.Create_World()
		self.Create_Body()
		self.Generate_Brain(False)

		# while not os.path.exists("world.sdf"):
		#   time.sleep(0.01)
		# while not os.path.exists("body.urdf"):
		#   time.sleep(0.01)
		# while not os.path.exists("brain.nndf"):
		#   time.sleep(0.01)
		os.system("python3 simulate.py " + dOrG +" "+str(self.myID)+
						  #" 2&>1"+
						  " &")

	def Wait_For_Simulation_To_End(self):
		while not os.path.exists("fitness" + str(self.myID)+".txt"):
			time.sleep(0.01)
		f = open("fitness" + str(self.myID)+".txt", "r")
		self.fitness = float(f.read())
		#print(self.fitness)
		f.close()
		os.system("rm " + "fitness" + str(self.myID)+".txt")
		os.system("rm body*.urdf")

	def Mutate(self):
		self.weights[random.randint(0,numpy.array(self.weights).shape[0]-1)][random.randint(0,numpy.array(self.weights).shape[1]-1)] = (random.random()*2) - 1
		probabilityint = random.randint(1,10)
		if probabilityint > 2:
			if probabilityint > 5:
				if probabilityint > 8:
					if random.randint(0,1) == 1:
						self.randlength += 3
					else:
						self.randlength -= 3
			else:
				self.randlength += 1

		else:
			self.randlength -= 1

	def Set_ID(self, numb):
		self.myID = numb
