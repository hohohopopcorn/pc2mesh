import numpy as np
from dataclasses import dataclass, field
from typing import List
from tqdm import tqdm
from numba import jit
# from functools import total_ordering


EPSILON = 1.00e-8  # a small number
ALPHA = 1.00e24    # a very large number


@dataclass
class Point:
    """
    Point object.
    """
    # Location
    x: float = field(default=0.00)
    y: float = field(default=0.00)
    z: float = field(default=0.00)

    def __eq__(self, other):
        return (self.x == other.x and
                self.y == other.y and
                self.z == other.z)

    def __add__(self, other):
        """
        add points with "+".
        """
        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return(Point(x, y, z))

    def __mul__(self, c: float):
        """
        multiply with a scalar using "*".
        """
        x = self.x * c
        y = self.y * c
        z = self.z * c
        return(Point(x, y, z))


@dataclass
class Oriented_Point(Point):
    """
    Oriented point.
    """

    # Normal
    nx: float = field(default=0.00)
    ny: float = field(default=0.00)
    nz: float = field(default=0.00)


@dataclass
class Oriented_Points:
    """
    Collector for unique oriented points.
    """
    points: List[Oriented_Point] = field(default_factory=list)

    def add(self, pt: Oriented_Point):
        """
        Add a point in the list of points,
        if it is not already in
        """
        if pt not in self.points:
            self.points.append(pt)
        else:
            raise ValueError('Oriented point already exists: '
                             + repr(pt))

    def bbox_center(self):
        """
        Compute the center of the bouding box
        """
        xs = [pt.x for pt in self.points]
        ys = [pt.y for pt in self.points]
        zs = [pt.z for pt in self.points]
        dX = (max(xs) + min(xs)) / 2.00
        dY = (max(ys) + min(ys)) / 2.00
        dZ = (max(zs) + min(zs)) / 2.00
        center = Point(dX, dY, dZ)
        return center

    def bbox_dim(self):
        """
        Compute the dimensions of the bouding box
        """
        xs = [pt.x for pt in self.points]
        ys = [pt.y for pt in self.points]
        zs = [pt.z for pt in self.points]
        dX = max(xs) - min(xs) + 2.00 * EPSILON
        dY = max(ys) - min(ys) + 2.00 * EPSILON
        dZ = max(zs) - min(zs) + 2.00 * EPSILON
        return (dX, dY, dZ)

    def split_along_plane(self,
                          center: Point,
                          plane: str):
        group1 = Oriented_Points()
        group2 = Oriented_Points()
        if plane == "xy":
            for pt in self.points:
                if pt.z < center.z:
                    group1.add(pt)
                else:
                    group2.add(pt)
        elif plane == "xz":
            for pt in self.points:
                if pt.y < center.y:
                    group1.add(pt)
                else:
                    group2.add(pt)
        elif plane == "yz":
            for pt in self.points:
                if pt.x < center.x:
                    group1.add(pt)
                else:
                    group2.add(pt)
        return (group1, group2)

    def to_npts_file(self, file_name):
        """
        Generates a point cloud file. The file is space delimited,
        each row is one point, columns are the components of the
        point's location and normal.
        file_name: name of the file *without the extension*
        """
        point_matrix = np.full((len(self.points), 6), 0.00)
        for i, pt in enumerate(self.points):
            point_matrix[i, :] = np.array(
                [pt.x, pt.y, pt.z, pt.nx, pt.ny, pt.nz]
            )
        np.savetxt(file_name+'.npts', point_matrix, delimiter=' ')

    def __repr__(self):
        return str(len(self.points)) + " points."


##########
# OCTREE #
##########


