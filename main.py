
from balance import *
from shapely.geometry import Polygon, Point
from math import pi
import binary_space_partition
import constants
import frame
import numpy as np

def test():
    pos1 = Point( -10, 0 );
    pos2 = Point( 10,  0 );
    mass1 = 10;
    mass2 = 10;
    center, radius, phi, alpha, balance_point = find_balance_point(mass1, mass2, pos1, pos2);

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
        self.pos = [0, 0, 0]; # y and z?
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

        aux_point = [(rv.left.pos[0][0]+rv.right.pos[0][0])/2.0, (rv.left.pos[0][1]+rv.right.pos[0][1])/2.0, (rv.left.pos[0][2]+rv.right.pos[0][2])/2.0 - 1.0]
        posleftright, T = frame.transfromto2D(np.matrix([rv.left.pos[0], rv.right.pos[0], aux_point]))

        center, radius, phi, alpha, pos = find_balance_point(rv.left.mass, rv.right.mass, Point(posleftright[0].tolist()[0]), Point(posleftright[1].tolist()[0]));

        rv.center = center
        rv.radius = radius
        rv.alpha = alpha
        rv.pos = frame.transfromto3D(np.matrix(list(pos.coords)), T, 1).tolist()
        rv.phi = phi

        rv.mass = rv.left.mass + rv.right.mass + constants.DENSITY * rv.radius * pi / 2.0 # Plus the mass of the bar
        cord_to_print = rv.pos
        output_list = [rv.node_id, cord_to_print[0][0], cord_to_print[0][1], cord_to_print[0][2], rv.radius, rv.phi, rv.alpha, rv.left.node_id, rv.right.node_id]
        print ';'.join(map(str,output_list))
        return rv
    else:#leaf
        rv = TreeNode(node_id_ref[0])
        node_id_ref[0]+=1
        rv.pos = tree_as_list[0]
        idx = centroid_list.index(tree_as_list[0])
        rv.mass = mass_list[idx]
        cord_to_print = rv.pos
        output_list = [rv.node_id, cord_to_print[0][0], cord_to_print[0][1], cord_to_print[0][2]]
        print ';'.join(map(str,output_list))
        return rv

def main():
    polygon_list = []
    centroid_list = []
    mass_list = []
    transformation_list = []
    with open('input.txt') as f:
        for line in f:
            if line[0] == '#':
                continue
            polygon_raw = []
            for point in line.split(' '):
                polygon_raw.append(map(float, point.split(',')))
            #print polygon_raw
            Coor_2D, T = frame.transfromto2D(polygon_raw)
            polygon_list.append(Polygon(Coor_2D))
            transformation_list.append(T)
            #print Coor_2D.tolist()
            polygon_shapely_2d = Polygon(Coor_2D.tolist())
            centroid2d = polygon_shapely_2d.centroid.coords
            #print list(centroid2d)
            centroid3d = frame.transfromto3D(np.matrix(list(centroid2d)), T, 1).tolist()
            print centroid3d
            centroid_list.append(centroid3d)


    with open('mass_list.txt') as f:
        mass_list = map(float, f.read().split('\n'))

    tree = binary_space_partition.kdtree(centroid_list)
    print tree
    buildTree(tree, centroid_list, mass_list, [1])


main();
