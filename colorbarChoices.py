import datetime
import json
import logging
import urllib2

import ee

import figureFormatting

#===========================================
#   GET_COLORBAR
#===========================================
def get_colorbar(variable, anomOrValue, units):
    """"""
    #Set defaults to avoid error
    palette = ""
    minColorbar = 999
    maxColorbar = 999
    colorbarLabel = ''
    #remove first character which identifies the product
    variable = variable[1:]

    if variable == 'NDVI' or variable == 'EVI':
        if anomOrValue == 'anom':
            palette = "A50026,D73027,F46D43,FDAE61,FEE08B,FFFFBF,D9EF8B,A6D96A,66BD63,1A9850,006837"
            minColorbar = -.4
            maxColorbar = .4
            colorbarLabel = variable + ' Difference from climatology'
            colorbarmap = 'RdYlGn'
            colorbarsize = '8'
            varUnits = ''
        else:
            palette = "FFFFE5,F7FCB9,D9F0A3,ADDD8E,93D284,78C679,41AB5D,238443,006837,004529"
            minColorbar = -.1
            maxColorbar = .9
            colorbarLabel = variable
            colorbarmap = 'YlGn'
            colorbarsize = '9'
            varUnits = ''
    elif variable == 'NDSI' or variable == 'NDWI':
        if anomOrValue == 'anom':
            palette = "A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
            minColorbar = -.5
            maxColorbar = .5
            colorbarLabel = variable + ' Difference from climatology'
            colorbarmap = 'RdYlBu'
            colorbarsize = '88888888'
            varUnits = ''
        else:
            palette = "08306B,08519C,2171B5,4292C6,6BAED6,9ECAE1,C6DBEF,DEEBF7,F7FBFF"
            minColorbar = -.2
            maxColorbar = .7
            colorbarLabel = variable
            colorbarmap = 'invBlues'
            colorbarsize = '8'
            varUnits = ''
    elif variable == 'pr':
        if anomOrValue == 'anompercentof':
            minColorbar = 0
            maxColorbar = 200 #%
            palette = "67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
            colorbarLabel = 'Precipitation Amount as Percent of climatology'
            colorbarmap = 'RdYlBu'
            colorbarsize = '8'
            varUnits = '%'
        else:
            minColorbar = 0
            palette = "FFFFD9,EDF8B1,C7E9B4,7FCDBB,41B6C4,1D91C0,225EA8,0C2C84"
	    if units == 'metric':
           	 colorbarLabel = 'Precipitation Amount (mm)'
                 maxColorbar = 400
                 varUnits = 'mm'
	    elif units == 'english':
           	 colorbarLabel = 'Precipitation Amount (in)'
                 maxColorbar = 16
                 varUnits = 'in'
            colorbarmap = 'YlGnBu'
            colorbarsize = '8'
    elif variable in ['tmmx', 'tmmn', 'tmean']:
        palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
        colorbarmap = 'BuRd'
        colorbarsize = '8'
        if units == 'metric':
            varUnits = 'deg C'
	    colorbarLabel = 'Temperature (deg C)'
        elif units == 'english':
            varUnits = 'deg F'
	    colorbarLabel = 'Temperature (deg F)' 
        if anomOrValue == 'anom':
            palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
	    if units == 'metric':
		 colorbarLabel = 'Temperature Difference from climatology (deg C)'
                 minColorbar = -5
                 maxColorbar = 5
	    elif units == 'english':
		 colorbarLabel = 'Temperature Difference from climatology (deg F)'
                 minColorbar = -10
                 maxColorbar = 10
            colorbarmap = 'BuYlRd'
            colorbarsize = '8'
        elif variable == 'tmmx':
	    if units == 'metric':
                 minColorbar = -5
                 maxColorbar = 35
	    elif units == 'english':
                 minColorbar = 20
                 maxColorbar = 100
        elif variable == 'tmmn':
	    if units == 'metric':
	         minColorbar = -20
	         maxColorbar =25 
	    elif units == 'english':
	         minColorbar = 0
	         maxColorbar = 80
        elif variable == 'tmean':
            if units == 'metric':
                 minColorbar = -20
                 maxColorbar = 20
            elif units == 'english':
                 minColorbar = 0
                 maxColorbar = 80
    elif variable == 'rmin' or variable == 'rmax':
        if anomOrValue == 'anom':
            palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
            #incorrect:palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar = -15
            maxColorbar = 15
            colorbarLabel = 'Difference from climatology'
            colorbarmap = 'BrBG'
            colorbarsize = '9'
            varUnits = 'deg %'
        elif variable == 'rmin':
            palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            #incorrect palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar = 0
            maxColorbar = 100
            colorbarLabel = 'Percent'
            colorbarmap = 'BrBG'
            colorbarsize = '8'
            varUnits = 'deg %'
        elif variable == 'rmax':
            palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            #incorrect:palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar = 0
            maxColorbar = 100
            colorbarLabel = '%'
            colorbarmap = 'BrBG'
            colorbarsize = '8'
            varUnits = 'deg %'
    elif variable == 'srad':
        if anomOrValue == 'anom':
            palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar = -25
            maxColorbar = 25
	    if units == 'metric':
            	colorbarLabel = 'Radiation Difference from climatology (W/m2)'
	    elif units == 'english':
            	colorbarLabel = 'Radiation Difference from climatology (W/m2)'
            varUnits = 'W/m2'
            colorbarmap = 'BuYlRd'
            colorbarsize = '8'
        else:
            palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar = 100
            maxColorbar = 350
	    if units == 'metric':
		colorbarLabel = 'Radiation (W/m2)'
	    elif units == 'english':
            	colorbarLabel = 'Radiation (W/m2)'
            colorbarmap = 'BuRd'
            colorbarsize = '8'
            varUnits = 'W/m^2'
    elif variable == 'vs':
        if anomOrValue == 'anom':
            palette = "A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
	    if units == 'metric':
		colorbarLabel = 'Wind Speed Difference from climatology(' +'m/s'+' )'
                minColorbar = -2.5
                maxColorbar = 2.5
                varUnits = 'm/s'
	    elif units == 'english':
		colorbarLabel = 'Wind Speed Difference from climatology(' +'mi/hr'+' )'
                minColorbar = -5
                maxColorbar = 5
                varUnits = 'mi/hr'
            colorbarmap = 'BuYlRd'
            colorbarsize = '8'
        else:
            palette = "FFFFD9,EDF8B1,C7E9B4,7FCDBB,5DC2C1,41B6C4,1D91C0,225EA8,253494,081D58"
            minColorbar = 0
	    if units == 'metric':
		colorbarLabel = 'Wind Speed (m/s)'
                maxColorbar = 5
                varUnits = 'm/s'
	    elif units == 'english':
		colorbarLabel = 'Wind Speed (mi/hr)'
                maxColorbar = 10
                varUnits = 'mi/hr'
            colorbarmap = 'YlGnBu'
            colorbarsize = '8'
    elif variable == 'sph':
        if anomOrValue == 'anom':
            minColorbar = -30
            maxColorbar = 30
            palette = "053061,2166AC,4393C3,67ADD1,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,E88465,D6604D,B2182B,67001F"
            colorbarLabel = 'Percent Difference from climatology'
            colorbarmap = 'BuYlRd'
            colorbarsize = '8'
            varUnits = 'kg/kg'
        else:
            palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026,D6604D,B2182B,67001F"
            minColorbar = 0
            maxColorbar = 0.02
            colorbarLabel = 'kg / kg'
            colorbarmap = 'BuRd'
            colorbarsize = '8'
            varUnits = 'kg/kg'
    elif variable == 'erc':
        if anomOrValue == 'anom':
            minColorbar = -20
            maxColorbar = 20
            palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            colorbarLabel = 'Difference from climatology'
            colorbarmap = 'BuYlRd'
            colorbarsize = '8'
            varUnits = ''
        else:
            palette = "FFFFFF,FFFFCC,FFEDA0,FED976,FEB24C,FD8D3C,FC4E2A,E31A1C,BD0026,800026,000000"
            minColorbar = 10
            maxColorbar = 120
            colorbarLabel = ''
            colorbarmap = 'YlOrRd'
            colorbarsize = '8'
            varUnits = ''
    elif variable == 'pet': #mm
        if anomOrValue == 'anom':
            minColorbar = 80
            maxColorbar = 120
            palette = "053061,2166AC,4393C3,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,D6604D,B2182B,67001F"
            colorbarLabel = 'PET Percent of climatology'
            colorbarmap = 'BuYlRd'
            colorbarsize = '8'
            varUnits = '%'
        else:
            palette = "313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
	    if units == 'metric':
		colorbarLabel = 'PET (mm)'
                minColorbar = 300
                maxColorbar = 800
                varUnits = 'mm'
	    elif units == 'english':
		colorbarLabel = 'PET (in)'
                minColorbar = 10
                maxColorbar = 30
                varUnits = 'in'
            colorbarmap = 'BuRd'
            colorbarsize = '8'
    elif variable == 'wb': #mm
        if anomOrValue == 'anom':
            minColorbar = -100
            maxColorbar = 100
            palette = "67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
            colorbarLabel = 'Water Balance Percent change from climatology'
            colorbarmap = 'RdYlBu'
            colorbarsize = '8'
            varUnits = '%'
        else:
            palette = "A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
	    if units == 'metric':
		colorbarLabel = 'Water Balance (mm)'
                minColorbar = -220
                maxColorbar = 220
                varUnits = 'mm'
	    elif units == 'english':
		colorbarLabel = 'Water Balance (in)'
                minColorbar = -10
                maxColorbar = 10
                varUnits = 'in'
            colorbarmap = 'RdBu'
            colorbarsize = '8'
    elif variable == 'pdsi':
        if anomOrValue == 'anom':
            minColorbar = -6
            maxColorbar = 6
            palette = "67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
            colorbarLabel = 'PDSI Percent of climatology'
            colorbarmap = 'RdYlBu'
            colorbarsize = '8'
            varUnits = '%'
        else:
            minColorbar = -6
            maxColorbar = 6
            palette = "67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
            colorbarLabel = 'PDSI'
            colorbarmap = 'RdYlBu'
            colorbarsize = '8'
            varUnits = ''

    return colorbarmap, colorbarsize, minColorbar, maxColorbar, colorbarLabel, varUnits
