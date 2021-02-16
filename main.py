import numpy as np
from planet import Planet
from tqdm import trange
import math
import constants as const
import config as conf
import matplotlib.pyplot as plt

starLuminosity = 0
a = 0
c = 1
if (conf.starMass < 0.43*const.SUN_MASS):
    a = 2.3
    c = 0.23
if (conf.starMass >= 0.43*const.SUN_MASS) and (conf.starMass < 2*const.SUN_MASS):
    a = 4
    c = 1
if (conf.starMass >= 2*const.SUN_MASS) and (conf.starMass < 55*const.SUN_MASS):
    a = 3.5
    c = 1.4
if (conf.starMass >= 55*const.SUN_MASS):
    a = 1
    c = 32000                                                                           #numbers taken from https://en.wikipedia.org/wiki/Mass%E2%80%93luminosity_relation
starLuminosity = const.SUN_LUMINOSITY*(c*(conf.starMass/const.SUN_MASS)**a) #L/L_o=c*(M/M_o)^a

initialTemperature = (((1-conf.albedo)*starLuminosity)/(16*math.pi*const.STEFAN_BOLTZMANN_CONSTANT*conf.orbitalRadius**2))**(1/4) #T=((1-a)L/(16*pi*sigma*d^2))^(1/4)

earth = Planet(conf.radius, conf.orbitalRadius, starLuminosity, conf.starMass, conf.obliquity, conf.dayLength, conf.specificHeatCapacity, conf.density, conf.albedo, conf.cellSize, initialTemperature)

f = open(conf.targetDataFile, "x")
nextLine = "iterations"
for i in conf.cellsOfInterest:
    nextLine = nextLine + ";" + str(i)
nextLine = nextLine + "\n"
f.write(nextLine)

for t in trange(conf.numberOfIterations, desc="Simulating Temperature (1 state/it)"):
    earth.calculateNextState(t, f)
f.close()

for i in conf.cellsOfInterest:
    x = []
    for j in range(conf.numberOfIterations+1):
        x.append(j*conf.iterationTime)
    plt.plot(x, earth.cells[i].temp, label="lat:{:.2f}°, lon:{:.2f}°".format(earth.cells[i].com[0], earth.cells[i].com[1]))
plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")
plt.legend(loc='lower right')
plt.savefig(conf.targetPlotFile, dpi=300)