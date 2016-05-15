# Hanging-Mobile
CS 189 Hanging Mobile Project

### Input
We are given a set of point mass with locations in 3D.

### Output
A set of cross bars and balancing points will be generated.


### Libraries
* [Shapely](http://toblerity.org/shapely/) A 2D geometry library.
* In order to install Shapely, first install GEOS `brew install geos`


###### Result format

```
bars
# <idx> <center position> <radius> <orientation> <balance point>

1 center.x, center.y, center.z, radius, phi, alpha
2 center.x, center.y, center.z, radius, phi, alpha
3 center.x, center.y, center.z, radius, phi, alpha
4 center.x, center.y, center.z, radius, phi, alpha
5 center.x, center.y, center.z, radius, phi, alpha

tree
# <idx> <left idx> <right idx>
1     2     5
2     3     4
3  
4

```
