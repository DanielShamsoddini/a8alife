import numpy
import matplotlib.pyplot
targetvalues = numpy.load("data/targetAnglesB.npy")
matplotlib.pyplot.plot(targetvalues, linewidth = 5, label = "Backleg")
targetvalues2 = numpy.load("data/targetAnglesF.npy")
matplotlib.pyplot.plot(targetvalues2, label = "Frontleg")
# backLegSensorValues = numpy.load("data/backLegSensorValues.npy")
# frontLegSensorValues = numpy.load("data/frontLegSensorValues.npy")
# print(backLegSensorValues)
# matplotlib.pyplot.plot(backLegSensorValues, linewidth = 5, label = "frontleg")
# matplotlib.pyplot.plot(frontLegSensorValues, label = "backleg")
matplotlib.pyplot.legend()
matplotlib.pyplot.show()