""" This module runs gradient descent on the locations of Mars on it's 
	orbitalplane in order to find the best-fit elliptical orbit for Mars.
"""

# Developed by Pulkit Singh, Niheshkumar Rathod & Rajesh Sundaresan
# Copyright lies with the Robert Bosch Center for Cyber-Physical Systems,
# Indian Institute of Science, Bangalore, India.

#----------------------------------------------------------------------------#

import numpy as np
import math

#----------------------------------------------------------------------------#

def evaluateDistance(xMars, yMars, xFocus, yFocus, majorAxis):
	""" Computes the cost of fitting an ellipse with one focus at the sun,
		and the other at [xFocus, yFocus], given the locations of Mars and
		the length of the major axis.

		Cost is caculated using the following formula:
		(sum of distances from focii - length of major axis)^2

	Parameters:
		xMars  (float): list of x-coordinates of Mars locations
		yMars  (float): list of y-coordinates of Mars locations
		xFocus (float): x-coordinate of second focus
		yFocus (float): y-coordinate of second focus
		majorAxis (float): length of the major axis

	Returns:
		squareDist (float): cost of fitting the ellipse (sum of square
							distances)

	"""

	# Finding the distance of each point from the origin
	dist = []

	# calculating (distance to origin + distance to focus2 
	# - major axis length)^2 for each (x, y) pair
	for i in range(len(xMars)):
		distOrigin = math.sqrt(math.pow(xMars[i], 2) + math.pow(yMars[i], 2))
		distFocus = math.sqrt(math.pow((xMars[i] - xFocus), 2) 
			+ math.pow((yMars[i] - yFocus), 2))
		dist.append(math.pow((distOrigin + distFocus - majorAxis), 2))

	# adding up all the square distances
	squareDist = sum(dist)
	return squareDist

#----------------------------------------------------------------------------#

def computeGradient(xMars, yMars, xFocus, yFocus, majorAxis):
	""" Computes the gradient vector with respect to the x-y coordinates of
		the second focus andthe length of the major axis.

		gradient vector = [df/d(xFocus), df/d(yFocus), df/d(majorAxis)]

	Parameters:
		xMars  (float): list of x-coordinates of Mars locations
		yMars  (float): list of y-coordinates of Mars locations
		xFocus (float): x-coordinate of second focus
		yFocus (float): y-coordinate of second focus
		majorAxis (float): length of the major axis

	Returns:
		gradient (float list): list of required gradients

	"""

	dxFocus = []
	dyFocus = []
	dmajorAxis = []

	# df/d(xFocus) = (-2 * (xMars - xFocus) * evaluateDistance) / distFocus
	# df/d(yFocus) = (-2 * (yMars - yFocus) * evaluateDistance) / distFocus
	# df/d(majorAxis) = -2 * evaluateDistance

	# computing partial derivatives for each set of coordinates
	for i in range(len(xMars)):
		distOrigin = math.sqrt(math.pow(xMars[i], 2) + math.pow(yMars[i], 2))
		distFocus = math.sqrt(math.pow((xMars[i] - xFocus), 2) 
			+ math.pow((yMars[i] - yFocus), 2))
		dist = distOrigin + distFocus - majorAxis

		xDiff = xMars[i] - xFocus
		yDiff = yMars[i] - yFocus

		dxFocus.append((-2 * xDiff * dist) / distFocus)
		dyFocus.append((-2 * yDiff * dist) / distFocus)
		dmajorAxis.append(-2 * dist)

	# returning gradient vector
	gradient = [float(sum(dxFocus)), 
				float(sum(dyFocus)), 
				float(sum(dmajorAxis))]
	return gradient

#----------------------------------------------------------------------------#

# Takes x-y coordinate matrix of different Mars locations, x-y coordinates of
# the second focus and the length of the major axis as input, and runs 
# gradient descent to find the best fit ellipse. Returns the x-y coordinates 
# of the found focus, and the length of the major axis of the ellipse.
def findEllipse(xMars, yMars, xf, yf, axis):
	""" Finds the best-fit ellipse for the Mars Orbit using gradient 
		descent. Returns the x-y coordinates of the found focus and the
		length of the major axis.

	Parameters:
		xMars  (float): list of x-coordinates of Mars locations
		yMars  (float): list of y-coordinates of Mars locations
		xFocus (float): x-coordinate of second focus
		yFocus (float): y-coordinate of second focus
		majorAxis (float): length of the major axis

	Returns:
		xf (float): x-coordinate of the found focus
		yf (float): y-coordinate of the found focus
		axis (float): length of the major axis
		cost (float list): list of costs in each gradient descent	
							iteration.

	"""

	
	# initialising alpha as the step value
	alpha = 0.001

	# initialising array to keep track of cost values in gradient descent
	cost = []

	# running gradient descent
	for i in range (10000):	
		# finding cost for given parameters
		squareDist = evaluateDistance(xMars, yMars, xf, yf, axis)
		#print("square dist"), squareDist

		# adding current cost to list of previous costs
		cost.append(squareDist)

		# finding gradient with parameter values a & b
		delta = computeGradient(xMars, yMars, xf, yf, axis)

		# updating parameter values
		xf   = xf - (alpha * delta[0])
		yf   = yf - (alpha * delta[1])
		axis = axis - (alpha * delta[2])

	return xf, yf, axis, cost

#----------------------------------------------------------------------------#
