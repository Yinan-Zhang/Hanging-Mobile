import sys,os
import bpy
import mathutils
from math import cos, sin, pi
from mathutils import Vector

class Piece:
    def __init__(self, vertices, normal):
        '''Convex, vertices are in 3D.'''
        self.verts = [] + vertices;
        self.normal = normal;

        for vert in vertices:
            self.verts.append( (vert[0] - normal[0] * 0.4, vert[1] - normal[1] * 0.4, vert[2] - normal[2] * 0.4) );
        
        self.faces = [];

        self.faces.append( tuple([i for i in range(len(vertices))]) );
        self.faces.append( tuple([i for i in range(len(self.verts)-1, len(vertices)-1, -1)]) );

        for i in range(len(vertices)-1):
            self.faces.append( (i, i+len(vertices), i+len(vertices)+1, i+1) )

        self.faces.append( (len(vertices)-1, len(vertices)*2-1 , 0 + len(vertices), 0 ) )

    def mesh_data(self):
        return self.verts, self.faces;

class CrossBar:
    def __init__(self, center, radius, phi, theta, alpha):
        '''
        @ center is the center of the quarter-circle
        radius, phi, theta together define the right end of the bar.
        @ alpah defines the '''
        self.center = center;
        self.radius = radius;
        self.phi    = phi;
        self.theta  = theta;
        self.alpah  = alpha;

    def mesh_data(self):
        '''Get mesh data including vertices and faces'''

        def get_point(phi_, theta_, r):
            return (r * cos(phi_) * cos(theta_), r * cos(phi_) * sin(theta_), r * sin(phi_))

        def get_four_vertices(phi_, theta_):
            eps = 0.005
            r= self.radius;
            width = self.radius * 0.01
            if phi_ < pi/2.0:
                vert1 = get_point(phi_,  theta_ - eps, r-width)
                vert2 = get_point(phi_,  theta_ + eps, r-width)
                vert3 = get_point(phi_,  theta_ + eps, r+width)
                vert4 = get_point(phi_,  theta_ - eps, r+width)
                return [vert1, vert2, vert3, vert4];
            else:
                print("what?")
                vert1 = get_point(phi_,  theta_ + eps, r-width)
                vert2 = get_point(phi_,  theta_ - eps, r-width)
                vert3 = get_point(phi_,  theta_ - eps, r+width)
                vert4 = get_point(phi_,  theta_ + eps, r+width)
                return [vert1, vert2, vert3, vert4];

        vertices = [];
        for i in range(0,90):
            ratio = pi/180.0
            vertices += get_four_vertices( self.phi + i*ratio, self.theta );

        faces = [( 0, 1, 2, 3 )];
        for i in range(0, len(vertices)-4, 4):
            faces.append( (i+0, i+3, i+7, i+4) );
            faces.append( (i+3, i+2, i+6, i+7) );
            faces.append( (i+2, i+1, i+5, i+6) );
            faces.append( (i+1, i+0, i+4, i+5) );
        faces.append( (len(vertices)-1,len(vertices)-2,len(vertices)-3,len(vertices)-4 ) )

        return vertices, faces;

def create_mesh(name, origin, verts, faces):
    # Create mesh and object
    me = bpy.data.meshes.new(name+'Mesh')
    ob = bpy.data.objects.new(name, me)
    ob.location = origin
    ob.show_name = True

    # Link object to scene and make active
    scn = bpy.context.scene
    scn.objects.link(ob)
    scn.objects.active = ob
    ob.select = True

    # Create mesh from given verts, faces.
    me.from_pydata(verts, [], faces)
    # Update mesh with new data
    me.update()
    return ob

def main():
    origin = Vector((0,0,0))
    #vertices = [(0,0,0), (10,0,0), (10,10,0), (0,10,0)]
    #piece = Piece(vertices, (0,0,1));
    #verts, faces = piece.mesh_data();
    #create_mesh( "test", origin, verts, faces )
    
    bar = CrossBar( (0,0,0), 10, pi/4, 0.3, 0.0 )
    verts, faces = bar.mesh_data();
    create_mesh( "bar", origin, verts, faces )
    pass;

main();
