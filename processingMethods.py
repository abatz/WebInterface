import datetime
import json
import logging
import urllib2

import ee

import collectionMethods
import figureFormatting

from google.appengine.api.labs import taskqueue
#===========================================
#   GET_IMAGES
#===========================================
def get_images(template_values):
    """"""
    from forms import stateLat, stateLong

    TV = {}
    for key, val in template_values.iteritems():
        TV[key] = val
    var = TV['variable']
    calculation = TV['anomOrValue']
    dT = TV['domainType']
    dS = TV['dateStart']
    dE = TV['dateEnd']
    yearStartClim = TV['yearStartClim']
    yearEndClim = TV['yearEndClim']
    statistic = TV['statistic']
    units = TV['units']
    palette = TV['palette']
    minColorbar = template_values['minColorbar']
    maxColorbar = template_values['maxColorbar']

    # Build EarthEngine date objects from date strings and explicitly set GMT
    # Note, by default EarthEngine date objects are already GMT
    dSUTC = ee.Date(dS, 'GMT')
    dEUTC = ee.Date(dE, 'GMT')

    # Remove starting character which indicates the product
    product = var[:1]
    var = var[1:]

    #==============
    #Initial Collection
    #==============
    collection, coll_name, coll_desc, var_desc, notes = collectionMethods.get_collection(
        product, var)

    #==============
    #Title and Source
    #==============
    #Set title
    title = statistic + ' ' + var_desc
    if calculation == 'clim':
        title = title + ' Climatology '
    elif calculation == 'anom':
        title = title + ' Difference from Climatology '
    elif calculation == 'anompercentchange':
        title = title + ' Percent Difference from Climatology '
    elif calculation == 'anompercentof':
        title = title + ' Percent Of Climatology '

    #Set source, domain, subdomain
    source = coll_desc + ' from ' + dS + '-' + dE + ''

    #==============
    #Anomaly
    #==============
    if calculation in ['value']:
        # FilterDate is exclusive on the high end, include an extra day on dEUTC
        collection = collection.filterDate(dSUTC, dEUTC.advance(1,'day'))
        collection = get_statistic(collection, statistic)
    elif calculation in ['anom', 'anompercentof', 'anompercentchange', 'clim']:
        # CalendarRange is inclusive on the high end, don't include an extra day on dEUTC
        collection, climatologyNotes = get_anomaly(
            collection, product, var, dSUTC, dEUTC, statistic,
            calculation, yearStartClim, yearEndClim)
        TV['climatologyNotes'] = climatologyNotes
        
    #==============
    #Units
    #==============
    collection = modify_units(collection, var, calculation, units)

    #==============
    #Get mapid
    #==============
    mapid = {'mapid':[], 'token':[]}
    mapid = map_collection(
        collection, TV['opacity'], palette, minColorbar, maxColorbar)

    #==============
    #Update template values
    #==============
    extra_template_values = {
        'source': source,
        'product':product,
        'productLongName': coll_desc,
        'variableShortName': var_desc,
        'title': title,
        'notes_map': notes
    }
    if mapid and mapid['mapid'] and mapid['token']:
        extra_template_values['mapid'] = mapid['mapid']
        extra_template_values['token'] = mapid['token']
    TV.update(extra_template_values)
    return TV

