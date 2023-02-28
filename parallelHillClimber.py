
from solution import SOLUTION
import constants as c
import copy
import os
import numpy
class PARALLEL_HILL_CLIMBER:
	def __init__(self):
		#os.system("rm brain*.nndf")
		#os.system("rm fitness*.txt")
		self.parents = {}
		self.nextAvailableID = 0
		for a in range(c.populationSize):
			self.parents[a] = SOLUTION(self.nextAvailableID)
			self.nextAvailableID = self.nextAvailableID + 1
		#print(self.parents)
		#exit()

	def Evolve(self):
		self.Evaluate(self.parents)

		# self.parent.Evaluate("GUI")
		for currentGeneration in range(c.numberOfGenerations):
			self.Evolve_For_One_Generation()
			#print("generation"+ str(currentGeneration))

		self.Show_Best()
		#self.Print()
		exit()

	def Evaluate(self,xyz):
		for parent in xyz:
			xyz[parent].Start_Simulation("DIRECT")
		for parent in self.parents:
			xyz[parent].Wait_For_Simulation_To_End()
			#print(self.parents[parent].fitness)

	def Evolve_For_One_Generation(self):
		self.Spawn()
		self.Mutate()
		self.Evaluate(self.children)
		self.Print()

		self.Select()

	def Spawn(self):
		self.children = {}
		for parent in self.parents:
			self.children[parent] = copy.deepcopy(self.parents[parent])
			self.children[parent].Set_ID(self.nextAvailableID)
			self.nextAvailableID = self.nextAvailableID + 1


	def Mutate(self):
		for child in self.children:
			self.children[child].Mutate()

	def Select(self):
		for child in self.children:
			if self.children[child].fitness > self.parents[child].fitness:
				self.parents[child] = self.children[child]

	def Print(self):
#		#for parent in self.parents:
#			#self.parents[parent].Evaluate("DIRECT")
#			print("\n")
#			print("parent: " + str(self.parents[parent].fitness))
#			print("child " + str(self.children[parent].fitness))
#			print("\n")
		
		parentfitness = [self.parents[parent].fitness for parent in self.parents]
		minarg = numpy.argmax(parentfitness)
		print()
		
		fil = open("seed1.txt", "a")
		fil.write(str(self.parents[minarg].fitness) + " ")
		fil.close()

	def Show_Best(self):

		print("finalgen")

		parentfitness = [self.parents[parent].fitness for parent in self.parents]
		minarg = numpy.argmax(parentfitness)
		#print(self.parents[minarg].fitness)
		self.parents[minarg].Best_Simulation("GUI")
		exit()
