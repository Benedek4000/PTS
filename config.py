COMprecision=10000 #number of iterations when calculating centre of mass for a cell
iteration = 864000

initialTemperature = 278 #initial temperature of the planet in Kelvins
cellSize = 0.1 #the side of a cell in degrees
radius = 6.371e+6  #radius of the planet in meters
orbitalRadius = 1.496e+11 #radius of the orbit of th eplanet in meters
starLuminosity = 3.828e+26 #in Watts(J/s)
specificHeatCapacity = 2000 #specific heat capacity of the planet's surface in J/(kg K)
density = 3000 # density of the surface of the planet in kg/m^3
albedo = 0.3
axialTilt = 23.5 #axial tilt of the planet in degrees, (0 is perpendicular to the field of the orbit)
cellsOfInterest = [0, 60000, 120000, 180000, 240000] #cells simulated, as a list of cell IDs