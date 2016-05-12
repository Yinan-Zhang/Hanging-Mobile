
from balance import *
from shapely.geometry import Polygon, Point
from math import pi

def test():
    pos1 = Point( -10, 0 );
    pos2 = Point( 10,  0 );
    mass1 = 10;
    mass2 = 10;
    center, radius, alpha, balance_point = find_balance_point(mass1, mass2, pos1, pos2);

    print center, radius, alpha, balance_point

    evaluate_balance_point(mass1, mass2, pos1, pos2, balance_point, center, radius, alpha);

test();
