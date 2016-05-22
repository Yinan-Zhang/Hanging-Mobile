import sys, os
from geometry2d import *
from math import sqrt, acos, cos, sin, pi, fabs

def find_balance_point( mass1, mass2, pos1, pos2 ):
    '''Find the balance point for a cross bar that hangs two points mass.
    We construct cross bars to be a quarter of a circle.
    pos1 is one the left and pos2 is on the right.
    Return:
        0. center of the quarter-circle
        1. radius of the quarter-circle cross bar
        2. angle indicates the balance point. (angle from the right-end point to the balance point)
        3. the balance point location
    '''
    center, radius = find_quarter_circle(pos1, pos2);

    phi = acos( ( pos2.x-center.x ) / float(radius) );# The angle between the right-end point and the horizon.
    cos_alpha_phi = ( (pos1.x * mass1 + pos2.x * mass2)/(mass1+mass2) - center.x ) / radius;
    alpha = acos(cos_alpha_phi) - phi;

    point = Point(center.x + radius * cos(phi+alpha), center.y + radius * sin(phi+alpha));
    return center, radius, phi, alpha, point

def evaluate_balance_point(mass1, mass2, pos1, pos2, pos_b, center, radius, alpha):
    '''
    @param mass1, mass2: the mass of two points mass
    @param pos1, pos2: the position of two ends of the cross bar.
    @param pos_b: balance point position
    @param center: center of the quarter-circle (cross-bar)
    @param radius: cross-bar radius
    @param alpha: angle from the right-end point to the balance point
    '''
    phi = acos( ( pos2.x-center.x ) / float(radius) );# The angle between the right-end point and the horizon
    del_alpha = pi / 100;
    left_shift_balance_point  = Point(center.x + radius * cos(phi+alpha+del_alpha), center.y + radius * sin(phi+alpha+del_alpha));
    right_shift_balance_point = Point(center.x + radius * cos(phi+alpha-del_alpha), center.y + radius * sin(phi+alpha-del_alpha));

    eval_left  = evaluate_hanging_point(mass1, mass2, pos1, pos2, left_shift_balance_point);
    eval_right = evaluate_hanging_point(mass1, mass2, pos1, pos2, right_shift_balance_point);

    return max(eval_left, eval_right);


def evaluate_hanging_point(mass1, mass2, pos1, pos2, pos_b):
    '''Given two points mass, and a hanging point (at pos_b), evaluate how much is the cross-bar
    going to rotate to keep them balanced, if the balance point is shifted a little bit.
    '''

    len_1 = length(pos1, pos_b);
    len_2 = length(pos2, pos_b);
    len_12= length(pos1, pos2);

    angle = acos( (len_1**2 + len_2**2 - len_12**2)/ (2 * len_1 * len_2) ); # the angle betweel two side points to the balance point

    balance_angle = balance_bin_search(mass1, mass2, len_1, len_2, 0, pi/2.0, angle, 0.001 );
    heigh1 = len_1 * sin(balance_angle);
    heigh2 = len_2 * sin(pi - balance_angle - angle);

    return fabs(pos1.y - heigh1) + fabs(pos2.y-heigh2);

def balance_bin_search(mass1, mass2, r1, r2, alpha_min, alpha_max, angle, min_tq_diff):
    '''Given a balance point, binary search for the balance position (rotation angle of the cross-bar)'''
    alpha = (alpha_min+alpha_max) / 2.0;
    tq1 = mass1 * r1 * cos(alpha)
    tq2 = mass2 * r2 * cos(pi - alpha - angle)
    if fabs(tq1 - tq2) < min_tq_diff:
        return alpha;
    if tq1 > tq2:
        return balance_bin_search(mass1, mass2, r1, r2, alpha, alpha_max, angle, min_tq_diff);
    else:
        return balance_bin_search(mass1, mass2, r1, r2, alpha_min, alpha, angle, min_tq_diff);


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

#center,r = find_quarter_circle(Point(0,0), Point(2,3 ))
#print center
#print r
#center, radius, phi, alpha, balance_point = find_balance_point(1, 2, Point(0.5, 0.5), Point(3.5, 1))
#print center
#print radius
#print balance_point
