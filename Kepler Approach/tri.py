""" This module triangulates the projections of Mars on the ecliptic plane,
and finds the radius and optimal-center of the best-fit circle. The sun is 
at the origin, but is not asssumed to be the center of the circle. The 
optimal center is placed on the line of apsides, which was calculated in 
the orbit-kepler module.

"""

#---------------------------------------------------------------------------#

import csv
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

#---------------------------------------------------------------------------#

# Using exercise #1 methodology to find projections of mars on the ecliptic
# plane. Sun is assumed to be placed at the origin, but it is not the center
# of the mars orbit
def findProjections():
	tri = "triangulation.csv"

	fields = []
	earthHelio = [] # heliocentric earth angles (in radians)
	marsGeo = []    # geocentric mars angles (in radians)

	# reading in triangulation csv file
	with open(tri, 'r') as trifile:
		triangulation = csv.reader(trifile)

		fields = triangulation.next()

		# Creating list of helio-earth and geo-mars angles (in radians)
		for row in triangulation:
			earthHelio.append(math.radians(float(row[4]) + (float(row[5])/60)))
			marsGeo.append(math.radians(float(row[6]) + (float(row[7])/60)))


	# calculating coordinates of earth
	xEarth = []     # x-coordinates of earth, xEarth = r * cos(earthHelio)
	yEarth = []     # y-coordinates of earth, yEarth = r * sin(earthHelio)

	for angle in earthHelio:
		xEarth.append(math.cos(angle))
		yEarth.append(math.sin(angle))


	# calculating coordinates of mars
	xMars = []      # x-coordinates of mars
	yMars = []      # y-coordinates of mars

	# for each paired obervation:
	#   * (x1, y1) and (x2, y2) are the two positions of earth
	#   * a1 and a2 are the two geocentric angles to mars respectively
	#   * (mx, my) is the location of mars (to be found)

	for i in range(5):
		x1 = xEarth[(2 * i)]        # first position of earth + mars angle
		y1 = yEarth[(2 * i)]
		a1 = marsGeo[(2 * i)]

		x2 = xEarth[(2 * i) + 1]    # second position of earth + mars angle
		y2 = yEarth[(2 * i) + 1]
		a2 = marsGeo[(2 * i) + 1]

		# trignometrically finding mars coordinates from paired observations
		mx = (y2 - y1 + (x1 * math.tan(a1)) - (x2 * math.tan(a2))) / (math.tan(a1) - math.tan(a2))
		my = (x2 - x1 + (y1 * (1 / math.tan(a1))) - (y2 * (1 / math.tan(a2)))) / ((1 / math.tan(a1)) - (1 / math.tan(a2)))

		xMars.append(mx)
		yMars.append(my)

	return xMars, yMars

# Finds the euclidian distance between Point2 (x2, y2) & Point1 (x1, y1)
def findDistance(x1, y1, x2, y2):
	xdiff = math.pow((x2 - x1), 2)
	ydiff = math.pow((y2 - y1), 2)
	return math.sqrt(xdiff + ydiff)

# Takes distance between sun and center of orbit and the projections of 
# Mars on the ecliptic plane. Returns the distance of each Mars projection 
# from the center.
def computeCoordinates(d, xMars, yMars):
	# angle of the line of apisodes (found previously)
	theta = 2.59152679

	# Finding the x-y coordinates of the center of the orbit
	dx = d * math.cos(theta)
	dy = d * math.sin(theta)

	# Finding the distance of each calculated projection 
	rMars = []
	for i in range(len(xMars)):
		rMars.append(findDistance(xMars[i], yMars[i], dx, dy))

	return rMars

# Takes distance between sun and center of orbit and the projections of 
# Mars on the ecliptic plane. Returns the mean square error of the best-fit
# circle on the plane.
def computeCost(d, xMars, yMars):

	# Finding distance of each projection from center
	rMars = computeCoordinates(d, xMars, yMars)

	# Finding the best-fit radius
	radius = sum(rMars) / len(rMars)

	# Computing the sum of losses for best-fit circle
	loss = 0.0 
	for r in rMars:
		loss = loss + math.pow((r - radius), 2)

	return loss / len(rMars)

# Finds distance between sun and center by minimizing cost of fitting a circle
# for the found projections of Mars
def minimizeDistance(d, xMars, yMars):
	minD = minimize(computeCost, d, args=(xMars, yMars), method='L-BFGS-B')
	return minD


# Takes optimal distance between sun and center of orbit and the projections 
# of Mars on the ecliptic plane. Plots resulting configuration.
def plotResults(d, xMars, yMars):

	# angle of the line of apisodes (found previously)
	theta = 2.59152679

	# finding coordinates of optimal center
	dx = d * math.cos(theta)
	dy = d * math.sin(theta)

	# creating a plot
	fig, ax = plt.subplots()

	# plotting line of asides
	x = np.arange(-1.8, 2, 0.1)
	y = x * math.tan(theta)
	ax.plot(x, y, 'y--', label='Line of Apsides')

	# plotting projections of mars and positions of sun and center
	ax.plot(xMars, yMars, 'ro', label='Mars Projections')
	ax.plot(dx, dy, 'go', label='Optimal Center')
	ax.plot(0, 0, 'yo', label='Sun')

	# finding and plotting radius of best fit circle
	rMars = computeCoordinates(d, xMars, yMars)
	r = sum(rMars)/len(rMars)
	print 'Radius of circle =', r
	fit = plt.Circle((dx,dy), r, color='g', fill=False)
	ax.add_artist(fit)

	# adding legend, text for graph
	ax.legend(fontsize='x-small')
	s = "Best-fit radius = " + str(round(r, 4))
	ax.text(0.75, -2.1, s, fontsize=7)
	

	# setting properties of figure, displaying it.
	lim = r + 0.7
	ax.set_xlim(-lim, lim)
	ax.set_ylim(-lim, lim)
	ax.set_aspect('equal')
	plt.show()




#---------------------------------------------------------------------------#



# Finding the projections of mars on the ec
xMars, yMars = findProjections()

# Finding the distance between the sun and the center of the Mars Orbit on
# the line of apisodes that minimizes the mean square error in the best-fit
# circle
minD = minimizeDistance(0.3, xMars, yMars)
print minD

# Plotting projections with the optimal positions of sun and center
plotResults(minD.x, xMars, yMars)



#---------------------------------------------------------------------------#