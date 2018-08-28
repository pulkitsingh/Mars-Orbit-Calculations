""" This module runs gradient descent on the locations of Mars on the 
	celestial Sphere, in order to find the best-fit Mars orbital Plane.
"""

# Developed by Pulkit Singh, Niheshkumar Rathod & Rajesh Sundaresan
# Copyright lies with the Robert Bosch Center for Cyber-Physical Systems,
# Indian Institute of Science, Bangalore, India.

#----------------------------------------------------------------------------#

import numpy as np
import math

#----------------------------------------------------------------------------#

def evaluateDistance(coordinates, a, b):
	""" Returns the cost of fitting a plane with parameters (a, b) to the
		coordinates of Mars on the celestial sphere. The plane has equation
		ax + by + z = 0

	Cost is the sum of squared euclidian distances.
	Therefore, cost = sum(((ax + by + z)/(a^2 + b^2 + 1))^2)

	Parameters:
		coordinates (float): x-y-z coordinates of Mars locations on the
							 celestial sphere.
		a (float): coefficient of x in plane equation
		b (float): coefficient of y in plane equation

	Returns:
		cost (float): sum of square euclidian distances

	"""

	# creating normal vector for plane
	normal = np.array([a, b, 1.0])[:,None]

	# calculating scale (a^2 + b^2 + 1)
	scale = math.pow(a, 2) + math.pow(b, 2) + 1.0

	# calculating distance = coordinate matrix * normal vector
	distance = np.dot(coordinates, normal) / scale

	# calculating and returning sum of square distances
	squareDist = float(sum(distance ** 2))
	return squareDist

#----------------------------------------------------------------------------#

def computeGradient(coordinates, a, b):
	""" Computes the gradient vector of the cost with respect to the 
		parameters of the plane.

	Parameters:
		coordinates (float): x-y-z coordinates of Mars locations on the
							 celestial sphere.
		a (float): coefficient of x in plane equation
		b (float): coefficient of y in plane equation

	Returns:
		gradient: [ d(cost)/da, d(cost)/db ]

	"""

	# creating normal vector for plane
	normal = np.array([a, b, 1.0])[:,None]

	# calculating scale (a^2 + b^2 + 1)
	scale = math.pow(a, 2) + math.pow(b, 2) + 1.0

	# linearSum = ax + by + z
	linearSum = np.dot(coordinates, normal)

	# calculating the partial derivatives with respect to a and b

	scaledX = np.array([coordinates[:, 0] * scale]).T  # scaled x-coordinates
	scaledY = np.array([coordinates[:, 1] * scale]).T  # scaled y-coordinates
	partialScale = (2 / (math.pow(scale, 3)))          # partial deriv scale

	# computing values of derivatives
	partialA = partialScale * ((-2 * a * linearSum) + scaledX) * linearSum
	partialB = partialScale * ((-2 * b * linearSum) + scaledY) * linearSum 

	# returning a gradient vector
	gradient = [float(sum(partialA)), float(sum(partialB))]
	return gradient

#----------------------------------------------------------------------------#

def findPlane(coordinates):
	""" Fits a plane to the coordinates of Mars on the celestial sphere,
		using gradient descent.

	Parameters:
		coordinates (float list): list of x-y-z coordinates of Mars on the
					celestial sphere.
		
	Returns:
		planeParameters (float list): coefficients (a,b) of x and y for a 
					plane with equation ax + by + z = 0

	"""
	
	# creating coordinate matrix: [x, y, z]
	coordinateMatrix = np.array(coordinates).T

	# initalizing guesses for plane parameters a and b to be 0.0
	a, b = 0.0, 0.0

	# initialising alpha as the step value
	alpha = 0.0001

	# initialising array to keep track of cost values in gradient descent
	cost = []

	# running gradient descent
	for i in range (10000):
		
		# finding cost for given parameter values a & b
		squareDist = evaluateDistance(coordinateMatrix, a, b)

		# adding current cost to list of previous costs
		cost.append(squareDist)
		
		# finding gradient with parameter values a & b
		delta = computeGradient(coordinateMatrix, a, b)
		
		# updating parameter values
		a = a - (alpha * delta[0])
		b = b - (alpha * delta[1])

	# Final parameters of the plane
	planeParams = [a, b]

	return planeParams

#----------------------------------------------------------------------------#
