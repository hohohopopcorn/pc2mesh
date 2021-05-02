import matplotlib.pyplot as plt
from johnvm.poisson import Octree, Oriented_Point, Oriented_Points, Point,  solve_for_x, indicator, fo
from johnvm.util_vis import show_Oriented_Points, show_octree, show_octree_leaf
import numpy as np


# Define the points
pts = Oriented_Points()  # initialize collector of points

pts.add(Oriented_Point(+0.50, +0.50, +0.50,
                       +1.0/np.sqrt(3), +1.0/np.sqrt(3), 0.00))
pts.add(Oriented_Point(-0.50, +0.50, +0.50,
                       -1.0/np.sqrt(3), +1.0/np.sqrt(3), 0.00))
pts.add(Oriented_Point(-0.50, -0.50, +0.50,
                       -1.0/np.sqrt(3), -1.0/np.sqrt(3), 0.00))
pts.add(Oriented_Point(+0.50, -0.50, +0.50,
                       +1.0/np.sqrt(3), -1.0/np.sqrt(3), 0.00))
pts.add(Oriented_Point(+0.50, +0.50, -0.50,
                       +1.0/np.sqrt(3), +1.0/np.sqrt(3), 0.00))
pts.add(Oriented_Point(-0.50, +0.50, -0.50,
                       -1.0/np.sqrt(3), +1.0/np.sqrt(3), 0.00))
pts.add(Oriented_Point(-0.50, -0.50, -0.50,
                       -1.0/np.sqrt(3), -1.0/np.sqrt(3), 0.00))
pts.add(Oriented_Point(+0.50,-0.50,-0.50,
                       +1.0/np.sqrt(3), -1.0/np.sqrt(3), 0.00))

octree = Octree(pts, 1)

show_octree(octree)

x_vector = solve_for_x(octree.leaf_nodes)


def my_fun(x, y):
    return indicator(x, y, 0.50, x_vector, octree.leaf_nodes)


xlist = np.linspace(-1.0, 1.0, 100)
ylist = np.linspace(-1.0, 1.0, 100)
X, Y = np.meshgrid(xlist, ylist)

from tqdm import tqdm
Z = np.full((len(xlist), len(ylist)), 0.00)
for i, x in enumerate(tqdm(xlist)):
    for j, y in enumerate(ylist):
        Z[i,j] = my_fun(x,y)

from matplotlib import cm
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
fig.show()

