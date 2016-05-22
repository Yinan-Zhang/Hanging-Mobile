# Given 2 points (A, B) in 3D, and a gravity vector g
# calcuate the matrix M that maps them into a 2D space, where
import math
import numpy as np

# p3d defined as [[x1, y1, z1], [x2, y2, z2]]
def global2local(p3dpair):
	M = [[0, 0]]
	delta_x = p3dpair[1][0]-p3dpair[0][0] # x2-x1
	delta_y = p3dpair[1][1]-p3dpair[0][1] # y2-y1
	delta_z = p3dpair[1][2]-p3dpair[0][2] # z2-z1
	M.append([math.sqrt(delta_x*delta_x+delta_y*delta_y), delta_z])
	return M
	

# p2d defined as [x, y]
def local2global(p3dpair, p2d, p2pair):
	#ratio = p2d[0]/p2pair[1][0]
	#p = []
	#delta_x = p3dpair[1][0]-p3dpair[0][0] # x2-x1
	#delta_y = p3dpair[1][1]-p3dpair[0][1] # y2-y1
	#delta_z = p3dpair[1][2]-p3dpair[0][2] # z2-z1
	#p.append(p3dpair[0][0] + ratio*delta_x)
	#p.append(p3dpair[0][1] + ratio*delta_y)
	#p.append(p3dpair[0][2] + ratio*delta_z)

	p = []
	ratio = p2d[0]/p2pair[1][0]
	delta_x = p3dpair[1][0]-p3dpair[0][0] # x2-x1
	delta_y = p3dpair[1][1]-p3dpair[0][1] # y2-y1
	p.append(p3dpair[0][0] + ratio*delta_x)
	p.append(p3dpair[0][1] + ratio*delta_y)
	p.append(p3dpair[0][2] + p2d[1])
	
	return p

def test_frame_funcs():
	p = [[1, 1, 1], [2, 2, 2]]
	pair2d = global2local(p) #[[0, 0], [1.4142135623730951, 1]]
	print pair2d
	p2d = [math.sqrt(2)/2.0, 0.5]
	print local2global(p, p2d, pair2d) #[1.5, 1.5, 1.5]

def normalize(v):
    norm=np.linalg.norm(v)
    if norm==0: 
       return v
    return v/norm

# from: http://www.mathworks.com/matlabcentral/answers/81694-rotate-3d-plane-to-a-new-2d-coordinate-system
def transfromto2D(Coor_3D_array): # Input format as [[1, 1, 1], [2, 2, 1], [2, 2, 2], [1, 1, 2]]
	N = len(Coor_3D_array)
	Coor_3D = np.matrix(Coor_3D_array)
	origin = Coor_3D[0,:]
	unito = normalize(origin)

	localz = np.cross(Coor_3D[1,:]-origin, Coor_3D[2,:]-origin)
	unitz = normalize(localz)

	localx = Coor_3D[1,:]-origin
	unitx = normalize(localx)

	localy = np.cross(localz, localx)  
	unity = normalize(localy) 

	unit = np.array([[0, 0, 0, 1]])
	T = np.concatenate((np.transpose(unitx), np.transpose(unity), np.transpose(unitz), np.transpose(unito)), axis=1)
	T = np.concatenate((T, unit), axis=0)
	C = np.concatenate((Coor_3D, np.ones((N,1))), axis=1)
	Original_Coor_2D = np.linalg.solve(T, C.T)
	Coor_2D = Original_Coor_2D[0:2,:]
	return Coor_2D.T, T

# input must be a numpy matrix
def transfromto3D(Coor_2D, T, N):
	Coor_2D = np.concatenate((Coor_2D.T, np.matrix(np.zeros(N)), np.matrix(np.ones(N))), axis=0) 
	result = np.dot(T, Coor_2D)
	result = result[0:3,:]
	return result.T

def test_transfromto2D():
	# Four points case
	Coor_3D_array = [[1, 1, 1], [2, 2, 1], [2, 2, 2], [2, 2, 1]]
	Coor_2D, T = transfromto2D(Coor_3D_array)
	print Coor_2D
	print T
	print transfromto3D(Coor_2D, T, 4)
	print transfromto3D(np.matrix([0.59771698, 0.42264973]), T, 1)

	print "Two points case"
	# Two points case
	Coor_3D_array = [[1, 1, 1], [2, 2, 1], [2, 2, 2]]
	Coor_2D, T = transfromto2D(Coor_3D_array)
	print Coor_2D


#test_transfromto2D()



