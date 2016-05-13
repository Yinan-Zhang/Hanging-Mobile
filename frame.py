# Given 2 points (A, B) in 3D, and a gravity vector g
# calcuate the matrix M that maps them into a 2D space, where
import math

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
	ratio = p2d[0]/p2pair[1][0]
	p = []
	delta_x = p3dpair[1][0]-p3dpair[0][0] # x2-x1
	delta_y = p3dpair[1][1]-p3dpair[0][1] # y2-y1
	delta_z = p3dpair[1][2]-p3dpair[0][2] # z2-z1
	p.append(p3dpair[0][0] + ratio*delta_x)
	p.append(p3dpair[0][1] + ratio*delta_y)
	p.append(p3dpair[0][2] + ratio*delta_z)
	return p

def test_frame_funcs():
	p = [[1, 1, 1], [2, 2, 2]]
	pair2d = global2local(p) #[[0, 0], [1.4142135623730951, 1]]
	print pair2d
	p2d = [math.sqrt(2)/2.0, 0.5]
	print local2global(p, p2d, pair2d) #[1.5, 1.5, 1.5]


