import math
import constants as const
import config as conf

class Cell:

    """class describing one surface zone on the planet
    
    latMin, latMax, lonMin, lonMax: the latitudes and longitudes bordering the cell in degrees (0 to 360, -90 to 90)
    temp: contains the temperature history
    area: area of the cell in m^2
    com: centre of mass of the cell. when the cell is treated as a pointlike object, this is its position [latitude, longitude]""" 
    
    def __init__(self, ID, latMin, latMax, lonMin, lonMax, initTemp, cellSize, radius):
        self.ID = ID
        self.latMin = latMin
        self.latMax = latMax
        self.lonMin = lonMin
        self.lonMax = lonMax
        self.temp = [initTemp]
        self.area = 1/720*abs(lonMax-lonMin)*abs(math.sin(math.radians(latMax))-math.sin(math.radians(latMin)))*4*math.pi*radius**2 #https://www.pmel.noaa.gov/maillists/tmap/ferret_users/fu_2004/msg00023.html  (pi/180)R^2 |sin(lat1)-sin(lat2)| |lon1-lon2|"""
        if self.ID in conf.cellsOfInterest:
            comLat = 0
            for i in range(conf.COMprecision+1):
                if (1/720*abs(lonMax-lonMin)*abs(math.sin(math.radians(latMin + i*cellSize/conf.COMprecision))-math.sin(math.radians(latMin)))) >= self.area/2:
                    comLat = latMin + i*cellSize/conf.COMprecision-(1/conf.COMprecision)/2
                    break
            self.com = [round(comLat, 4), round((lonMax+lonMin)/2, 4)]
        else:
            self.com = None

    def __repr__(self):
        #return "Latitude: {}° - {}°; Longitude: {}° - {}°; Area: {}".format(self.latMin, self.latMax, self.lonMin, self.lonMax, self.area)
        return "ID = {}   AREA =  {:.0f}  COM = [{:.3f}, {:.3f}]   TEMP = {:.0f}".format(self.ID, self.area, self.com[0], self.com[1], self.temp[len(self.temp)-1])