@dataclass
class Node:
    """
    Octree node.
    """
    depth: int

    # is it a leaf node?
    leaf: bool

    # center of the node
    center: Point
    # width of the cube
    width: float

    # oriented points contained in the node
    contents: Oriented_Points

    # association with other nodes
    parent: 'Node'
    children: List['Node'] = field(default_factory=list)

    def subdivide(self, max_depth):
        """
        Subdivide `depth` times
        """
        pts = self.contents
        # If the node contains any points
        if pts.points:
            # Must subdivide.
            # Make children:
            self.contents = None
            self.leaf = False
            # compute lower-left-front corner
            # (to obtain child centerpoints more easily)
            dlf_point = self.center + Point(*[-self.width/2]*3)
            # Splitting the containing oriented points
            # split along yz (into top-bottom quadrants)
            down_up = pts.split_along_plane(
                self.center, 'xy')
            for z, du in enumerate(down_up):
                # and then along zx (into front-back pairs)
                front_back = du.split_along_plane(
                    self.center, 'xz')
                for y, fb in enumerate(front_back):
                    # and then along xy (into left and right cube)
                    left_right = fb.split_along_plane(
                        self.center, 'yz')
                    for x, lr in enumerate(left_right):
                        # compute initialization parameters
                        # and instantiate new leaf nodes
                        child_depth = self.depth + 1
                        child_width = self.width/2.00
                        child_center = dlf_point + Point(
                            x * child_width + child_width/2.00,
                            y * child_width + child_width/2.00,
                            z * child_width + child_width/2.00
                        )
                        child_node = Node(
                            child_depth,
                            True,
                            child_center,
                            child_width,
                            lr,
                            self
                        )
                        self.children.append(child_node)
                        # recursively subdivide:
                        if child_depth < max_depth:
                            child_node.subdivide(max_depth)

    def leaf_nodes(self, d):
        """
        Return all leaf nodes *of depth d* connected to this parent node
        (directly or further down the tree)
        that contain at least one sample
        """
        node = self  # start here
        leaves = []  # instantiate an empty array
        if node.leaf and node.depth == d:  # if it's already a leaf
            if node.contents.points:  # if list of points is nonempty
                leaves.append(self)
        else:
            # it's not a leaf. go down recursively and check the children
            for child in self.children:
                for leaf in child.leaf_nodes(d):
                    leaves.append(leaf)
        # at this point we have collected all the leaves
        return leaves

    def __repr__(self):
        return str(id(self))


@dataclass
class Octree:
    """
    Octree spatial partition.
    Parameters:
        Points (Points): Points object
        depth (int): Maximum depth of the tree
    Returns:
        Octree object
    """
    points: Oriented_Points
    depth: int
    head: Node = field(init=False)
    leaf_nodes: List[Node] = field(default_factory=list)

    def __post_init__(self):
        # instantiate the head node
        self.head = Node(
            0,
            True,
            self.points.bbox_center(),
            max(self.points.bbox_dim()),
            self.points,
            None
        )
        # subdivide `depth` times
        self.head.subdivide(self.depth)
        self.leaf_nodes = self.head.leaf_nodes(self.depth)


"""
Functions used to populate vector v and matrix L, solve the system
and give access to the indicator function
"""


@jit(nopython=True)
def A(x, y, z, ocx, ocy, ocz, ocpx, ocpy, ocpz, snx, sny, snz):
    """
    Low-level function. Used in `I1oop`.
    Result of definite integral for the computation of the components
    of vector v.
    [Debug note: Output matches Mathematica -> OK]
    """
    return -(1.0/24.0)*x*y*z*(
        + 12. * (-2.0 + ocx**2 + ocy**2 + ocz**2) *
        (ocpx*snx + ocpy*sny + ocpz*snz)
        - 6.0 * ((-2.0 + 2.0 * ocpx * ocx + ocx**2 + ocy**2 + ocz**2)
                 * snx + 2.0 * ocx * (ocpy * sny + ocpz * snz)) * x
        + 4.0 * (ocpx*snx + 2.0 * ocx*snx + ocpy *
                 sny + ocpz*snz) * x**2 - 3.0 * snx * x**3
        - 6.0 * (2.0 * ocpx * ocy * snx + (-2.0 + ocx**2 + 2.0 * ocpy *
                                           ocy + ocy**2 + ocz**2) * sny
                 + 2.0 * ocpz * ocy * snz) * y
        + 6.0 * (ocy*snx + ocx*sny)*x*y
        - 2.0 * sny*x**2*y + 4.0*(
            ocpx*snx + ocpy*sny + 2.0 * ocy * sny + ocpz*snz) * y**2
        - 2.0 * snx*x*y**2 - 3.0*sny*y**3
        - 6.0 * (2.0*ocpx*ocz*snx + 2.0*ocpy*ocz*sny +
                 (-2.0 + ocx**2 + ocy**2 + 2*ocpz*ocz + ocz**2)*snz)*z
        + 6.0 * (ocz*snx + ocx*snz)*x*z - 2.0*snz*x**2*z +
        6.0*(ocz*sny + ocy*snz)*y*z - 2.0*snz*y**2*z
        + 4.0 * (ocpx*snx + ocpy*sny + (ocpz + 2.0 * ocz)*snz) *
        z**2 - 2.0*snx*x*z**2 - 2.0*sny*y*z**2 - 3.0*snz*z**3
    )


