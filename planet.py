from cell import Cell
import numpy as np
from tqdm import trange
import random
import math
import constants as const
import config as conf

class Planet:

    """class describing the planet
    """

    def __init__(self, radius, orbitalRadius, starLuminosity, starMass, axialTilt, dayLength, specificHeatCapacity, density, albedo, cellSize, initialTemperature):
        self.radius = radius #m
        self.axialTilt = axialTilt #degrees
        self.density = density
        self.dayLength = dayLength
        self.period = ((4*math.pi**2*orbitalRadius**3)/(const.GRAVITATIONAL_CONSTANT*starMass))**(1/2) #s   T^2 = ((4*pi^2)/(G*M))*r^3
        self.maxEnergyIn = (1-albedo)*starLuminosity/(4*math.pi*orbitalRadius**2) #J m^-2   E/A = L*(1-a)/(4*pi*R^2), Sun at 90 degrees
        self.SHC = specificHeatCapacity #J kg^-1 K^-1
        self.cells = self.createCells(cellSize, initialTemperature, radius)

    def __repr__(self):
        return "r={:.0f}   AxialTilt={:.2f}   MaxEnergyIn={}   SHC={}".format(self.radius, self.axialTilt, self.maxEnergyIn, self.SHC)

    def createCells(self, cellSize, initialTemperature, radius):
        cells = {}
        id = 0
        for i in trange(int(const.LAT_RANGE/cellSize), desc="Creating Cells ("+"{:.0f}".format(const.LON_RANGE/cellSize)+"/it)"):
            for j in range(int(const.LON_RANGE/cellSize)):
                cells.update({id: Cell(id, -90+i*cellSize, -90+cellSize+i*cellSize, 0+j*cellSize, 0+cellSize+j*cellSize, initialTemperature, cellSize, radius)})
                id = id + 1
        return cells

    def calculateNextState(self, tqdmValue, fileToWrite):
        nextLine = str(tqdmValue*conf.iterationTime)
        for i in conf.cellsOfInterest:
                currentCell = self.cells[i]
                currentTemp = currentCell.temp[len(currentCell.temp)-1]
                angleDueRotation = currentCell.com[1]-const.LON_RANGE*(tqdmValue*conf.iterationTime/self.dayLength)
                angleOfIncidence = angleDueRotation
                #print(str(tqdmValue*conf.iterationTime/self.dayLength), str(angleOfIncidence), str(math.cos(math.radians(angleOfIncidence))))
                if math.cos(math.radians(angleOfIncidence)) > 0:
                    TempIn = math.cos(math.radians(angleOfIncidence))*conf.iterationTime*self.maxEnergyIn*currentCell.area/(self.SHC*currentCell.area*const.SUN_PENETRATION_DEPTH*self.density)
                else:
                    TempIn = 0
                TempOut = conf.iterationTime*currentCell.area*conf.emissivity*const.STEFAN_BOLTZMANN_CONSTANT*currentTemp**4/(self.SHC*currentCell.area*const.SUN_PENETRATION_DEPTH*self.density)
                #print("Current:{:.0f}   In:{:.8f}   Out:{:.8f}".format(currentTemp, TempIn, TempOut))
                currentCell.temp.append(currentTemp+TempIn-TempOut)
                self.cells[i] = currentCell
                nextLine = nextLine + ";" + str(round(currentCell.temp[len(currentCell.temp)-1], 1))
        nextLine = nextLine + "\n"
        if tqdmValue%conf.iterationPerSave: 
            fileToWrite.write(nextLine)