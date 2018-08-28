""" This module fits an orbit for mars with an approach more in line with
Kepler's original model. It assumes that there is a point on the circle
called the average-sun, from which Mars has uniform angular velocity. It
finds the position of the average sun and the angle of the line of apsides
(the line that connects the sun and average sun).

"""

#----------------------------------------------------------------------------#

# importing necessary modules
import csv
import math
import matplotlib.pyplot as plt
import numpy as np
import random
from scipy.optimize import minimize
from scipy.stats import mstats as stat

#----------------------------------------------------------------------------#

# loads opposition data set, returns two lists of mars longitudes with 
# respect to actual sun and average sun respectively
def loadData():
	opp = "opposition.csv"

	sunLong = []
	avgLong = []

	# reading in opposition csv file
	with open(opp, 'r') as oppfile:
		opposition = csv.reader(oppfile)

		fields = opposition.next()

		for row in opposition:

			# Computing mars longitudes w.r.t actual sun (in radians)
			sunLong.append(math.radians((30 * float(row[3])) + float(row[4]) 
				+ (float(row[5])/60) + (float(row[6])/3600)))

			# Computing mars longitudes w.r.t average sun (in radians)
			avgLong.append(math.radians((30 * float(row[9])) + float(row[10]) 
				+ (float(row[11])/60) + (float(row[12])/3600)))

	return sunLong, avgLong

#----------------------------------------------------------------------------#

# calculates distance from origin of point (x, y)
def computeRadius(x, y):
	return math.sqrt(math.pow(x, 2) + math.pow(y, 2))

#----------------------------------------------------------------------------#

# calculates sum of squared error between mean value and each observation
def squareError(mean, observation):
	errorSum = 0.0
	n = len(observation)
	for i in range(n):
		error = math.pow((mean - observation[i]), 2)
		errorSum = errorSum + error
	return errorSum / n

#----------------------------------------------------------------------------#

# Takes y-distance of average sun (a) and sun (b) from center and list of 
# longitudes from actual and average sun, and returns x-y coordinates of
# triangulated mars locations and distance of each position from origin
def computeCoordinates(ty, a, sunLong, avgLong):

	t = ty[0]
	theta = ty[1]

	cos_t = math.cos(theta)
	sin_t = math.sin(theta)

	# creating list for radius of mars
	xMars = []
	yMars = []
	rMars = []

	# finding positions of mars and distance of each position from origin
	for i in range(len(sunLong)):
		
		# calculating slope of lines from actual and average sun
		sunSlope = math.tan(sunLong[i])
		avgSlope = math.tan(avgLong[i])

		# calculating x-y coordinates
		diff = avgSlope - sunSlope
		x = ((cos_t * ((a * t * sunSlope) + (a * avgSlope))) 
			- (sin_t * (a + t * a))) / diff
		y = ((x - a * cos_t) * avgSlope) + a * sin_t

		xMars.append(x)
		yMars.append(y)

		# calculating radius
		r = computeRadius(x, y)
		rMars.append(r)

	return xMars, yMars, rMars

#----------------------------------------------------------------------------#

# Takes y-distance of average sun (a) and sun (b) from center and list of 
# longitudes from actual and average sun, and returns the sum of losses for 
# fitting a circle for the triangulated positions of mars
def computeCost(t, a, sunLong, avgLong):

	# finding x-y coordinates, radii values of mars for given a, b values
	xMars, yMars, rMars = computeCoordinates(t, a, sunLong, avgLong)
	#print 'x-coordinates', xMars
	#print 'y-coordinates', yMars

	# calculating average radius
	radius = sum(rMars) / len(rMars)

	# calculating the arithmetic mean
	aMean = squareError(radius, rMars)
	#print 'Arithmetic Mean:', aMean

	# calculating the geometic mean
	gMean = stat.gmean(rMars)
	#print 'Geometric Mean:', gMean

	return np.log(aMean/gMean)

#----------------------------------------------------------------------------#

# Takes parameters of model (distance between sun and center, reference angle),
# scale parameter, and longitudes. Plots the positions of mars, average sun,
# sun, and the best-fit circle
def plotResults(parameters, a, sunLong, avgLong):
	xMars, yMars, rMars = computeCoordinates(parameters, a, sunLong, avgLong)

	t = parameters[0]
	theta = parameters[1]
	sin_t = math.sin(theta)
	cos_t = math.cos(theta)

	# finding radius of best fit circle
	r = sum(rMars)/len(rMars)
	print 'Radius =', r

	fig, ax = plt.subplots()
	ax.plot(xMars, yMars, 'ro')                    # plotting mars
	ax.plot(a * cos_t, a * sin_t, 'go')            # plotting average-sun
	ax.plot(-1 * t * cos_t, -1 * t * sin_t, 'yo')  # plotting sun

	fit = plt.Circle((0,0), r, color='g', fill=False) 
	ax.add_artist(fit)

	lim = r * 1.5
	ax.set_xlim(-lim, lim)
	ax.set_ylim(-lim, lim)
	ax.set_aspect('equal')
	plt.show()


#----------------------------------------------------------------------------#


sunLong, avgLong = loadData()

#testSunLong = [0.88226, -1.14959, -1.36839]
#testAvgLong = [0.212015, -0.63191, -1.08039]

a = 1
parameters = [0.2, math.pi/4]
boundT = ((0.00001, None), (0.0, (2 * math.pi)))
minT = minimize(computeCost, parameters, args=(a, sunLong, avgLong), 
				bounds=boundT, method='L-BFGS-B')
print minT

optParam = minT.x
plotResults(optParam, a, sunLong, avgLong)

#----------------------------------------------------------------------------#