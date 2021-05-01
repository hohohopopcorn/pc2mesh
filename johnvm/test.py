import matplotlib.pyplot as plt
from johnvm.poisson import Point, Oriented_Point, Oriented_Points, Octree, Node
from johnvm.util_vis import show_Oriented_Points, show_octree, show_octree_leaf
import numpy as np

import time
# os.chdir("./johnvm")


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


def test_generate_plane(n_pts=1000):
    """
    Generate oriented points sampled from some plane
    """
    pts = Oriented_Points()  # initialize collector of points
    point_matrix = np.random.uniform(size=(n_pts, 3))
    normal_vec = np.array([1.0, -1.0, 1.0])
    normal_vec = normal_vec/np.linalg.norm(normal_vec)
    for i in range(n_pts):
        point_matrix[i, :] -= np.dot(point_matrix[i, :],
                                     normal_vec) * normal_vec
        pts.add(Oriented_Point(point_matrix[i, 0],
                               point_matrix[i, 1],
                               point_matrix[i, 2],
                               1.0, -1.0, 1.0))
    return pts


pts = test_generate_plane(500)
octree = Octree(pts, 1)
show_octree(octree)


show_Oriented_Points(pts)
pts.to_npts_file("lala")

pts.centroid()
max(pts.bbox_dim())


def get_volume(pts, size):
    octree = Octree(pts, size)
    volume = 0.00
    for leaf in octree.leaf_nodes:
        if len(leaf.contents.points) > 0:
            volume += leaf.width**3
    return volume


def get_n_leaves(pts, size):
    octree = Octree(pts, size)
    n = 0
    for leaf in octree.leaf_nodes:
        if len(leaf.contents.points) > 0:
            n += 1
    return n


tic = time.perf_counter()


sizes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
# volumes = [get_volume(pts, size) for size in sizes]
leaves = [get_n_leaves(pts, size) for size in sizes]

toc = time.perf_counter()
print(f"Execution time: {toc - tic:0.4f} seconds")

plt.figure()
plt.plot(sizes, leaves)
plt.show()
