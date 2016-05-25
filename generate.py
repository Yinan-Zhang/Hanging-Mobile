# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 18:51:08 2015
@author: Duncan
A simplified version of linearring.py, one of the shapely examples
"""

from basic_units import cm, inch
from matplotlib import pyplot as plt
from shapely.geometry.polygon import LinearRing, Polygon
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.gridspec as gridspec

#import matplotlib.units as units


def generatePNG(poly, name):
	return

# 1: valid ring

#poly = Polygon([(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 0.8), (0, 0)])
	x,y = poly.exterior.xy

# ring = LinearRing([(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 0.8), (0, 0)])
# x, y = ring.xy

	fig = plt.figure(1)
	ax = fig.add_subplot(1,1,1)
	ax.plot(x, y)
	#plt.gca().xaxis.set_major_locator(plt.NullLocator())
	#plt.gca().yaxis.set_major_locator(plt.NullLocator())
	#plt.axis('off')
	#plt.xticks(np.arange(min(x), max(x)+1, 1.0))
	#plt.yticks(np.arange(min(y), max(y)+1, 1.0))
	#xrange = [-1, 3]
	#yrange = [-1, 3]
	#ax.set_xlim(*xrange)
	#ax.set_xticks(range(*xrange) + [xrange[-1]])
	#ax.set_ylim(*yrange)
	#ax.set_yticks(range(*yrange) + [yrange[-1]])
	ax.set_aspect(1)
	#plt.axis('off')
	#fig.savefig('to.png')

	plt.savefig('./img/'+name, bbox_inches='tight')

	plt.clf()

	#with PdfPages(name+'.pdf') as pdf:
	#	pdf.savefig(fig)

#generatePNG(Polygon([(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 0.8), (0, 0)]), "hehe")