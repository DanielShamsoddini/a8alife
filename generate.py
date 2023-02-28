import pyrosim.pyrosim as pyrosim
def Create_World():   
    pyrosim.Start_SDF("world.sdf")
    l = 1
    w = 1
    h = 1
    pyrosim.Send_Cube(name="Box", pos = [100,100,1.5], size = [l,w,h])
    pyrosim.End()

#Create_World()

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")
    l = 1
    w = 1
    h = 1
    pyrosim.Send_Cube(name="Torso", pos = [0,0,0.5], size = [l,w,h])
    pyrosim.Send_Joint( name = "Torso_Leg" , parent= "Torso" , child = "Leg" , type = "revolute", position =[0,0,1])
    pyrosim.Send_Cube(name="Leg", pos = [1,0,0.5], size= [l,w,h])
    pyrosim.End()

#Create_Robot()
def Create_Robot2():
    pyrosim.Start_URDF("body.urdf")
    l = 1
    w = 1
    h = 1
    pyrosim.Send_Cube(name="Torso", pos = [0,0,1.5], size = [l,w,h])
    pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position =[-0.5,0,1])
    pyrosim.Send_Cube(name="BackLeg", pos = [-0.5,0,-0.5], size= [l,w,h])
    pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position =[0.5,0,1])
    pyrosim.Send_Cube(name="FrontLeg", pos = [0.5,0,-0.5], size= [l,w,h])
    pyrosim.End()
Create_Robot2()
def Generate_Brain():
    pyrosim.Start_NeuralNetwork("brain.nndf")
    pyrosim.Send_Sensor_Neuron(name = 0, linkName = "Torso")
    pyrosim.Send_Sensor_Neuron(name = 1, linkName = "BackLeg")
    pyrosim.Send_Sensor_Neuron(name = 2, linkName = "FrontLeg")
    pyrosim.Send_Motor_Neuron(name = 3, jointName = "Torso_BackLeg")
    pyrosim.Send_Motor_Neuron(name = 4, jointName = "Torso_FrontLeg")
    pyrosim.Send_Synapse(sourceNeuronName = 0, targetNeuronName = 4, weight = 3.0)
    pyrosim.Send_Synapse(sourceNeuronName = 1, targetNeuronName = 4, weight = 15.0)
    pyrosim.Send_Synapse(sourceNeuronName = 2, targetNeuronName = 4, weight = 3.0)
    pyrosim.Send_Synapse(sourceNeuronName = 0, targetNeuronName = 3, weight = 0.2)
    pyrosim.End()
Generate_Brain()
#for c in range(0,5):
#    for b in range(0,5):
#        l = 1
#        w = 1
#        h = 1
#        for a in range(0,10):
#            pyrosim.Send_Cube(name = ("Box"+str(a)+str(b)+str(c)) , pos = [b,c,0.5+a], size = [l,w,h])
#            l = 0.9*l
#            w = 0.9*w
#            h = 0.9*h
#pyrosim.Send_Cube(name="Box", pos = [0,0,0.5], size = [l,w,h])
#pyrosim.Send_Cube(name="Box2", pos = [1,0,1.5], size = [l,w,h])
#pyrosim.End()
