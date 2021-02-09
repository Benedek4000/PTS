targetDataFile = "results.txt"
targetPlotFile = "plot.png"

COMprecision = 10000 #number of iterations when calculating centre of mass for a cell
numberOfIterations = 3*365*24*12 #number of iterations
iterationTime = 300 #time interval between  in seconds
iterationPerSave = 10 #save after every x iteration

cellSize = 0.1 #the side of a cell in degrees
star_penetration_depth = 0.1 #the depth which the radiation reaches in the surface of the planet in meters
radius = 6.371e+6  #radius of the planet in meters
orbitalRadius = 1.496e+11 #radius of the orbit of the planet in meters
starLuminosity = 3.828e+26 #in Watts(J/s)
starMass = 1.989e+30 #in kg
dayLength = 86400 #in seconds
specificHeatCapacity = 2000 #specific heat capacity of the planet's surface in J/(kg K)
density = 3000 # density of the surface of the planet in kg/m^3
albedo = 0.31 #0.31 for Earth
emissivity = 0.95 #0.95-1 for Earth
obliquity = 23.5 #obliquity of the planet in degrees, (0 is perpendicular to the field of the orbit)
#cellsOfInterest = [0, 720000, 1620000, 2520000, 3240000, 6480000-2520000, 6480000-1620000, 6480000-720000, 6480000-3600] #cells simulated, as a list of cell IDs
cellsOfInterest = [0, 1440000, 2160000, 3240000]
#cellsOfInterest = [0, 3240000]