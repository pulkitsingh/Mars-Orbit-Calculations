# E0 259: Data Analytics. Module 1: Mars Orbit. Question 2.
# Pulkit Singh, July 18 2018

# importing required modules
import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# importing file containing required values calculated in other modules
import cfg

# importing custom module to run gradient descent on mars orbital plane
import planeGradientDescent

#-------------------------------------------------------------------------------#

# Part 1: Finding Mars' Heliocentric Latitudes & Celestial Sphere Location

opp = "opposition.csv"

fields = []
r = cfg.r          # estimated radius of mars projection on ecliptic plane
helioLong = []     # heliocentric longitude of Mars (in radians)
geoLat = []        # geocentric latitude of Mars (in radians)
helioLat = []      # heliocentric latitude of Mars (in radians)

# reading in opposition csv file
with open(opp, 'r') as oppfile:
	opposition = csv.reader(oppfile)

	fields = opposition.next()

	for row in opposition:

		# Computing heliocentric longitudes (in radians)
		helioLong.append(math.radians((30 * float(row[3])) + float(row[4]) 
			+ (float(row[5])/60) + (float(row[6])/3600)))

		# Computing geocentric latitudes (in radians)
		geoLat.append(math.radians(float(row[7]) + (float(row[8])/60)))


# Computing heliocentric latitude from geocentric latitude 
scale = (r - 1)/r
for angle in geoLat:
	helioLat.append(math.atan(scale * math.tan(angle)))


# Computing Mars' location on the Celestial Sphere

# initalising lists for mars' celestial sphere coordinates
xMars = []
yMars = []
zMars = []

# Given the radius of celestial sphere, latitude and longitude of mars, we have
# spherical coordinates of Mars.
# Spherical coordinates can be converted to cartesian using the formula:
# 	x = radius * cos(pi/2 - latitude) * cos(longitude)
# 	y = radius * sin(pi/2 - latitude) * sin(longitude)
#   z = radius * cos(pi/2 - latitude)
for i in range(len(helioLat)):
	xMars.append(math.sin((math.pi / 2.0)-helioLat[i]) * math.cos(helioLong[i]))
	yMars.append(math.sin((math.pi / 2.0)-helioLat[i]) * math.sin(helioLong[i]))
	zMars.append(math.cos((math.pi / 2.0)-helioLat[i]))

print("\nComputing heliocentric latitudes of Mars's location.\n")

#-------------------------------------------------------------------------------#

# Part 2 + 3: Finding best fit plane for Mars's Orbital Plane

# creating coordinate matrix: [x, y, z]
coordinates = np.array([xMars, yMars, zMars]).T

# initalizing guesses for plane parameters a and b to be 0.0
a, b = 0.0, 0.0

# initialising alpha as the step value
alpha = 0.0001

# initialising array to keep track of cost values in gradient descent
cost = []

# running gradient descent
for i in range (10000):
	
	# finding cost for given parameter values a & b
	squareDist = planeGradientDescent.evaluateDistance(coordinates, a, b)

	# adding current cost to list of previous costs
	cost.append(squareDist)
	
	# finding gradient with parameter values a & b
	delta = planeGradientDescent.computeGradient(coordinates, a, b)
	
	# updating parameter values
	a = a - (alpha * delta[0])
	b = b - (alpha * delta[1])


# printing results of gradient descent
print "Running gradient descent to compute best fit orbital plane for Mars:"
print "Finding parameters for plane with equation ax + by + z = 0."
print "Final Square Distance: ", squareDist
print "Final a: ", a
print "Final b: ", b
angle = math.acos(1/(math.sqrt(math.pow(a, 2) + math.pow(b, 2) + 1.0)))
print
print "Calculating orbital angle from best-fit orbital plane:"
degAngle = math.degrees(angle)
print "Orbital angle (degrees) = ", degAngle
print "Orbital angle (DMS) = ", int(degAngle), "degrees", int((degAngle % 1) * 60), "minutes" 


# creating a figure
fig = plt.figure()
ax = Axes3D(fig)

# plotting Mars's locations on the celestial sphere
ax.scatter(xMars, yMars, zMars)

# plotting mars's best-fit orbital plane
point = np.array([0.0, 0.0, 0.0])
normal = np.array([a, b, 1.0])
d = -point.dot(normal)
xx, yy = np.meshgrid(range(-2, 3), range(-2, 3))
z = (-normal[0] * xx - normal[1] * yy - d) * 1. /normal[2]
ax.plot_surface(xx, yy, z, alpha=0.2)

plt.show()

# plotting cost as a function of number of iterations
# plt.plot(cost)
# plt.show()

#-------------------------------------------------------------------------------#








