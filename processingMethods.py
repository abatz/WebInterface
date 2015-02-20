import datetime as dt
import json
import logging
import urllib2

import ee
from google.appengine.api.labs import taskqueue

import collectionMethods
import figureFormatting

#===========================================
#   GET_IMAGES
#===========================================
def get_images(template_values):
    """"""
    #from forms import stateLat, stateLong

    TV = {}
    for key, val in template_values.iteritems():
        TV[key] = val
    var = TV['variable']
    calculation = TV['calculation']
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
            collection, product, var, dS, dE, statistic,
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
    dS_int = ee.Date(dS, 'GMT').millis().getInfo()
    dE_int = ee.Date(dE, 'GMT').millis().getInfo()
    ##dS_int = 1000 * calendar.timegm(dt.datetime.strptime(dS, '%Y-%m-%d').timetuple())
    ##dE_int = 1000 * calendar.timegm(dt.datetime.strptime(dE, '%Y-%m-%d').timetuple())
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
        dateStart: string of the start date isoformat (YYYY-MM-DD)
        dateEnd: string of the end date isoformat (YYYY-MM-DD)
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

    #Build python datetime objects from the date string
    dateStart_dt = dt.datetime.strptime(dateStart, '%Y-%m-%d')
    dateEnd_dt = dt.datetime.strptime(dateEnd, '%Y-%m-%d')

    #Check timedelta between start and end is greater than 365 (366 instead?)
    #Could also separate date to components and add a year
    #Can EE dates be compared?  That might be an easier approach also
    if dateEnd_dt > (dateStart_dt + dt.timedelta(days=365)):
        sub_year_flag = True
    else:
        sub_year_flag = False

    #Get the start and end DOY for filtering using calendarRange
    doyStart = dateStart_dt.timetuple().tm_yday
    doyEnd = dateEnd_dt.timetuple().tm_yday
    doy_filter = ee.Filter.calendarRange(doyStart, doyEnd, 'day_of_year')

    #get climatology
    climatologyNote = 'Climatology calculated from {0}-{1}'.format(
        yearStartClim, yearEndClim)
    #FilterDate needs an extra day on the high end,Set yearEnd to Jan 1st of next year
    yearStartClimUTC = dt.datetime(int(yearStartClim), 1, 1)
    yearEndClimUTC = dt.datetime(int(yearEndClim)+1, 1, 1)

    climatology = collection.filterDate(yearStartClimUTC, yearEndClimUTC).filter(doy_filter)
    if statistic == 'Min':
        #List sequence is inclusive (i.e. don't advance yearEnd)
        yearListClim = ee.List.sequence(int(yearStartClim),int(yearEndClim))
        def min_climatology_func(year):
            """For each year, return an image of the minimum value over the DOY range"""
            return ee.Image(collection\
                .filter(ee.Filter.calendarRange(year, year, 'year'))\
                .filter(ee.Filter.calendarRange(doyStart, doyEnd, 'day_of_year')).min())
        climatology = ee.ImageCollection.fromImages(yearListClim.map(min_climatology_func))
        climatology = get_statistic(climatology, 'Mean')
    elif statistic == 'Max':
        #List sequence is inclusive (i.e. don't advance yearEnd)
        yearListClim = ee.List.sequence(int(yearStartClim),int(yearEndClim))
        def max_climatology_func(year):
            """For each year, return an image of the maximum value over the DOY range"""
            return ee.Image(collection\
                .filter(ee.Filter.calendarRange(year, year, 'year'))\
                .filter(ee.Filter.calendarRange(doyStart, doyEnd, 'day_of_year')).max())
        climatology = ee.ImageCollection.fromImages(yearListClim.map(max_climatology_func))
        climatology = get_statistic(climatology, 'Mean')
    else: #'Mean','Total','Median'
        climatology = get_statistic(climatology,statistic)

    #This metric is really only good for year ranges <1 year
    if statistic == 'Total' and sub_year_flag==True:
         num_years = int(yearEndClim) - int(yearStartClim) + 1
         climatology = climatology.divide(num_years)

    #get statistic of collection
    #filterDate is exclusive on end date
    collection = get_statistic(
        collection.filterDate(dateStart_dt, dateEnd_dt + dt.timedelta(days=1)), statistic)

    #calculate
    if calculation == 'clim':
        #mask = collection.gt(-9999)
        #climatology = climatology.mask(mask)
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
