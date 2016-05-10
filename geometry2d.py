import sys, os
from shapely import Point

def normalize(vec):
    length = math.sqrt(vec[0]**2 + vec[1]**2)
    return (vec[0]/length, vec[1]/length)

def length(point_a, point_b):
    return math.sqrt( (point_a.x-point_b.x)**2 + (point_a.y-point_b.y)**2 );

def vector(point_a, point_b):
    '''return the vector from point a to b'''
    return Point( point_b.x-point_a.x, point_b.y-point_a.y );

def vec_dot(vec_a, vec_b):
    return vec_a.x * vec_b.x + vec_a.y * vec_b.y;

def vec_plus(vec_a, vec_b):
    return Point(vec_a.x + vec_b.x, vec_a.y + vec_b.y);

def vec_times(vec, num):
    '''vector times a number'''
    return Point(vec.x * num, vec.y * num);

def point2str(point):
    return "(" + str(point.x) + ", " + str(point.y) + ')';

class Segment:
    '''A segment is directed fron vert1 to vert2'''
    def __init__(self, vert1, vert2):
        self.vert1 = vert1;
        self.vert2 = vert2;

    def normal(self):
        a = (self.vert2.x - self.vert1.x, self.vert2.y - self.vert1.y);
        b1 = a[1]; b2 = -a[0];
        if a[0] * b2 - a[0] * b1 < 0:
            return Point(normalize((b1, b2)));
        else:
            return Point(normalize((-b1, -b2)));

    def length(self):
        return math.sqrt( (self.vert1.x-self.vert2.x)**2 + (self.vert1.y-self.vert2.y)**2 );
