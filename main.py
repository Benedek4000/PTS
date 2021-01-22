import numpy as np
from planet import Planet
from tqdm import trange
import math
import constants as const
import config as conf
import matplotlib.pyplot as plt

initialTemperature = (((1-conf.albedo)*conf.starLuminosity)/(16*math.pi*const.STEFAN_BOLTZMANN_CONSTANT*conf.orbitalRadius**2))**(1/4)

earth = Planet(conf.radius, conf.orbitalRadius, conf.starLuminosity, conf.axialTilt, conf.specificHeatCapacity, conf.density, conf.albedo, conf.cellSize, initialTemperature)

f = open("results.txt", "x")
nextLine = "iterations"
for i in conf.cellsOfInterest:
    nextLine = nextLine + ";" + str(i)
nextLine = nextLine + "\n"
f.write(nextLine)

for t in trange(conf.iteration, desc="Simulating Temperature (1 state/it)"):
    earth.calculateNextState(60, t, f)
f.close()

for i in conf.cellsOfInterest:
    plt.plot(earth.cells[i].temp)
plt.savefig("plot.png")