
from solution import SOLUTION
import constants as c
import copy
class HILL_CLIMBER:
	def __init__(self):
		self.parent = SOLUTION()

	def Evolve(self):
		self.parent.Evaluate("GUI")
		for currentGeneration in range(c.numberOfGenerations):
			self.Evolve_For_One_Generation()

		self.Show_Best()
		exit()

	def Evolve_For_One_Generation(self):
		self.Spawn()
		self.Mutate()
		self.child.Evaluate("DIRECT")
		self.Print()
		self.Select()

	def Spawn(self):
		self.child = copy.deepcopy(self.parent)

	def Mutate(self):
		self.child.Mutate()

	def Select(self):
		if self.child.fitness > self.parent.fitness:
			self.parent = self.child

	def Print(self):
		print("\n")
		print("parent: " + str(self.parent.fitness))
		print("child: " + str(self.child.fitness))

	def Show_Best(self):
		print("finalgen")
		self.parent.Evaluate("GUI")