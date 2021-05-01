from johnvm.poisson import Oriented_Points, Node, Octree
import matplotlib.pyplot as plt


def show_Oriented_Points(pts: Oriented_Points):
    """
    Show a 3D scatter polot of the points
    """
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    x_coords = []
    y_coords = []
    z_coords = []
    for pt in pts.points:
        x_coords.append(pt.x)
        y_coords.append(pt.y)
        z_coords.append(pt.z)
    ax.scatter(x_coords, y_coords, z_coords)
    plt.show()


def generate_octree_node_bbox(n: Node):
    return ([
        [[n.center.x - n.width/2.00,
            n.center.x + n.width/2.00],
         [n.center.y - n.width/2.00,
            n.center.y - n.width/2.00],
         [n.center.z - n.width/2.00,
            n.center.z - n.width/2.00]],
        [[n.center.x - n.width/2.00,
            n.center.x - n.width/2.00],
         [n.center.y - n.width/2.00,
            n.center.y - n.width/2.00],
         [n.center.z - n.width/2.00,
            n.center.z + n.width/2.00]],
        [[n.center.x - n.width/2.00,
            n.center.x + n.width/2.00],
         [n.center.y - n.width/2.00,
            n.center.y - n.width/2.00],
         [n.center.z + n.width/2.00,
            n.center.z + n.width/2.00]],
        [[n.center.x + n.width/2.00,
            n.center.x + n.width/2.00],
         [n.center.y - n.width/2.00,
            n.center.y - n.width/2.00],
         [n.center.z - n.width/2.00,
            n.center.z + n.width/2.00]],
        [[n.center.x - n.width/2.00,
            n.center.x + n.width/2.00],
         [n.center.y + n.width/2.00,
            n.center.y + n.width/2.00],
         [n.center.z - n.width/2.00,
            n.center.z - n.width/2.00]],
        [[n.center.x - n.width/2.00,
            n.center.x - n.width/2.00],
         [n.center.y + n.width/2.00,
            n.center.y + n.width/2.00],
         [n.center.z - n.width/2.00,
            n.center.z + n.width/2.00]],
        [[n.center.x - n.width/2.00,
            n.center.x + n.width/2.00],
         [n.center.y + n.width/2.00,
            n.center.y + n.width/2.00],
         [n.center.z + n.width/2.00,
            n.center.z + n.width/2.00]],
        [[n.center.x + n.width/2.00,
            n.center.x + n.width/2.00],
         [n.center.y + n.width/2.00,
            n.center.y + n.width/2.00],
         [n.center.z - n.width/2.00,
            n.center.z + n.width/2.00]],
        [[n.center.x - n.width/2.00,
            n.center.x - n.width/2.00],
         [n.center.y - n.width/2.00,
            n.center.y + n.width/2.00],
         [n.center.z + n.width/2.00,
            n.center.z + n.width/2.00]],
        [[n.center.x + n.width/2.00,
            n.center.x + n.width/2.00],
         [n.center.y - n.width/2.00,
            n.center.y + n.width/2.00],
         [n.center.z + n.width/2.00,
            n.center.z + n.width/2.00]],
        [[n.center.x - n.width/2.00,
            n.center.x - n.width/2.00],
         [n.center.y - n.width/2.00,
            n.center.y + n.width/2.00],
         [n.center.z - n.width/2.00,
            n.center.z - n.width/2.00]],
        [[n.center.x + n.width/2.00,
            n.center.x + n.width/2.00],
         [n.center.y - n.width/2.00,
            n.center.y + n.width/2.00],
         [n.center.z - n.width/2.00,
            n.center.z - n.width/2.00]],
    ])


def show_octree_leaf(o: Octree, i: int):
    """
    Makes a plot of a single leaf node (the i-th)
    and its containing points
    """
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    kwargs_node = {'alpha': 0.20, 'color': 'black'}

    for lines in generate_octree_node_bbox(o.head):
        ax.plot3D(*lines, **kwargs_node)

    leaf = o.leaf_nodes[i]
    for lines in generate_octree_node_bbox(leaf):
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


def show_octree(o: Octree):
    """
    ! WARNING ! For small cases only!
    Makes a plot showing the boundaries of the
    octree leaf nodes and the points
    """
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    kwargs_node = {'alpha': 0.20, 'color': 'black'}

    for lines in generate_octree_node_bbox(o.head):
        ax.plot3D(*lines, **kwargs_node)

    for leaf in o.leaf_nodes:

        for lines in generate_octree_node_bbox(leaf):
            ax.plot3D(*lines, **kwargs_node)
        x_coords = []
        y_coords = []
        z_coords = []
        for pt in leaf.contents.points:
            x_coords.append(pt.x)
            y_coords.append(pt.y)
            z_coords.append(pt.z)
        ax.scatter(x_coords, y_coords, z_coords, marker=".")
    plt.show()
