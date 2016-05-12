'''
Given a polyhedral, assume the mass is evenly distributed, find the center of mass. 
'''
from shapely.geometry import Polygon

def mass_center(polygon):
	point_list = list(polygon.exterior.coords)
	# Algorithm from: http://stackoverflow.com/questions/5271583/center-of-gravity-of-a-polygon
	A = 0.0
	Cx = 0.0
	Cy = 0.0
	size = len(point_list) - 1
	if size <= 2:
		print "not a polygon"
		return
	for i in range(0, size-1):
		A = A + (point_list[i][0]*point_list[i+1][1]-point_list[i+1][0]*point_list[i][1])
		Cx = Cx + (point_list[i][0]*point_list[i+1][1]-point_list[i+1][0]*point_list[i][1])*(point_list[i][0]+point_list[i+1][0])
		Cy = Cy + (point_list[i][0]*point_list[i+1][1]-point_list[i+1][0]*point_list[i][1])*(point_list[i][1]+point_list[i+1][1])
	
	A = A/2.0
	Cx = Cx/6.0/A
	Cy = Cy/6.0/A

	return [Cx, Cy]

def test_mass_center():
	polygon1 = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])
	print mass_center(polygon1), "which should be [0.5, 0.5]"

# test_mass_center()
		