#===========================================
#    TIME_SERIES
#===========================================
def get_time_series(template_values):
    """"""
    TV = {}
    for key, val in template_values.iteritems():
        TV[key] = val
    var = TV['variable']
    mc = TV['marker_colors']
    dS = TV['dateStart']
    dE = TV['dateEnd']
    statistic = TV['statistic']
    units = TV['units']
    pointsLongLat = str(TV['pointsLongLat']) #string of comma separates llon,lat pairs
    pointsLongLatList = pointsLongLat.replace(' ','').split(',')
    pointsLongLatTuples = [
        [float(pointsLongLatList[i]),float(pointsLongLatList[i+1])]
        for i in range(0, len(pointsLongLatList) - 1, 2)]
    points = ee.Feature.MultiPoint(pointsLongLatTuples)

    # Remove starting character which indicates the product
    product = var[:1]
    var = var[1:]

    #Get the collection
    collection, coll_name, coll_desc, var_desc, notes = collectionMethods.get_collection(
        product, var)
    #Note: EE has a 2500 img limit per request
    #We need to split up larger data request into 5 year chunks
    #Max's suggestion: work with time and get data in chunks,
    dS_int = ee.Date(dS,'GMT').millis().getInfo()
    dE_int = ee.Date(dE,'GMT').millis().getInfo()
    ##dS_int = ee.Date(dS,'GMT').millis().getInfo()
    ##dE_int = ee.Date(dE,'GMT').millis().getInfo()
    step = 5 * 365 * 24 * 60 * 60 * 1000
    start = dS_int
    dataList = []
    while start < dE_int:
        if start + step < dE_int:
            end = start + step
        else:
            end = dE_int + 24 * 60 * 60 * 1000
        '''
        #First attempt at task queue, gives error
        #data = collection.filterDate(start, end).getRegion(points,1).slice(1).getInfo()
        AttributeError: 'unicode' object has no attribute 'filterDate')
        # Add the task to the default queue.
        q_params = {
            'collection':collection,
            'start':start,
            'end':end
        }
        data = taskqueue.add(url='/worker', params=q_params)
        '''
        data = collection.filterDate(start, end).getRegion(points,1).slice(1).getInfo()
        dataList+=data
        start+=step
    timeSeriesTextData,timeSeriesGraphData = figureFormatting.set_time_series_data(dataList,TV)

    '''
    #Code to get time series data viw getDownloadUrl -->
    #not working for requests > 6 years
    collection, coll_name, coll_desc, var_desc, notes = collectionMethods.get_collection(
        product, var)
    collection = collection.filterDate(dSUTC,dEUTC);
    collection = collection.getRegion(points,1);

    #check units
    #modify_units_in_timeseries(val,var,units):
    #collection =modify_units(collection, var, 'value', units);

    features = ee.FeatureCollection(
        ee.Feature(None, {'sample': collection}))
    downloadUrl = features.getDownloadUrl('json')
    response = urllib2.urlopen(downloadUrl)
    json_dict = json.loads(response.read())
    dataList = json_dict['features'][0]['properties']['sample']
    dataList.pop(0)
    timeSeriesTextData = []
    timeSeriesGraphData = []
    timeSeriesTextData, timeSeriesGraphData = figureFormatting.set_time_series_data(
        dataList,TV)
    '''
    source = coll_desc + ' from ' + dS + '-' + dE + ''
    #Set title
    title = statistic + ' ' + var_desc
    #Update template values
    extra_template_values = {
        'source_time':source,
        'title_time':title,
        'product_time':product,
        'productLongName_time':coll_desc,
        'variableShortName_time':var_desc,
        'timeSeriesData':timeSeriesTextData,
        'timeSeriesGraphData':json.dumps(timeSeriesGraphData),
        'notes_time': notes
    }
    TV.update(extra_template_values)
    return TV

