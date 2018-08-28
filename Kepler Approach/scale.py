""" This module integrates the results of the orbitkepler and tri modules, by
scaling the model found in orbit-kepler by the results of tri. Thus, it finds
the averagSun - Sun - Mars model in relevant units (AU).

"""


# importing necessary modules
import csv
import math
import matplotlib.pyplot as plt
import numpy as np 
from scipy.optimize import minimize
from matplotlib.patches import Ellipse
import ellipseGradientDescent

# importing the orbit model functions
import orbitkepler as orbit
import tri

# Takes parameters of model, scale parameter, and longitudes as input, returns
# the radius of the best-fit circle.
def computeRadius(a, parameters, sunLong, avgLong):
	xMars, yMars, rMars = orbit.computeCoordinates(parameters, a, 
												   sunLong, avgLong)
	return sum(rMars)/len(rMars)

# Computes the error between radius from model and radius found from analysis
# of the triangulation data
def computeCost(a, parameters, sunLong, avgLong):
	
	triRad = 1.53350526978
	foundRad = computeRadius(a, parameters, sunLong, avgLong)

	error = math.pow((triRad - foundRad), 2)
	return error

#----------------------------------------------------------------------------#

# Plotting positions of mars found from both opposition 
def plotBoth(a, parameters, sunLong, avgLong):

	# finding positions of mars from opposition data
	xMars, yMars, rMars = orbit.computeCoordinates(parameters, a, 
												   sunLong, avgLong)

	# finding positions of mars from triangulation data
	triX, triY = tri.findProjections()

	t = parameters[0]
	theta = parameters[1]
	sin_t = math.sin(theta)
	cos_t = math.cos(theta)


	# finding radius of best fit circle
	r = sum(rMars)/len(rMars)
	print 'Radius =', r

	fig, ax = plt.subplots()
	
	# plotting line of asides
	x = np.arange(-1.8, 2, 0.1)
	y = x * math.tan(theta)
	ax.plot(x, y, 'y--', label='Line of Apsides')

	# plotting positions of mars from opposition data
	ax.plot(xMars, yMars, 'ro', label='Mars (opposition data)')

	# plotting positions of mars from triangulation data
	ax.plot(triX, triY, 'bo', label = 'Mars (triangulation data)')

	ax.plot(a * cos_t, a * sin_t, 'go')            # plotting average sun
	ax.plot(-1 * t * cos_t, -1 * t * sin_t, 'yo')  # plotting sun

	# adding best fit circle
	fit = plt.Circle((0,0), r, color='g', fill=False) 
	ax.add_artist(fit)

	# adding legend, text for graph
	ax.legend(fontsize='x-small')
	s = "Best-fit radius = " + str(round(r, 4))
	ax.text(0.75, -2.1, s, fontsize=7)

	lim = r * 1.5
	ax.set_xlim(-lim, lim)
	ax.set_ylim(-lim, lim)
	ax.set_aspect('equal')
	plt.show()

#----------------------------------------------------------------------------#

# running regression to find the appropriate scale parameter
sunLong, avgLong = orbit.loadData()
a = 0.2
parameters = [1.00000000e-05, 2.59152679e+00]
minA = minimize(computeCost, a, args=(parameters, sunLong, avgLong), 
	method='L-BFGS-B')
print minA

plotBoth(minA.x, parameters, sunLong, avgLong)

#----------------------------------------------------------------------------#