@jit(nopython=True)
def I1oop(xmin, xmax, ymin, ymax, zmin, zmax,
          ocx, ocy, ocz, ocpx, ocpy, ocpz, snx, sny, snz):
    """
    Evaluates the definite integral given a domain.
    [Debug note: Output matches Mathematica. Integration also
    verified numerically  using A directly
    instead of substituting to the
    indefinite integral function -> OK]
    """
    return A(xmax, ymax, zmax,
             ocx, ocy, ocz, ocpx, ocpy, ocpz, snx, sny, snz) \
        - A(xmax, ymax, zmin,
            ocx, ocy, ocz, ocpx, ocpy, ocpz, snx, sny, snz) \
        - A(xmax, ymin, zmax,
            ocx, ocy, ocz, ocpx, ocpy, ocpz, snx, sny, snz) \
        + A(xmax, ymin, zmin,
            ocx, ocy, ocz, ocpx, ocpy, ocpz, snx, sny, snz) \
        - A(xmin, ymax, zmax,
            ocx, ocy, ocz, ocpx, ocpy, ocpz, snx, sny, snz) \
        + A(xmin, ymax, zmin,
            ocx, ocy, ocz, ocpx, ocpy, ocpz, snx, sny, snz) \
        + A(xmin, ymin, zmax,
            ocx, ocy, ocz, ocpx, ocpy, ocpz, snx, sny, snz) \
        - A(xmin, ymin, zmin,
            ocx, ocy, ocz, ocpx, ocpy, ocpz, snx, sny, snz) \



@jit(nopython=True)
def domain(oc, ow, ocp, owp):
    """
    Used to obtain the domain of integration.
    It is called once per coordinate.
    """
    minimum = max(oc-ow/2.0, ocp-owp/2)
    maximum = min(oc+ow/2.0, ocp+owp/2)
    return (minimum, maximum)


def v(leaf_nodes: List[Node]):
    """
    Computes and returns the vector `v`
    """
    v_vec = np.full(len(leaf_nodes), 0.00)
    for i, o in enumerate(tqdm(leaf_nodes)):
        value = 0.00  # initialize
        for op in leaf_nodes:
            if not op.contents:  # if the considered leaf is empty, skip
                break
            # it's not empty!
            aoop = 1/(o.width**3)*1/(op.width**5) * np.power(2*np.pi, -3.00)
            # note: If all nodes have the same depth and width,
            # this will always be the same...
            xmin, xmax = domain(o.center.x, o.width, op.center.x, op.width)
            ymin, ymax = domain(o.center.y, o.width, op.center.y, op.width)
            zmin, zmax = domain(o.center.z, o.width, op.center.z, op.width)
            # check for nonempty integration domain
            exists = (xmin < xmax and ymin < ymax and zmin < zmax)
            if exists:
                # add the contribution of each sample
                # `s` that's inside leaf `op`
                for s in op.contents.points:
                    value += aoop * \
                        I1oop(xmin, xmax, ymin, ymax, zmin, zmax,
                              o.center.x, o.center.y, o.center.z,
                              op.center.x, op.center.y, op.center.z,
                              s.nx, s.ny, s.nz)
        v_vec[i] = value
    return v_vec


