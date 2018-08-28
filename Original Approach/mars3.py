# E0 259: Data Analytics. Module 1: Mars Orbit. Question 3.
# Pulkit Singh, July 20 2018

# importing required modules
import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.patches import Ellipse

# importing file containing required values calculated in other modules
import cfg

# importing custom module to run gradient descent on elliptical mars orbit
import ellipseGradientDescent 

#-------------------------------------------------------------------------------#

# Part 1: Finding 5 different locations of Mars on it's orbital plane.

# retrieving x-y coordinates of mars computed in Part 1
xMars, yMars = cfg.xMars, cfg.yMars 

# x-y coordinates of Mars will be the same as the projections
# to calculate z coordinates, we must use the formula as follows:
# zMars = (-a * xMars) + (-b * yMars), where a and b are the parameters
# of the best-fit plane calculated in Part 2.
zMars = []
for i in range(len(xMars)):
	zMars.append((-1 * cfg.a * xMars[i]) + (-1 * cfg.b * yMars[i]))

print("\nCalculating 5 different locations of Mars on it's orbital plane.\n")

#-------------------------------------------------------------------------------#

# Part 2: Finding the best fit circle on Mars's orbital plane


# Finding the distance of each point from the origin
rMars = []
for i in range(len(xMars)):
	sqDist = math.pow(xMars[i], 2) + math.pow(yMars[i], 2) + math.pow(zMars[i], 2)
	rMars.append(math.sqrt(sqDist))

# Finding the average radius, which is the radius of the best fit circle
r = sum(rMars) / len(rMars)

# Computing the sum of losses
loss = 0.0 
for radius in rMars:
	loss = loss + math.pow((r - radius), 2)

print("Finding the best fit circle on the orbital plane.")
print "Radius of circle", r
print "Sum of losses =", loss
print


#-------------------------------------------------------------------------------#

# Part 3: Finding the best fit ellipse on Mars's orbital plane

# initialising parameters for x-y coordinates of focus and length of major axis
xf1, yf1, axis1 = 0.0, 0.0, 0.0

# finding the best fit ellipse
xf, yf, axis, cost = ellipseGradientDescent.findEllipse(xMars, yMars, xf1, yf1, axis1)

print "Finding best fit ellipse on the orbital plane:"
print "Running gradient to find coordinates of second focus and length of major axis."
print "x-coordinate of focus:", xf
print "y-coordinate of focus:", yf 
print "Length of Major Axis:", axis
print "Length of Semi-Major Axis", axis/2.0



# calculating distance between focii
interFocii = math.sqrt(math.pow(xf, 2) + math.pow(yf, 2))
print "Distance between Focii:", interFocii


# calculating values to plot ellipse
centerX = xf / 2.0
centerY = yf / 2.0
minorAxis = math.sqrt(math.pow(axis, 2) - math.pow(interFocii, 2))
rotationAngle = 360 - math.degrees(math.atan(yf / abs(xf)))

# plotting cost as a function of number of iterations 
#plt.plot(cost)
#plt.show()

# creating a plot
fig, ax = plt.subplots()

# plotting mars locations and the focii
ax.plot(xMars, yMars, "ro")
ax.plot(xf, yf, "yo")
ax.plot(0.0, 0.0, "yo")

# adding best fit circle
fit_c = plt.Circle((0,0), r, color='c', fill=False)
ax.add_artist(fit_c)

# adding best fit ellipse
fit_e = Ellipse((centerX, centerY), axis, minorAxis, rotationAngle, color='b', fill=False)
ax.add_artist(fit_e)

# setting dimensions of the plot
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)
ax.set_aspect('equal')

# updating legend 
ax.legend([fit_c, fit_e], ['Best-fit Circle', 'Best-fit Ellipse'], fontsize='x-small')

plt.show()


#-------------------------------------------------------------------------------#












