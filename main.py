import numpy as np
from planet import Planet
from tqdm import trange
import math
import constants as const
import config as conf
import matplotlib.pyplot as plt

COMprecision = conf.COMprecision
initialTemperature = conf.initialTemperature
cellSize = conf.cellSize
radius = conf.radius
orbitalRadius = conf.orbitalRadius
starLuminosity = conf.starLuminosity
specificHeatCapacity = conf.specificHeatCapacity
density = conf.density
albedo = conf.albedo
axialTilt = conf.axialTilt
cellsOfInterest = conf.cellsOfInterest

if cellsOfInterest == []:
    for i in range(int(const.LON_RANGE*const.LAT_RANGE/(cellSize**2))):
        cellsOfInterest.append(i)

earth = Planet(radius, orbitalRadius, starLuminosity, axialTilt, specificHeatCapacity, density, albedo, cellSize, initialTemperature, COMprecision, cellsOfInterest)

iteration = conf.iteration
f = open("results.txt", "x")
nextLine = "iterations"
for i in cellsOfInterest:
    nextLine = nextLine + ";" + str(i)
nextLine = nextLine + "\n"
f.write(nextLine)

for t in trange(iteration, desc="Simulating Temperature (1 state/it)"):
    earth.calculateNextState(60, t, f, cellsOfInterest)
f.close()

for i in cellsOfInterest:
    plt.plot(earth.cells[i].temp)
plt.savefig("plot.png")