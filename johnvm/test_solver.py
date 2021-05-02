import matplotlib.pyplot as plt
from johnvm.poisson import Octree, Oriented_Point, Oriented_Points, Point,  solve_for_x, indicator, fo
from johnvm.util_vis import show_Oriented_Points, show_octree, show_octree_leaf
import numpy as np


np.random.seed(42)

# import time
# tic = time.perf_counter()
# toc = time.perf_counter()
# print(f"Execution time: {toc - tic:0.4f} seconds")

# I1oop(-1.0, 1.0, 1.0, 2.0, -2.0, -1.0, 1.0,
#       2.0, 4.0, 1.0, 5.0, 1.0, 5.0, 7.0, 9.0)
# should return -1572.166666666666666666

# domain(2.0, 4.0, 3.0, 2.0)
# should return (2.0, 4.0)

# domain(2.0, 4.0, 6.0, 2.0)
# should return (5.0, 4.0)


# B(3, 2, 11, 1, 2, 1, 2)
# should return 203.5
# B(8, 1, 2, 4, 3, 6, 5)
# should return -4.16


def test_generate_sphere(n_pts=1000):
    """
    Generate oriented points sampled from a sphere
    centered at (0,0,0) with radius 1
    """
    pts = Oriented_Points()  # initialize collector of points
    # use numpy to sample points on a sphere
    point_matrix = np.random.normal(size=(n_pts, 3))
    for i in range(n_pts):
        pt_data = point_matrix[i, :] / \
            np.linalg.norm(point_matrix[i, :])  # normalize
        # add in the point list
        pts.add(Oriented_Point(pt_data[0], pt_data[1], pt_data[2],
                               pt_data[0], pt_data[1], pt_data[2]))
    return pts


pts = test_generate_sphere(2000)
octree = Octree(pts, 4)

x_vector = solve_for_x(octree.leaf_nodes)


def my_fun(x, y):
    return indicator(x, y, 0.00, x_vector, octree.leaf_nodes)


xlist = np.linspace(-1.0, 0.0, 100)
ylist = np.linspace(0.0, 1.0, 100)
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