@jit(nopython=True)
def B(x, y, z, ocpx, ocpy, ocpz, ow):
    """
    Low-level function. Used in `I2oop`.
    Result of definite integral for the computation of the components
    of matrix L.
    [Debug note: Output matches Mathematica -> OK]
    """
    return 1.0/(6.0 * ow**2) * (x*y*z) * \
        (
            + x**2 + y**2 + z**2
            - 3.0 * (
                + ocpx * x
                + ocpy * y
                + ocpz * z
            )
            + 3.0 * (ocpx**2 + ocpy**2 + ocpz**2)
            - 6.0 * ow**2
    )


@jit(nopython=True)
def I2oop(xmin, xmax, ymin, ymax, zmin, zmax,
          ocpx, ocpy, ocpz, ow):
    """
    Evaluates the definite integral given a domain.
    [Debug note: Output matches Mathematica -> OK]
    """
    return B(xmax, ymax, zmax, ocpx, ocpy, ocpz, ow) \
        - B(xmax, ymax, zmin, ocpx, ocpy, ocpz, ow) \
        - B(xmax, ymin, zmax, ocpx, ocpy, ocpz, ow) \
        + B(xmax, ymin, zmin, ocpx, ocpy, ocpz, ow) \
        - B(xmin, ymax, zmax, ocpx, ocpy, ocpz, ow) \
        + B(xmin, ymax, zmin, ocpx, ocpy, ocpz, ow) \
        + B(xmin, ymin, zmax, ocpx, ocpy, ocpz, ow) \
        - B(xmin, ymin, zmin, ocpx, ocpy, ocpz, ow) \



def L(leaf_nodes: List[Node]):
    """
    Computes and returns the matrix `L`
    """
    L_mat = np.full((len(leaf_nodes), len(leaf_nodes)), 0.00)  # initialize
    for i, o in enumerate(tqdm(leaf_nodes)):
        # for j in range(i, len(leaf_nodes)):
        for j in range(len(leaf_nodes)):
            op = leaf_nodes[j]
            value = 0.00  # initialize
            # I AM HERE
            aoop = 1/(o.width**5)*1/(op.width**3) * \
                np.power(2*np.pi, -3.00)
            xmin, xmax = domain(o.center.x, o.width, op.center.x, op.width)
            ymin, ymax = domain(o.center.y, o.width, op.center.y, op.width)
            zmin, zmax = domain(o.center.z, o.width, op.center.z, op.width)
            # check for nonempty integration domain
            exists = (xmin < xmax and ymin < ymax and zmin < zmax)
            if exists:
                value += 3.00 * aoop * \
                    I2oop(xmin, xmax, ymin, ymax, zmin, zmax,
                          op.center.x, op.center.y, op.center.z, op.width)
            L_mat[i, j] = value
            # if i > j:
            #     L_mat[j, i] = value
    return L_mat


def solve_for_x(leaf_nodes: List[Node]):
    """
    Solves the system of equations to obtain
    the vector x
    """
    L_mat = L(leaf_nodes)
    v_vec = v(leaf_nodes)
    x_vec = np.linalg.solve(L_mat, v_vec)
    return x_vec


def fo(x, y, z, w, cx, cy, cz):
    """
    Evaluates a node's basis function at a given point
    """
    q = np.array([x, y, z])
    c = np.array([cx, cy, cz])
    ok = np.abs(x-cx) < w/2.0 and np.abs(y-cy) < w/2.0 and np.abs(z-cz) < w/2.0
    if ok:
        return np.power(2.0*np.pi, -3.0/2.0) \
            * (1.00/w**3) * (
                1.00 - 1.0/2.0 * 1.0/w**2 * np.dot((q-c), (q-c))
        )
    else:
        return 0.0


def indicator(x, y, z, x_vec, leaf_nodes: List[Node]):
    """
    Evaluates the indicator function at a given point
    """
    value = 0.00  # initialize
    for i, o in enumerate(leaf_nodes):
        value += x_vec[i] * fo(x, y, z, o.width,
                               o.center.x, o.center.y, o.center.z)
    return value


if __name__ == "__main__":
    pass
