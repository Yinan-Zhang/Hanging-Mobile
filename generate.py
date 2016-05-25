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
from matplotlib.transforms import Affine2D
import mpl_toolkits.axisartist.floating_axes as floating_axes
import numpy as np
import mpl_toolkits.axisartist.angle_helper as angle_helper
from matplotlib.projections import PolarAxes
from mpl_toolkits.axisartist.grid_finder import (FixedLocator, MaxNLocator,
                                                 DictFormatter)
import constants
import sdxf

#import matplotlib.units as units

def setup_axes2(fig, rect, radius, width):
    """
    With custom locator and formatter.
    Note that the extreme values are swapped.
    """
    tr = PolarAxes.PolarTransform()

    pi = np.pi
    angle_ticks = [(0, r"$0$"),
                   (.25*pi, r"$\frac{1}{4}\pi$"),
                   (.5*pi, r"$\frac{1}{2}\pi$")]
    grid_locator1 = FixedLocator([v for v, s in angle_ticks])
    tick_formatter1 = DictFormatter(dict(angle_ticks))

    grid_locator2 = MaxNLocator(2)

    grid_helper = floating_axes.GridHelperCurveLinear(
        tr, extremes=(.5*pi, 0, radius+width, radius),
        grid_locator1=grid_locator1,
        grid_locator2=grid_locator2,
        tick_formatter1=tick_formatter1,
        tick_formatter2=None)

    ax1 = floating_axes.FloatingSubplot(fig, rect, grid_helper=grid_helper)
    fig.add_subplot(ax1)

    # create a parasite axes whose transData in RA, cz
    aux_ax = ax1.get_aux_axes(tr)

    aux_ax.patch = ax1.patch  # for aux_ax to have a clip path as in ax
    ax1.patch.zorder = 0.9  # but this has a side effect that the patch is
    # drawn twice, and possibly over some other
    # artists. So, we decrease the zorder a bit to
    # prevent this.

    return ax1, aux_ax

def generateBAR(radius, alpha, name):
	fig = plt.figure(1)
	ax2, aux_ax2 = setup_axes2(fig, 111, radius, constants.BAR_WIDTH)

	theta = alpha
	radius = radius + constants.BAR_WIDTH/2.0
	aux_ax2.scatter(theta, radius)
	
	ax2.set_aspect(1)
	aux_ax2.set_aspect(1)
	#plt.axes().set_aspect('equal', 'datalim')

	plt.savefig('./img/'+name, bbox_inches='tight')
	plt.clf()


def generatePNG(poly, name):
	#poly = Polygon([(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 0.8), (0, 0)])
	x,y = poly.exterior.xy

	d=sdxf.Drawing()

	#add drawing elements
	d.append(sdxf.LwPolyLine(points=list(poly.exterior.coords), flag=1))

	d.saveas('./img/' + name + '.dxf')

	'''
	#output PNG
	fig = plt.figure(1)
	ax = fig.add_subplot(1,1,1)
	ax.plot(x, y)
	ax.set_aspect(1)
	plt.savefig('./img/'+name, bbox_inches='tight')
	plt.clf()
	'''


#generatePNG(Polygon([(0, 0), (0, 2), (1, 1), (2, 2), (2, 0), (1, 0.8), (0, 0)]), "hehe")
#generateBAR(1, np.pi/4, "hehe")