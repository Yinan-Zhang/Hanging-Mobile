import sys, os
from geometry2d import *
from math import sqrt

def find_balance_point( mass1, mass2, pos1, pos2 ):
    '''Find the balance point for a cross bar that hangs two points mass.
    We construct cross bars to be a quarter of a circle.
    Return:
        1. radius of the quarter-circle cross bar
        2. angle indicates the balance point. (angle from the right-end point to the balance point)
    '''
    pass;


def find_quarter_circle(point1, point2):
    '''Return the center and radius of the quarter circle'''
    high = None; low = None;
    if point1.y > point2.y:
        high = point1; low = point2;
    else:
        high = point2; low = point1;

    segment = Segment(low, high);
    mid_point = Point( (point1.x+point2.x)/2.0, (point1.y+point2.y)/2.0 );
    normal = segment.normal();
    center = vec_plus(mid_point, vec_times(normal, segment.length()/2.0));
    radius = segment.length() / sqrt(2);
    return center, radius;
