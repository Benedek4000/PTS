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

    def __init__(self, radius, orbitalRadius, starLuminosity, starMass, obliquity, dayLength, specificHeatCapacity, density, albedo, cellSize, initialTemperature):
        self.radius = radius #m
        self.obliquity = obliquity #degrees
        self.density = density
        self.dayLength = dayLength
        self.period = ((4*math.pi**2*orbitalRadius**3)/(const.GRAVITATIONAL_CONSTANT*starMass))**(1/2) #s   T^2 = ((4*pi^2)/(G*M))*r^3
        self.maxEnergyIn = (1-albedo)*starLuminosity/(4*math.pi*orbitalRadius**2) #J s^-1 m^-2   E/A = L*(1-a)/(4*pi*R^2), Sun at 90 degrees
        self.SHC = specificHeatCapacity #J kg^-1 K^-1
        self.cells = self.createCells(cellSize, initialTemperature, radius)

    def __repr__(self):
        return "r={:.0f}   Obliquity={:.2f}   MaxEnergyIn={}   SHC={}".format(self.radius, self.obliquity, self.maxEnergyIn, self.SHC)

    def createCells(self, cellSize, initialTemperature, radius):
        cells = {}
        id = 0
        #for i in trange(int(const.LAT_RANGE/cellSize), desc="Creating Cells ("+"{:.0f}".format(const.LON_RANGE/cellSize)+"/it)"):
        for i in range(int(const.LAT_RANGE/cellSize)):
            for j in range(int(const.LON_RANGE/cellSize)):
                cells.update({id: Cell(id, -90+i*cellSize, -90+cellSize+i*cellSize, 0+j*cellSize, 0+cellSize+j*cellSize, initialTemperature, cellSize, radius)})
                id = id + 1
        return cells

    def xcalculateNextState(self, tqdmValue, fileToWrite):
        #nextLine = str(tqdmValue*conf.iterationTime)
        for i in conf.cellsOfInterest:
                currentCell = self.cells[i]
                currentTemp = currentCell.temp[len(currentCell.temp)-1]
                eff_obliquity = -self.obliquity*math.cos(2*math.pi*tqdmValue*conf.iterationTime/self.period)
                if (90-abs(currentCell.com[0])+eff_obliquity)<90:
                    max_angle = 90-abs(currentCell.com[0])+eff_obliquity
                else:
                    max_angle = 90+abs(currentCell.com[0])-eff_obliquity
                if (-90+abs(currentCell.com[0])+eff_obliquity)>-90:
                    min_angle = -90+abs(currentCell.com[0])+eff_obliquity
                else:
                    min_angle = -90-abs(currentCell.com[0])-eff_obliquity
                mid_angle = (max_angle+min_angle)/2
                angle_range = (max_angle-min_angle)/2
                AngleOfIncidence = np.sign(currentCell.com[0])*mid_angle-angle_range*math.cos(math.radians(currentCell.com[1]-const.LON_RANGE*tqdmValue*conf.iterationTime/self.dayLength))
                sinAngleOfIncidence = math.sin(math.radians(AngleOfIncidence))
                sinAngleOfIncidence = np.heaviside(sinAngleOfIncidence, 0)*sinAngleOfIncidence
                TempIn = sinAngleOfIncidence*conf.iterationTime*self.maxEnergyIn*currentCell.area/(self.SHC*currentCell.area*conf.star_penetration_depth*self.density)
                TempOut = conf.iterationTime*currentCell.area*conf.emissivity*const.STEFAN_BOLTZMANN_CONSTANT*currentTemp**4/(self.SHC*currentCell.area*conf.star_penetration_depth*self.density)
                currentCell.temp.append(currentTemp+TempIn-TempOut)
                self.cells[i] = currentCell
                #nextLine = nextLine + ";" + str(round(currentCell.temp[len(currentCell.temp)-1], 1))
        #nextLine = nextLine + "\n"
        #if tqdmValue%conf.iterationPerSave==0: 
            #fileToWrite.write(nextLine)

    def calculateNextState(self, tqdmValue):
        for i in conf.cellsOfInterest:
                currentCell = self.cells[i]
                currentTemp = currentCell.temp[len(currentCell.temp)-1]
                eff_obliquity = -self.obliquity*math.cos(2*math.pi*tqdmValue*conf.iterationTime/self.period)
                if (90-abs(currentCell.com[0])+eff_obliquity)<90:
                    max_angle = 90-abs(currentCell.com[0])+eff_obliquity
                else:
                    max_angle = 90+abs(currentCell.com[0])-eff_obliquity
                if (-90+abs(currentCell.com[0])+eff_obliquity)>-90:
                    min_angle = -90+abs(currentCell.com[0])+eff_obliquity
                else:
                    min_angle = -90-abs(currentCell.com[0])-eff_obliquity
                mid_angle = (max_angle+min_angle)/2
                angle_range = (max_angle-min_angle)/2
                AngleOfIncidence = np.sign(currentCell.com[0])*mid_angle-angle_range*math.cos(math.radians(currentCell.com[1]-const.LON_RANGE*tqdmValue*conf.iterationTime/self.dayLength))
                sinAngleOfIncidence = math.sin(math.radians(AngleOfIncidence))
                sinAngleOfIncidence = np.heaviside(sinAngleOfIncidence, 0)*sinAngleOfIncidence
                TempIn = sinAngleOfIncidence*conf.iterationTime*self.maxEnergyIn*currentCell.area/(self.SHC*currentCell.area*conf.star_penetration_depth*self.density)
                TempOut = conf.iterationTime*currentCell.area*conf.emissivity*const.STEFAN_BOLTZMANN_CONSTANT*currentTemp**4/(self.SHC*currentCell.area*conf.star_penetration_depth*self.density)
                currentCell.temp.append(currentTemp+TempIn-TempOut)
                self.cells[i] = currentCell