#===========================================
#    GET_ANOMALY
#===========================================
def get_anomaly(collection, product, variable, dateStart, dateEnd,
                statistic, calculation, yearStartClim, yearEndClim):
    """Return the anomaly image collection

    Args:
        collection: EarthEngine collection to process
        product: string of the product ()
        variable: string of the variable ()
        dateStart: EarthEngine date object
        dateEnd: EarthEngine date object
        statistic: string of the statistic (Mean, Median, Total, etc.)
        calculation: string of the calculation type (anon, value, etc.)
        yearStartClim: string of the climatology start year
        yearEndClim: string of the climatology end year
    Returns:
        EarthEngine image collection object
        String of additional notes about the collection
    """
    #here calculation = ['anom','anompercentof','anompercentchange','clim'] only
    #here the collection has already chosen variable

    #get the day ranges
    doyStart = ee.Number(dateStart.getRelative('day', 'year')).add(1)
    doyEnd = ee.Number(dateEnd.getRelative('day', 'year')).add(1)
    doy_filter = ee.Filter.calendarRange(doyStart, doyEnd, 'day_of_year')

    #check if year Range <1 to ease calculations

    #get climatology
    climatologyNote = 'Climatology calculated from {0}-{1}'.format(
        yearStartClim, yearEndClim)

    #FilterDate needs an extra day on the high end
    yearStartClimUTC = ee.Date(yearStartClim+'-01-01', 'GMT')
    yearEndClimUTC = ee.Date(yearEndClim+'-12-31', 'GMT').advance(1,'day')

    #climatology = collection.filterDate(yearStartClim, str(int(yearEndClim)+1)).filter(doy_filter)
    climatology = collection.filterDate(yearStartClimUTC, yearEndClimUTC).filter(doy_filter)
    if statistic in ['Mean', 'Total', 'Median']:
        climatology = get_statistic(climatology,statistic)
    else: #need a solution for min/max
        climatology = get_statistic(climatology,statistic)

    #This metric is really only good for year ranges <1 year
    if statistic == 'Total':
         num_years = int(yearEndClim) - int(yearStartClim) + 1
         climatology = climatology.divide(num_years)

    #get statistic of collection
    collection = get_statistic(
        collection.filterDate(dateStart, dateEnd.advance(1,'day')), statistic)

    #calculate
    if calculation == 'clim':
        mask = collection.gt(-9999)
        climatology = climatology.mask(mask)
        collection = climatology
    elif calculation == 'anom':
        collection = ee.Image(collection.subtract(climatology))
    elif calculation == 'anompercentof':
        collection = ee.Image(collection.divide(climatology).multiply(100)) #anomaly
    elif calculation == 'anompercentchange':
        collection = ee.Image(collection.subtract(climatology).divide(climatology).multiply(100)) #anomaly

    return collection, climatologyNote

#===========================================
#   GET_STATISTIC
#===========================================
def get_statistic(collection, statistic):
    """"""
    if statistic == 'Mean':
         collection = collection.mean()
    elif statistic == 'Max':
         collection = collection.max()
    elif statistic == 'Min':
         collection = collection.min()
    elif statistic == 'Median':
         collection = collection.median()
    elif statistic == 'Total':
         collection = collection.sum()
    return collection

#===========================================
#   MODIFY_UNITS
#===========================================
def modify_units(collection, variable, calculation, units):
    """"""
    #don't modify if calculation == 'anompercentof' or 'anompercentchange'

    if calculation in ['value', 'clim', 'anom']:
        if variable in ['LST_Day_1km']:
            collection = collection.multiply(0.02);  #convert from unsigned 16-bit integer
        if variable in ['tmmx', 'tmmn', 'tmean','LST_Day_1km']:
            if calculation == 'anom' and units == 'english':
                collection = collection.multiply(1.8)    #convert C anom to F anom
            elif calculation == 'value' or calculation == 'clim':
                collection = collection.subtract(273.15)  #convert K to C
                if units == 'english': #convert C to F
                     collection = collection.multiply(1.8).add(32)
        elif variable in ['pr', 'pet', 'wb'] and units == 'english':
                collection = collection.divide(25.4) #convert mm to inches
        elif variable == 'vs' and units == 'english':
            collection = collection.multiply(2.23694) #convert m/s to mi/h
    return collection

#this is not currently being used.... need to fix this.. as time series units aren't being corrected
def modify_units_in_timeseries(val, var, units):
    """"""
    if var in ['LST_Day_1km']:
        val = val*0.02;  #convert from unsigned 16-bit integer
    if var in ['tmmx', 'tmmn', 'tmean','LST_Day_1km']:
        val = val - 273.15          #convert K to C
        if units == 'english':
            val = 1.8 * val + 32    #convert C to F
    elif var in ['pr', 'pet', 'wb'] and units == 'english':
        val = val / 25.4            #convert mm to inches
    elif var == 'vs' and units == 'english':
        val = 2.23694 * val         #convert m/s to mi/h
    return val

#===========================================
#   MAP_COLLECTION
#===========================================
def map_collection(collection, opacity, palette, minColorbar, maxColorbar):
    """"""
    colorbarOptions = {
        'min':minColorbar,
        'max':maxColorbar,
        'palette':palette,
        'opacity':opacity, #range [0,1]
    }
    mapid = collection.getMapId(colorbarOptions)
    return mapid
