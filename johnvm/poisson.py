import numpy as np
from dataclasses import dataclass, field
from typing import List
import matplotlib.pyplot as plt
# from functools import total_ordering


@dataclass
class Point:
    """
    Oriented point.
    """
    # Location
    x: float
    y: float
    z: float
    # Normal
    nx: float
    ny: float
    nz: float

    def __eq__(self, other):
        return (self.x == other.x and
                self.y == other.y and
                self.z == other.z)


@dataclass
class Points:
    """
    Collector for unique oriented points.
    """
    points: List[Point] = field(default_factory=list)

    def add(self, pt: Point):
        """
        Add a point in the list of points,
        if it is not already in
        """
        if pt not in self.points:
            self.points.append(pt)
        else:
            raise ValueError('Oriented point already exists: '
                             + repr(pt))

    def show(self):
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

##########
# OCTREE #
##########


@dataclass
class Node:
    """
    Octree node.
    """
    # is it a leaf node?
    leaf: bool

    # center of the cube
    center: Point
    # width of the cube
    width: float

    # association with other nodes
    parent: 'Node'
    children: List['Node']
    depth: int

    # points contained in the node
    contents: List[Point]


@dataclass
class Octree:
    """
    Octree spatial partition
    """
