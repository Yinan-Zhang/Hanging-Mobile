
from balance import *
from shapely.geometry import Polygon, Point
from math import pi
import binary_space_partition

def test():
    pos1 = Point( -10, 0 );
    pos2 = Point( 10,  0 );
    mass1 = 10;
    mass2 = 10;
    center, radius, alpha, balance_point = find_balance_point(mass1, mass2, pos1, pos2);

    print center, radius, alpha, balance_point

    print evaluate_balance_point(mass1, mass2, pos1, pos2, balance_point, center, radius, alpha);


    ###########################################################
    ##### High level steps of the algorithm
    ###########################################################
    ## We construct the hanging mobile as a binary tree, where
    ## every polygon is a leaf, and every cross-bar is a non-leaf
    ## node of the tree.
    ##  1. Compute mass centers for each polygons
    ##  2. Based on the mass center, determine the hanging point
    ##     on each polygon
    ##  3. sort mass centers using kd-tree
    ##     (kd-tree constructs the mass centers as a binary tree.
    ##      let set_a, set_b be two sets of points that belong to
    ##      a same node in the tree, we will put a cross bar to
    ##      hang the two sets of points. )
    ##  4. Find balance points from bottom up. Take cross-bar weight
    ##     into consideration. (the weight of the cross bar is
    ##     positive correlated to the length)

class TreeNode(object):
    def __init__(self, node_id):
        self.pos = Point(0, 0); # y and z?
        self.radius = 0
        self.phi = 0
        self.alpha = 0
        self.mass = 0
        self.center = 0
        self.node_id = node_id
        self.left = None
        self.right = None


def buildTree(tree_as_list, centroid_list, mass_list, node_id_ref):
    if tree_as_list[0] == -1:#this this hanging bar
        rv = TreeNode(node_id_ref[0])
        node_id_ref[0]+=1
        rv.left = buildTree(tree_as_list[1], centroid_list, mass_list, node_id_ref)
        rv.right = buildTree(tree_as_list[2], centroid_list, mass_list, node_id_ref)
        center, radius, alpha, pos = find_balance_point(rv.left.mass, rv.right.mass, rv.left.pos, rv.right.pos);
        
        rv.center = center
        rv.radius = radius
        rv.alpha = alpha
        rv.pos = pos
        
        rv.mass = rv.left.mass + rv.right.mass
        print rv.node_id, rv.pos, rv.radius, rv.phi, rv.alpha, rv.left.node_id, rv.right.node_id
        return rv
    else:#leaf
        rv = TreeNode(node_id_ref[0])
        node_id_ref[0]+=1
        rv.pos = Point(tree_as_list[0])
        idx = centroid_list.index(tree_as_list[0])
        rv.mass = mass_list[idx]
        print rv.node_id, rv.pos 
        return rv

def main():
    polygon_list = []
    centroid_list = []
    mass_list = []
    with open('input.txt') as f:
        for line in f:
            if line[0] == '#':
                continue
            polygon_raw = []
            for point in line.split(' '):
                polygon_raw.append(map(float, point.split(',')))
            #print polygon_raw
            polygon_list.append(Polygon(polygon_raw))

    with open('mass_list.txt') as f:
        mass_list = map(float, f.read().split('\n'))

    for polygon in polygon_list:
        centroid_list.append(list(polygon.centroid.coords))

    tree = binary_space_partition.kdtree(centroid_list)
    buildTree(tree, centroid_list, mass_list, [1])


main();
