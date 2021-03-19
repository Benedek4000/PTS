targetDataFile = "results.txt"
targetPlotFile = "plot.png"

COMprecision = 10000 #number of iterations when calculating centre of mass for a cell
numberOfIterations = 10*365*24*12 #number of iterations
iterationTime = 300 #time interval between  in seconds
iterationPerSave = 10 #save after every x iteration

cellSize = 0.1 #the side of a cell in degrees
star_penetration_depth = 8 #the depth which the radiation reaches in the surface of the planet in meters
radius = 6.371e+6  #radius of the planet in meters
orbitalRadius = 1.496e+11 #radius of the orbit of the planet in meters
starMass = 1.989e+30 #in kg
dayLength = 58.5*86400 #in seconds
specificHeatCapacity = 2000 #specific heat capacity of the planet's surface in J/(kg K)
density = 2.83e3 # density of the surface of the planet in kg/m^3
albedo = 0 #0.31 for Earth
emissivity = 1 #0.95-1 for Earth
obliquity = 0 #obliquity of the planet in degrees, (0 is perpendicular to the field of the orbit)
#cellsOfInterest = [0, 720000, 1620000, 2520000, 3240000, 6480000-2520000, 6480000-1620000, 6480000-720000, 6480000-3600] #cells simulated, as a list of cell IDs
cellsOfInterest = [3240000, 3600000, 3960000, 4320000]