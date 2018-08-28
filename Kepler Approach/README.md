## Mars Orbit Calculation: Kepler's approach

This directory contains code to calculate the Mars Orbit with an approach more in line with Kepler's original calculation. 

### Approach Summary

The approach in this section relies on the following model:
- Mars has a circular orbit
- The Sun is at the origin, but this is not necessarily the center of the orbit.
- There is a point inside the orbit where Mars has uniform angular velocity, and this point is called the average sun.
- The line joining the sun and the average sun is called the line of apsides.

### Outline of Materials

- orbitkepler.py : This module fits an orbit for Mars by finding the optimal relative position of the average sun and the angle of the line of apsides. This is done using opposition data. However, these findings are in arbitrary units, and must be scaled appropriately to find the best-estimated model. 

- tri.py : This module triangulates the projections of Mars on the ecliptic plane (from the triangulation data), and finds the radius and optimal-center of the best-fit circle, using the angle of the line of apsides calculated in the orbitkepler module.

- scale.py : This module integrates the results of the orbitkepler and tri modules, by
scaling the model found in orbit-kepler by the results of tri.