from simulation import SIMULATION
from world import WORLD
import sys
dorg = sys.argv[1]
brainnn = sys.argv[2]
simulation = SIMULATION(dorg, brainnn)
simulation.Get_Fitness()

# import pybullet as p
# import time
# import pybullet_data
# import pyrosim.pyrosim as pyrosim
# import numpy
# import math
# import random
# import constants as c









# backLegSensorValues = numpy.zeros(1000)
# frontLegSensorValues = numpy.zeros(1000)
# for a in range(0,1000):
#     p.stepSimulation()
#     backLegSensorValues[a] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
#     frontLegSensorValues[a] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
#     x1 = numpy.linspace(0*c.frequencyB+c.phaseOffsetB,2*numpy.pi*c.frequencyB+c.phaseOffsetB,1000)
#     x1 = numpy.sin(x1)
#     targetAnglesB = numpy.interp(x1, (x1.min(), x1.max()), (-c.amplitudeB, c.amplitudeB))
#     x2= numpy.linspace(0*c.frequencyF+c.phaseOffsetF,2*numpy.pi*c.frequencyF+c.phaseOffsetF,1000)
#     x2 = numpy.sin(x2)
#     targetAnglesF = numpy.interp(x2, (x2.min(), x2.max()), (-c.amplitudeF, c.amplitudeF))
#     numpy.save("data/targetAnglesB",targetAnglesB)
#     numpy.save("data/targetAnglesF",targetAnglesF)
#     pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_BackLeg", controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesB[a], maxForce = 25)
#     pyrosim.Set_Motor_For_Joint(bodyIndex = robotId, jointName = "Torso_FrontLeg", controlMode = p.POSITION_CONTROL, targetPosition = targetAnglesF[a], maxForce = 25)

#     time.sleep(1/600)
    

# #print(backLegSensorValues)
# numpy.save("data/backLegSensorValues",backLegSensorValues)
# numpy.save("data/frontLegSensorValues",frontLegSensorValues)

