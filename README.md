# Hanging-Mobile
CS 189 Hanging Mobile Project

### Input
We are given a set of point mass with locations in 3D.

### Output
A set of cross bars and balancing points will be generated.


### Libraries
* [Shapely](http://toblerity.org/shapely/) A 2D geometry library.
* In order to install Shapely, first install GEOS `brew install geos`


#### Result format

We are going to assume that every hanging object is a sheet of polygon (2D object with thickness), and their normals are all parallel to x-axis.  

```
# <idx> BAR <center position> <radius> <orientation_phi> <orientation_theta> <balance point orientation>
# <idx> OBJ <p1.x> <p1.y> <p1.z> <p2.x> <p2.y> <p2.z> ....

1 BAR center.x, center.y, center.z, radius, phi, theta, alpha
2 BAR center.x, center.y, center.z, radius, phi, theta, alpha
3 BAR center.x, center.y, center.z, radius, phi, theta, alpha
4 BAR center.x, center.y, center.z, radius, phi, theta, alpha
5 BAR center.x, center.y, center.z, radius, phi, theta, alpha
6 OBJ point1.x, point1.y, point1.z, point2.x, point2.y, point2.z ....
7 OBJ point1.x, point1.y, point1.z, point2.x, point2.y, point2.z ....
8 OBJ point1.x, point1.y, point1.z, point2.x, point2.y, point2.z ....

tree
# <idx> <left idx> <right idx>
TREE 1     2     5
TREE 2     3     4
TREE 3  
TREE 4

```

**Explain:**

<img align="left" src="https://github.com/Yinan-Zhang/Hanging-Mobile/blob/master/doc/3D%20bar%20position%20explain.png" width="400">
<img align="right" src="https://github.com/Yinan-Zhang/Hanging-Mobile/blob/master/doc/IMG_0686.JPG" width="400">
