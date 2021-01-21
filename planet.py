from cell import Cell
import numpy as np
from tqdm import trange
import random
import math
import constants as const

class Planet:

    """class describing the planet
    """

    def __init__(self, radius, orbitalRadius, starLuminosity, axialTilt, specificHeatCapacity, density, albedo, cellSize, initialTemperature, COMprecision, cellsOfInterest):
        self.radius = radius #m
        self.axialTilt = axialTilt #degrees
        self.density = density
        self.maxEnergyIn = (1-albedo)*starLuminosity/(4*math.pi*orbitalRadius**2) #J m^-2 E/A = L*(1-a)/(4*pi*R^2), Sun at 90 degrees
        self.SHC = specificHeatCapacity #J kg^-1 K^-1
        self.cells = self.createCells(cellSize, initialTemperature, radius, COMprecision, cellsOfInterest)

    def __repr__(self):
        return "r={:.0f}   AxialTilt={:.2f}   MaxEnergyIn={}   SHC={}".format(self.radius, self.axialTilt, self.maxEnergyIn, self.SHC)

    def createCells(self, cellSize, initialTemperature, radius, COMprecision, cellsOfInterest):
        cells = {}
        id = 0
        for i in trange(int(const.LAT_RANGE/cellSize), desc="Creating Cells ("+"{:.0f}".format(const.LON_RANGE/cellSize)+"/it)"):
            for j in range(int(const.LON_RANGE/cellSize)):
                cells.update({id: Cell(id, -90+i*cellSize, -90+cellSize+i*cellSize, 0+j*cellSize, 0+cellSize+j*cellSize, initialTemperature, cellSize, radius, COMprecision, cellsOfInterest)})
                id = id + 1
        return cells

    def calculateNextState(self, intervalBetweenStates, tqdmValue, fileToWrite, cellsOfInterest):
        nextLine = str(tqdmValue)
        for i in cellsOfInterest:
                currentCell = self.cells[i]
                currentTemp = currentCell.temp[len(currentCell.temp)-1]
                TempIn = abs(math.sin(i))*self.maxEnergyIn*currentCell.area/(self.SHC*currentCell.area*0.1*self.density) #number is depth in m, should be determined
                TempOut = currentCell.area*const.STEFAN_BOLTZMANN_CONSTANT*currentTemp**4/(self.SHC*currentCell.area*0.1*self.density) #number is depth in m, should be determined
                #print("Current:{:.0f}   In:{:.8f}   Out:{:.8f}".format(currentTemp, TempIn, TempOut))
                currentCell.temp.append(currentTemp+TempIn-TempOut)
                self.cells[i] = currentCell
                nextLine = nextLine + ";" + str(currentCell.temp[len(currentCell.temp)-1])
        nextLine = nextLine + "\n"
        fileToWrite.write(nextLine)