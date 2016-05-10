import sys, os
from geometry2d import *
from math import sqrt, acos, cos, sin

def find_balance_point( mass1, mass2, pos1, pos2 ):
    '''Find the balance point for a cross bar that hangs two points mass.
    We construct cross bars to be a quarter of a circle.
    pos1 is one the left and pos2 is on the right.
    Return:
        1. radius of the quarter-circle cross bar
        2. angle indicates the balance point. (angle from the right-end point to the balance point)
    '''
    center, radius = find_quarter_circle(pos1, pos2);

    # The angle between the right-end point and the horizon.
    phi = acos( ( pos2.x-center.x ) / float(radius) );
    cos_alpha_phi = ( (pos1.x * mass1 + pos2.x * mass2)/(mass1+mass2) - center.x ) / radius;
    alpha = acos(cos_alpha_phi) - phi;
    return radius, alpha

def evaluate_balance_point(self, mass1, mass2, pos1, pos2, pos_b):
    '''Given two points mass, and a balance point (at pos_b), evaluate how much is the cross-bar
    going to rotate to keep them balanced, if the balance point is shifted a little bit.'''
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
