import numpy as np
from planet import Planet
from tqdm import tqdm, trange
import math
import constants as const
import config as conf
import matplotlib.pyplot as plt

"""Tmax=0
Tmin=1e6

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

exoplanet = Planet(conf.radius, conf.orbitalRadius, starLuminosity, conf.starMass, conf.obliquity, conf.dayLength, conf.specificHeatCapacity, conf.density, conf.albedo, conf.cellSize, initialTemperature)

f = open(conf.targetDataFile, "x")
nextLine = "iterations"
for i in conf.cellsOfInterest:
    nextLine = nextLine + ";" + str(i)
nextLine = nextLine + "\n"
f.write(nextLine)

for t in trange(conf.numberOfIterations, desc="Simulating Temperature (1 state/it)"):
    exoplanet.xcalculateNextState(t, f)
f.close()

for i in conf.cellsOfInterest:
    x = []
    for j in range(conf.numberOfIterations+1):
        x.append(j*conf.iterationTime)
    plt.plot(x, exoplanet.cells[i].temp, label="lat:{:.2f}°, lon:{:.2f}°".format(exoplanet.cells[i].com[0], exoplanet.cells[i].com[1]))
plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")
plt.legend(loc='lower right')
plt.savefig(conf.targetPlotFile, dpi=300)

for i in conf.cellsOfInterest:
    for j in exoplanet.cells[i].temp[int(len(exoplanet.cells[i].temp)//2):]:
        if j < Tmin:
            Tmin = j
        if j > Tmax:
            Tmax = j
print("L = {:.3e} W/m^2\nr = {:.3e} m\nObliquity = {:.1f} degrees\nT_min = {:.0f} K\nT_max = {:.0f} K".format(starLuminosity, conf.orbitalRadius, conf.obliquity, Tmin*const.GREENHOUSE_EFFECT_COEFFICIENT, Tmax*const.GREENHOUSE_EFFECT_COEFFICIENT))
"""

f = open(conf.targetDataFile, "x")
nextLine = "Mass(kg);Orbital Radius(m);Obliquity(degrees);Luminosity(W/m^2);Tmin(K);Tmax(K)\n"
f.write(nextLine)

mass=[18.0, 3.2, 1.7, 1.1, 0.8, 0.3] #in solar masses
radius=[0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 15.0, 20.0] # in AU
#obliquity=[0.0, 10.0, 20.0, 30.0, 40.0] #in degrees
obliquity=[0.0]

AU = 1.496e11

for i in tqdm(mass, leave=None):
    for j in tqdm(radius, leave=None):
        for k in tqdm(obliquity, leave=None):

            currentMass = i*const.SUN_MASS
            currentRadius = j*AU
            currentObliquity = k

            Tmax=0
            Tmin=1e6

            starLuminosity = 0
            a = 0
            c = 1
            if (currentMass < 0.43*const.SUN_MASS):
                a = 2.3
                c = 0.23
            if (currentMass >= 0.43*const.SUN_MASS) and (currentMass < 2*const.SUN_MASS):
                a = 4
                c = 1
            if (currentMass >= 2*const.SUN_MASS) and (currentMass < 55*const.SUN_MASS):
                a = 3.5
                c = 1.4
            if (currentMass >= 55*const.SUN_MASS):
                a = 1
                c = 32000                                                                           #numbers taken from https://en.wikipedia.org/wiki/Mass%E2%80%93luminosity_relation
            starLuminosity = const.SUN_LUMINOSITY*(c*(currentMass/const.SUN_MASS)**a) #L/L_o=c*(M/M_o)^a

            initialTemperature = (((1-conf.albedo)*starLuminosity)/(16*math.pi*const.STEFAN_BOLTZMANN_CONSTANT*currentRadius**2))**(1/4) #T=((1-a)L/(16*pi*sigma*d^2))^(1/4)

            if initialTemperature < 1500:
                exoplanet = Planet(conf.radius, currentRadius, starLuminosity, currentMass, currentObliquity, conf.dayLength, conf.specificHeatCapacity, conf.density, conf.albedo, conf.cellSize, initialTemperature)

                for t in range(conf.numberOfIterations):
                    exoplanet.calculateNextState(t)

                for l in conf.cellsOfInterest:
                    for m in exoplanet.cells[l].temp[int(len(exoplanet.cells[l].temp)/2):]:
                        if m < Tmin:
                            Tmin = m
                        if m > Tmax:
                            Tmax = m

                nextLine = str(currentMass) + ";" + str(currentRadius) + ";" + str(currentObliquity) + ";" + str(starLuminosity) + ";" + str(Tmin*const.GREENHOUSE_EFFECT_COEFFICIENT) + ";" + str(Tmax*const.GREENHOUSE_EFFECT_COEFFICIENT) + "\n"
                f.write(nextLine)

f.close()