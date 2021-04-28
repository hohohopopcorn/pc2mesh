import numpy as np
from dataclasses import dataclass, field
from typing import List
import matplotlib.pyplot as plt
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

    def centroid(self):
        """
        Compute the centroid of the points
        """
        centroid = Point()
        for pt in self.points:
            centroid += pt
        centroid = centroid * (1.00/float(len(self.points)))
        return centroid

    def bbox_dim(self):
        """
        Compute the dimensions of the bouding box
        """
        xs = [pt.x for pt in self.points]
        ys = [pt.y for pt in self.points]
        zs = [pt.z for pt in self.points]
        dX = max(xs) - min(xs)
        dY = max(ys) - min(ys)
        dZ = max(zs) - min(zs)
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

    def show(self):
        """
        Show a 3D scatter polot of the points
        """
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')
        x_coords = []
        y_coords = []
        z_coords = []
        for pt in self.points:
            x_coords.append(pt.x)
            y_coords.append(pt.y)
            z_coords.append(pt.z)
        ax.scatter(x_coords, y_coords, z_coords)
        plt.show()

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

    def leaf_nodes(self):
        """
        Return all leaf nodes connected to this parent node
        (directly or further down the tree)
        """
        node = self  # start here
        leaves = []  # instantiate an empty array
        if node.leaf:  # if it's already a leaf
            leaves.append(self)
        else:
            # it's not a leaf. go down recursively and check the children
            for child in self.children:
                for leaf in child.leaf_nodes():
                    leaves.append(leaf)
        # at this point we have collected all the leaves
        return leaves

    def lines_to_plot(self):
        """
        (For plotting the cube)
        """
        return ([
            [[self.center.x - self.width/2.00,
                self.center.x + self.width/2.00],
             [self.center.y - self.width/2.00,
                self.center.y - self.width/2.00],
             [self.center.z - self.width/2.00,
                self.center.z - self.width/2.00]],
            [[self.center.x - self.width/2.00,
                self.center.x - self.width/2.00],
             [self.center.y - self.width/2.00,
                self.center.y - self.width/2.00],
             [self.center.z - self.width/2.00,
                self.center.z + self.width/2.00]],
            [[self.center.x - self.width/2.00,
                self.center.x + self.width/2.00],
             [self.center.y - self.width/2.00,
                self.center.y - self.width/2.00],
             [self.center.z + self.width/2.00,
                self.center.z + self.width/2.00]],
            [[self.center.x + self.width/2.00,
                self.center.x + self.width/2.00],
             [self.center.y - self.width/2.00,
                self.center.y - self.width/2.00],
             [self.center.z - self.width/2.00,
                self.center.z + self.width/2.00]],
            [[self.center.x - self.width/2.00,
                self.center.x + self.width/2.00],
             [self.center.y + self.width/2.00,
                self.center.y + self.width/2.00],
             [self.center.z - self.width/2.00,
                self.center.z - self.width/2.00]],
            [[self.center.x - self.width/2.00,
                self.center.x - self.width/2.00],
             [self.center.y + self.width/2.00,
                self.center.y + self.width/2.00],
             [self.center.z - self.width/2.00,
                self.center.z + self.width/2.00]],
            [[self.center.x - self.width/2.00,
                self.center.x + self.width/2.00],
             [self.center.y + self.width/2.00,
                self.center.y + self.width/2.00],
             [self.center.z + self.width/2.00,
                self.center.z + self.width/2.00]],
            [[self.center.x + self.width/2.00,
                self.center.x + self.width/2.00],
             [self.center.y + self.width/2.00,
                self.center.y + self.width/2.00],
             [self.center.z - self.width/2.00,
                self.center.z + self.width/2.00]],
            [[self.center.x - self.width/2.00,
                self.center.x - self.width/2.00],
             [self.center.y - self.width/2.00,
                self.center.y + self.width/2.00],
             [self.center.z + self.width/2.00,
                self.center.z + self.width/2.00]],
            [[self.center.x + self.width/2.00,
                self.center.x + self.width/2.00],
             [self.center.y - self.width/2.00,
                self.center.y + self.width/2.00],
             [self.center.z + self.width/2.00,
                self.center.z + self.width/2.00]],
            [[self.center.x - self.width/2.00,
                self.center.x - self.width/2.00],
             [self.center.y - self.width/2.00,
                self.center.y + self.width/2.00],
             [self.center.z - self.width/2.00,
                self.center.z - self.width/2.00]],
            [[self.center.x + self.width/2.00,
                self.center.x + self.width/2.00],
             [self.center.y - self.width/2.00,
                self.center.y + self.width/2.00],
             [self.center.z - self.width/2.00,
                self.center.z - self.width/2.00]],
        ])

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
            self.points.centroid(),
            max(self.points.bbox_dim()),
            self.points,
            None
        )
        # subdivide `depth` times
        self.head.subdivide(self.depth)
        self.leaf_nodes = self.head.leaf_nodes()

    def show(self):
        """
        ! WARNING ! For small cases only!
        Makes a plot showing the boundaries of the
        octree leaf nodes and the points
        """
        fig = plt.figure()
        ax = plt.axes(projection='3d')
        kwargs_node = {'alpha': 0.50, 'color': 'black'}

        for lines in self.head.lines_to_plot():
            ax.plot3D(*lines, **kwargs_node)

        for leaf in self.leaf_nodes:

            for lines in leaf.lines_to_plot():
                ax.plot3D(*lines, **kwargs_node)
            x_coords = []
            y_coords = []
            z_coords = []
            for pt in leaf.contents.points:
                x_coords.append(pt.x)
                y_coords.append(pt.y)
                z_coords.append(pt.z)
            ax.scatter(x_coords, y_coords, z_coords)
        plt.show()
