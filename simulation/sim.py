import sys,os
import bpy
import mathutils
from math import cos, sin, pi
from mathutils import Vector

class Piece:
    def __init__(self, vertices, center, normal, thickness = 0.15):
        '''Convex, vertices are in 3D.'''
        self.verts = [];
        self.normal = normal;
        self.center = center;

        vertices_new = []
        for vert in vertices:
            vertices_new.append( (vert[0]-self.center[0],vert[1]-self.center[1],vert[2]-self.center[2]) )

        for vert in vertices_new:
            self.verts.append( (vert[0] + normal[0] * thickness, vert[1] + normal[1] * thickness, vert[2] + normal[2] * thickness) );
        for vert in vertices_new:
            self.verts.append( (vert[0] - normal[0] * thickness, vert[1] - normal[1] * thickness, vert[2] - normal[2] * thickness) );

        self.faces = [];

        self.faces.append( tuple([i for i in range(len(vertices))]) );
        self.faces.append( tuple([i for i in range(len(self.verts)-1, len(vertices)-1, -1)]) );

        for i in range(len(vertices)-1):
            self.faces.append( (i, i+len(vertices), i+len(vertices)+1, i+1) )

        self.faces.append( (len(vertices)-1, len(vertices)*2-1 , 0 + len(vertices), 0 ) )

    def mesh_data(self):
        return self.verts, self.faces;
    
    def create_obj(self, name):
        verts, faces = self.mesh_data();
        obj = create_mesh( name, Vector(self.center), verts, faces )
        bpy.context.object.select = False;
        obj.select = True;
        bpy.context.scene.objects.active = obj;
        bpy.ops.rigidbody.object_add();
        obj.rigid_body.collision_shape = "MESH"
        return obj
    @staticmethod
    def create_dummy_obj( location, name):
        vertices = [(0,0,0), (0.01,0,0),(0.01,0.01,0),(0,0.01,0)];
        piece = Piece(vertices, location, (1,0,0), 0.01);
        obj = piece.create_obj(name);
        return obj

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
        self.object = None;
       

    def left_end(self):
        r = self.radius;
        local = (r * cos(self.phi+pi/2.0) * cos(self.theta), r * cos(self.phi+pi/2.0) * sin(self.theta), r * sin(self.phi+pi/2.0))
        return (self.center[0]+local[0], self.center[1]+local[1], self.center[2]+local[2])
    
    def right_end(self):
        r = self.radius;
        local = (r * cos(self.phi) * cos(self.theta), r * cos(self.phi) * sin(self.theta), r * sin(self.phi))
        return (self.center[0]+local[0], self.center[1]+local[1], self.center[2]+local[2])

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

    def create_obj( self, name ):
        verts, faces = self.mesh_data();
        obj = create_mesh( name, Vector(self.center), verts, faces )
        self.object = obj;
        #obj.game.physics_type = "RIGID_BODY"
        bpy.context.object.select = False;
        obj.select = True;
        bpy.context.scene.objects.active = obj;
        bpy.ops.rigidbody.object_add();
        obj.rigid_body.collision_shape = "MESH"
        #bpy.ops.object.origin_set(type="GEOMETRY_ORIGIN");
        bpy.ops.object.select_all(action='DESELECT')
        return obj

def hang(obj, bar, option):
    '''hang obj1 on bar (left or right)'''
    bar_pos = None;
    if option == "left":
        bar_pos = bar.left_end();
    elif option == "right":
        bar_pos = bar.right_end();
    
    bpy.ops.object.select_all(action='DESELECT')
    # Create a dummy object with fixed constraint with obj 2
    dummy = Piece.create_dummy_obj( bar_pos, bar.object.name + "_dummy" + ("_l" if option== "left" else '_r') );
    dummy.select = True;
    bar.object.select = True;
    bpy.ops.rigidbody.connect(con_type = "FIXED");
    bpy.ops.object.select_all(action='DESELECT')
    
    # Hang obj1 to the dummy object with rigid body constraint.
    dummy.select = True;
    bpy.context.scene.objects.active = dummy;
    bpy.ops.rigidbody.constraint_add(type = "POINT");
    dummy.rigid_body_constraint.object1 = dummy;
    dummy.rigid_body_constraint.object2 = obj;
    
    # De-select all.
    bpy.ops.object.select_all(action='DESELECT')
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

def parse_OBJ(coords):
    vertices = [];
    for i in range(0,len(coords),3):
        vertices.append( (float(coords[i]), float(coords[i+1]), float(coords[i+2])) );
    return Piece( vertices[1:], vertices[0], (1,0,0) );

def parse_BAR(coords):
    center = (float(coords[0]),float(coords[1]),float(coords[2]))
    radius = float(coords[3])
    phi    = float(coords[4])
    theta  = float(coords[5])
    alpha  = float(coords[6])
    return CrossBar( center, radius, phi, theta, alpha );

def read_file(filepath):
    file = open(filepath, "r");
    for line in file:
        info = line.split(",")
        if info[0].strip() != "TREE":
            idx = int(info[0].strip());
            if info[1].strip() == "BAR":
                bar = parse_BAR(info[2:])
                bar.create_obj(str(idx))
            elif info[1].strip() == "OBJ":
                obj = parse_OBJ(info[2:])
                obj.create_obj(str(idx))
        else: # Tree
            pass;

def delete_all():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete();

def main():
    origin = Vector((0,0,0))
    #vertices = [(0,0,0), (1,0,0), (1,1,0), (0,1,0)]
    #piece = Piece(vertices, (0,1,0), (0,0,1));
    #piece.create_obj("test")

    bar = CrossBar( (0,0,3), 3, pi/4, 0.3, 0.0 )
    bar_obj = bar.create_obj("bar");
    cube2 = bpy.data.objects["2"];
    hang(cube2, bar, "right")
    cube3 = bpy.data.objects["3"];
    hang(cube3, bar, "left")
    #pass;
    
    #delete_all()
    #read_file("../OBJECT.csv")

main();
