import numpy as np
from poisson import Point, Points


def test_generate_sphere(n_pts=1000):
    """
    Generate oriented points sampled from a sphere
    centered at (0,0,0) with radius 1
    """
    pts = Points()  # initialize collector of points
    # use numpy to sample points on a sphere
    point_matrix = np.random.normal(size=(n_pts, 3))
    for i in range(n_pts):
        pt_data = point_matrix[i, :] / \
            np.linalg.norm(point_matrix[i, :])  # normalize
        # add in the point list
        pts.add(Point(pt_data[0], pt_data[1], pt_data[2],
                pt_data[0], pt_data[1], pt_data[2]))
    return pts


pts = test_generate_sphere()

# pts.show()
# pts.to_npts_file("lala")
