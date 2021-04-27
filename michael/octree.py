import numpy as np

points = []

for x in range(2):
    for y in range(2):
        for z in range(2):
            points.append([x, y, z])
points = np.array(points)

class Node:
    def __init__(self, indices):
        node_points = np.array([points[i] for i in indices])
        self.indices = indices
        self.minimum = node_points.min(axis=0)
        self.maximum = node_points.max(axis=0)
        self.means = node_points.mean(axis=0)
        self.children = []

def construct_tree(points, indices, depth=0, max_depth=3):
    if len(indices) == 0:
        return None
    
    node = Node(indices)
    
    if len(indices) == 1 or depth == max_depth:
        return node
    
    child_indices = [[], [], [], [], [], [], [], []]
    
    for i in indices:
        if points[i, 0] < node.means[0]:
            if points[i, 1] < node.means[1]:
                index = 0
            else:
                index = 2
            if points[i, 2] < node.means[2]:
                child_indices[index].append(i)
            else:
                child_indices[index + 1].append(i)
        else:
            if points[i, 1] < node.means[1]:
                index = 0
            else:
                index = 2
            if points[i, 2] < node.means[2]:
                child_indices[index + 4].append(i)
            else:
                child_indices[index + 5].append(i)
            
    for i in range(8):
        node.children.append(construct_tree(points, child_indices[i], depth + 1))
    return node

root = construct_tree(points, [i for i in range(len(points))])