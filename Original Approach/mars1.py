# E0 259: Data Analytics. Module 1: Mars Orbit. Question 1.
# Pulkit Singh, July 13 2018

# importing required modules
import csv
import math
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------#

# Part 1: Mars' Location on Ecliptic Plane

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

print("Finding projections of Mars on the Ecliptic Plane.")
print xMars
print
print yMars

#-------------------------------------------------------------------------------#

# Part 2: Finding Best Fit Circle of Mars Orbit

# finding distances from origin for each mars location
rMars = []
for i in range (5):
	sqDist = math.pow(xMars[i], 2) + math.pow(yMars[i], 2)
	rMars.append(math.sqrt(sqDist))

# to find best fit line, we must minimize square euclidian distance
# differentiating this function, and setting to 0, we get radius r
# we find r = 1/5(r1 + r2 ... + r5)
r = sum(rMars) / len(rMars)
print("Calculating radius of best fit circle for found projections.")
print "Radius of circle =", r

#-------------------------------------------------------------------------------#

# Part 3: Graphing positions of Mars and best fit circle on the eclipic plane

# creating a plot
fig, ax = plt.subplots()

# plotting the sun at the origin
ax.plot(0, 0, 'yo', markersize=12)

# plotting the projections of Mars on the ecliptic plane
ax.plot(xMars, yMars, 'ro', markersize=5, label="Mars's Projection")

# plotting best fit circle
fit = plt.Circle((0,0), r, color='g', fill=False)
ax.add_artist(fit)

# setting dimensions of the plot
ax.set_xlim(-2.2, 2.2)
ax.set_ylim(-2.2, 2.2)
ax.set_aspect('equal')
ax.legend(fontsize='x-small')
s = "Best-fit radius = " + str(round(r, 4))
ax.text(0.75, -2, s, fontsize=7)

# function to show the plot
plt.show()

#-------------------------------------------------------------------------------#






