import datetime
import json
import logging
import urllib2

import ee

import collectionMethods
import figureFormatting
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
    aOV = TV['anomOrValue']
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

    #change date to UTC and add 1 for end date exclusiveness
    dSUTC = ee.Date(dS,'GMT');
    dEUTC = ee.Date(dE,'GMT').advance(1,'day');

    # Remove starting character which indicates the product
    product = var[:1]
    var = var[1:]

    #==============
    #Collection
    #==============
    #Get initial collection
    collection, coll_name, coll_desc, var_desc, notes = collectionMethods.get_collection(product, var)

    #==============
    #Title and Source
    #==============
    #Set title
    title = statistic + ' ' + var_desc
    if aOV == 'clim':
        title = title + ' Climatology '
    elif aOV == 'anom':
        title = title + ' Difference from Climatology '
    elif aOV == 'anompercentchange':
        title = title + ' Percent Difference from Climatology '
    elif aOV == 'anompercentof':
        title = title + ' Percent Of Climatology '

    #Set source, domain, subdomain
    source = coll_desc + ' from ' + dS + '-' + dE + ''

    #==============
    #Anomaly
    #==============
    if aOV in ['value']:
        collection = collection.filterDate(dSUTC,dEUTC)
        collection = get_statistic(collection, statistic)
    elif aOV in ['anom','anompercentof','anompercentchange','clim']:
        collection, climatologyNotes = get_anomaly(
            collection, product, var, coll_name, dSUTC, dEUTC, statistic,
            aOV, yearStartClim, yearEndClim)
        TV['climatologyNotes'] = climatologyNotes
    #==============
    #Units
    #==============
    collection = modify_units(collection, var, aOV, units)

    #==============
    #Get mapid
    #==============
    mapid = {'mapid':[],'token':[]}
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
    #Modify dates to give UTC and to add one to end date for exclusive python nature of this
    #dSUTC = ee.Date(dS,'GMT')
    #dEUTC = ee.Date(dE,'GMT').advance(1,'day')

    #Note: EE has a 2500 img limit per request
    #We need to split up larger data request into 5 year chunks
    #Max's suggestion: work with time and get data in chunks,
    #FIX ME: Avoid getInfo(), currently the .cat is not working as expected
    #This might be because data is a list of lists?
    dS_int = ee.Date(dS,'GMT').millis().getInfo()
    dE_int = ee.Date(dE,'GMT').millis().getInfo()
    step = 5 * 365 * 24 * 60 * 60 * 1000
    start = dS_int
    dataList = []
    #dataList = ee.List([])
    while start < dE_int:
        if start + step < dE_int:
            end = start + step
        else:
            end = dE_int + 24 * 60 * 60 * 1000
        #data = collection.filterDate(start, end).select(var).getRegion(points,1).slice(1)
        #dataList.cat(data)
        data = collection.filterDate(start, end).select(var).getRegion(points,1).slice(1).getInfo()
        dataList+=data
        start+=step
    #dataList = dataList.getInfo()
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
def get_anomaly(collection, product, variable, coll_name, dateStart,
                dateEnd, statistic, anomOrValue, yearStartClim, yearEndClim):
    """"""
    #here anomOrValue =['anom','anompercentof','anompercentchange','clim'] only
    #here the collection has already chosen variable

    #get the day ranges
    doyStart = ee.Number(ee.Algorithms.Date(dateStart).getRelative('day', 'year')).add(1)
    doyEnd = ee.Number(ee.Algorithms.Date(dateEnd).getRelative('day', 'year')).add(1)
    doy_filter = ee.Filter.calendarRange(doyStart, doyEnd, 'day_of_year')

    #check if year Range <1 to ease calculations


    #get climatology
    climatologyNote = 'Climatology calculated from {0}-{1}'.format(
        yearStartClim, yearEndClim)
    climatology = collection.filterDate(yearStartClim, str(int(yearEndClim)+1)).filter(doy_filter)
    if(statistic=='Mean' or statistic =='Total' or statistic=='Median'):
        climatology = get_statistic(climatology,statistic)
    else: #need a solution for min/max
        climatology = get_statistic(climatology,statistic)

    #This metric is really only good for year ranges <1 year
    if statistic == 'Total':
         num_years = int(yearEndClim) - int(yearStartClim) + 1
         climatology = climatology.divide(num_years)

    #get statistic of collection
    collection = get_statistic(collection.filterDate(dateStart, dateEnd), statistic)

    #calculate
    if anomOrValue == 'clim':
        mask = collection.gt(-9999)
        climatology = climatology.mask(mask)
        collection = climatology
    elif anomOrValue == 'anom':
        collection = ee.Image(collection.subtract(climatology))
    elif anomOrValue == 'anompercentof':
        collection = ee.Image(collection.divide(climatology).multiply(100)) #anomaly
    elif anomOrValue == 'anompercentchange':
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
def modify_units(collection, variable, anomOrValue, units):
    """"""
    #don't modify if anomOrValue == 'anompercentof' or 'anompercentchange'

    if anomOrValue in ['value', 'clim', 'anom']:
        if variable in ['tmmx', 'tmmn', 'tmean']:
            if anomOrValue == 'anom' and units == 'english':
                collection = collection.multiply(1.8)    #convert C anom to F anom
            elif anomOrValue == 'value' or anomOrValue == 'clim':
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
    if var in ['tmmx', 'tmmn', 'tmean']:
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
