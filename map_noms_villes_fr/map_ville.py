#!/usr/bin/python3

import re
import gmplot
import numpy as np


coord_map = open('./eucircos_regions_departements_circonscriptions_communes_gps.csv', 'r')

term = 'ville'

LONG = []
LAT = []

for line in coord_map:
	
	
	name = line.split(';')[8]
	lat_ = line.split(';')[11]
	long_ = line.split(';')[12]
	
	if lat_ == '' or long_ == '' or long_ == '-':
		continue
		
	if re.search(term.lower(), name.lower()):
		
		
		LAT.append(float(long_))
		LONG.append(float(lat_))


''' Get map '''
gmap = gmplot.GoogleMapPlotter(47, 2.4, 3)
''' And point map '''
gmap.scatter(LONG, LAT, '#d041e0', size=5000, marker=False)
''' Heatmap '''
gmap.heatmap(LONG, LAT)
''' Final plot '''
gmap.draw("mymap.html")

