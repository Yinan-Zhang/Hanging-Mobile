import sys,os
import bpy
import mathutils
from mathutils import Vector

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

        def get_four_vertices(phi_, theta_):
            eps = 0.01;
            vert1 = self.center.x


        vertices = [];
        faces = [];



        pass;


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
