import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
os.system("rm fitness*.txt")
os.system("rm world*.sdf")
phc = PARALLEL_HILL_CLIMBER()

phc.Evolve()
exit()
# for a in range(0,5):
# 	os.system("python3 generate.py")
# 	os.system("python3 simulate.py")
