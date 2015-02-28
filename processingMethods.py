import datetime as dt


import json
import logging, threading
import urllib2


import ee

import collectionMethods

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
    domainType = TV['domainType']
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

    #==============
    #Rectangle Data Extraction
    #==============
    if domainType == 'rectangle':
        NELat = TV['NELat']
        NELong = TV['NELong']
        SWLat = TV['SWLat']
        SWLong = TV['SWLong']
        rectangle = ee.Geometry.Rectangle(SWLong, SWLat, NELong, NELat)
        ## I think Export.image needs a string of coordinates, not a geometry object
        ## The following should work but there might be a cleaner way
        ##rectangle = ee.Geometry.Rectangle(SWLong, SWLat, NELong, NELat).toGeoJSON().coordinates
        extra_template_values['downloadURL'] =rectangle
        TV.update(extra_template_values)
        downloadOptions ={
            'name': 'test_image',
            'scale':4000,
            'crs': 'EPSG:4326',
            'region': rectangle
        }
        #downloadURL = '[['+NELong+','+NELat+'], ['+
        #               ' ['+SELong+','+NELat+'],['+
        #               ' ['+NELong+','+SELat+'],['+
        #               ' ['+SELong+','+SELat+']]'
        #downloadURL = ???Export.Image(,'title',{'region': rectangle})

    return TV

#===========================================
#    TIME_SERIES
#===========================================
def set_logger(name):
    '''
    Logger for debugging purposes
    Args:
        name: logger name
    Returns:
        python logger object
    '''
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    sh = logging.StreamHandler()
    sh.setLevel(logging.DEBUG)
    logger.addHandler(sh)
    return logger

def initialize_timeSeriesTextDataDict(point):
    '''
    Data for each point in time series
    is stored in a separate dictionary
    Args:
        point: [Lon, Lat]
    Returns:
        dictionary with keys: values
            LonLat: Long, Lat string
            Data: empty list
    '''
    data_dict = {
        'LongLat': '{0:0.4f},{1:0.4f}'.format(*point),
        'Data':[]
    }
    return data_dict

def initialize_timeSeriesGraphDataDict(point,marker_color):
    '''
    Graph data for each point in time series
    is stored in a separate dictionary
    Args:
        point: [Lon, Lat]
        marker_color: color of marker and plot
    Returns:
        dictionary with keys: values
            MarkerColor: marker_color
            LonLat: Long, Lat string
            Data: empty list
    '''

    data_dict_graph = {
        'MarkerColor':marker_color,
        'LongLat': '{0:0.4f},{1:0.4f}'.format(*point),
        'Data':[]
    }
    return data_dict_graph

def process_timeSeriesTextData(row_data,var,units):
    '''
    Processes row data returned by ee time series request.
    Args:
        row_data: [(long, lat),date,time,value]
        var: variable short name
        units: english or metric
    Returns:
        formatted data: [date_string, value_string]
    '''
    time_int = int(row_data[3])
    date_obj = dt.datetime.utcfromtimestamp(float(time_int) / 1000)
    date_str = date_obj.strftime('%Y-%m-%d')
    try:
        val = modify_units_in_timeseries(float(row_data[4]),var,units)
        return [date_str, '{0:0.4f}'.format(val)]
    except:
        return [date_str, 'None']

def process_timeSeriesGraphData(row_data,var,units):
    '''
    Process row data returned by ee time series request.
    Args:
        row_data: [(long, lat),date,time,value]
        var: variable short name
        units: english or metric
    Returns:
        formatted data: [date_integer, value_float]
    '''

    time_int = int(row_data[3])
    try:
        val = modify_units_in_timeseries(float(row_data[4]),var,units)
        return [time_int, val]
    except:
        return None

def process_threadData(point_data, var, units):
    '''
    Args:
        point_data: unformatted data returned by ee time series request
        var: variable short name
        units: english or metric
    Returns:
        time series data for text display
        time series graph data for plotting with highcharts
    '''
    ts_data = [];graph_data =[]
    for row_data in point_data:
        ts_row_data = process_timeSeriesTextData(row_data,var,units)
        graph_row_data = process_timeSeriesGraphData(row_data,var,units)
        if graph_row_data is not None:
            graph_data.append(graph_row_data)
        ts_data.append(ts_row_data)
    return sorted(ts_data), sorted(graph_data)

def get_time_series(template_values):
    """
    Args:
        template_values -- a dictionary of user and system input
    Returns:
        updated template_values with time series data
    """

    def ts_point_worker(collection,point,start,end,threadData,point_idx):
        '''
        Threading worker for time series.
        Applies getInfo call on collection filtered by dates and point
        Args:
            collection: ee ImageCollection
            point: ee.GeometryPoint
            start: integer time of start date
            end: integer time of end date
            threadData: list to store thread results
            point_idx: index to be populated in threaData
        Returns:
            error: None if no error was encountered
        '''
        try:
            p_data = collection.filterDate(start,end).getRegion(point,1).slice(1).getInfo()
            threadData[point_idx].append(p_data)
        except Exception, e:
            threadData[point_idx].append([])
            logger.error('EXCEPTION IN THREAD: '  + str(e))
            error = str(e)

    #Logger for debugging purposes
    logger = set_logger('ts_debug')

    #Keep track of errors
    error = None

    #Set variables
    TV = {}
    for key, val in template_values.iteritems():
        TV[key] = val
    var = TV['variable']
    mc = TV['marker_colors']
    dS = TV['dateStart']
    dE = TV['dateEnd']
    statistic = TV['statistic']
    units = TV['units']

    #Set points
    pointsLongLatList = str(TV['pointsLongLat']).replace(' ','').split(',')
    pointsLongLatPairs = [
        [float(pointsLongLatList[i]),float(pointsLongLatList[i+1])]
        for i in range(0, len(pointsLongLatList) - 1, 2)]

    # Remove starting character which indicates the product
    product = var[:1]
    var = var[1:]

    #Get the collection and set some new template variables
    collection, coll_name, coll_desc, var_desc, notes = collectionMethods.get_collection(
        product, var)
    source = coll_desc + ' from ' + dS + '-' + dE + ''
    title = statistic + ' ' + var_desc
    extra_template_values = {
        'source_time':source,
        'title_time':title,
        'product_time':product,
        'productLongName_time':coll_desc,
        'variableShortName_time':var_desc,
        'notes_time': notes
    }


    #Note: EE has a 2500 img limit per request
    #We need to split up larger data request into smaller chunks
    #Max's suggestion: work with time and get data in chunks,
    dS_int = ee.Date(dS, 'GMT').millis().getInfo()
    dE_int = ee.Date(dE, 'GMT').millis().getInfo()

    #Set time step
    step = 5 * 365 * 24 * 60 * 60 * 1000

    #Start a thread for each point and time chunk
    #Save the threads and data in the apporpriate slot in a list
    threads =[[] for p in pointsLongLatPairs]
    threadData = [[] for p in pointsLongLatPairs];
    t_idx = -1
    for p_idx, p in enumerate(pointsLongLatPairs):
        point = ee.Geometry.Point(p)
        start = dS_int
        while start < dE_int:
            t_idx+=1
            if start + step < dE_int:
                end = start + step
            else:
                end = dE_int + 24 * 60 * 60 * 1000
            t_args = (collection,point,start,end,threadData,p_idx)
            logger.info('STARTING THREAD FOR TIME SLICE %s, POINT %s' %(str(t_idx+1),str(p_idx + 1)))
            t = threading.Thread(target=ts_point_worker, args = t_args)
            threads[p_idx].append(t)
            t.start()
            start+=step

    #Check for errors in threading
    if error is not None:
        extra_template_values['timeSeriesData'] = []
        extra_template_values['timeSeriesGraphData'] = []
        extra_template_values['ts_error'] = str(error)
        TV.update(extra_template_values)
        return TV

    #Combine threading results
    timeSeriesTextData = [];timeSeriesGraphData = []
    for p_idx,point in enumerate(pointsLongLatPairs):
        marker_color = mc[p_idx]
        data_dict_ts = initialize_timeSeriesTextDataDict(point)
        data_dict_graph = initialize_timeSeriesGraphDataDict(point,marker_color)
        point_data =[]
        for t_idx in range(len(threads[p_idx])):
            try:
                threads[p_idx][t_idx].join()
                point_data+=threadData[p_idx][t_idx]
                logger.info('THREAD FINISHED AND DATA APPENDED')
            except Exception, e:
                logger.error(str(e).upper())
                error = str(e)
                extra_template_values['timeSeriesData'] = []
                extra_template_values['timeSeriesGraphData'] = []
                extra_template_values['ts_error'] = str(error)
                TV.update(extra_template_values)
                return TV
        data_dict_ts['Data'],data_dict_graph['Data'] = process_threadData(point_data, var, units)
        timeSeriesTextData.append(data_dict_ts)
        timeSeriesGraphData.append(data_dict_graph)

    #logger.info(timeSeriesGraphData)
    logger.info('TIME SERIES DATA FORMATTED')

    #Update template values
    extra_template_values['timeSeriesData'] = timeSeriesTextData
    extra_template_values['timeSeriesGraphData'] = json.dumps(timeSeriesGraphData)
    TV.update(extra_template_values)
    return TV


#===========================================
#    GET_ANOMALY
#===========================================
def get_anomaly(collection, product, variable, dateStart, dateEnd,
                statistic, calculation, yearStartClim, yearEndClim):
    """Return the anomaly image collection

    Args:
        collection: EarthEngine collection to process (has already selected variable)
        product: string of the product ()
        variable: string of the variable ()
        dateStart: string of the start date isoformat (YYYY-MM-DD)
        dateEnd: string of the end date isoformat (YYYY-MM-DD)
        statistic: string of the statistic (Mean, Median, Total, etc.)
        calculation: string of the calculation type (anom, value, anompercentof,anompercentchange,clim)
        yearStartClim: string of the climatology start year
        yearEndClim: string of the climatology end year
    Returns:
        EarthEngine image collection object
        String of additional notes about the collection
    """

    #Build python datetime objects from the date string
    dateStart_dt = dt.datetime.strptime(dateStart, '%Y-%m-%d')
    dateEnd_dt = dt.datetime.strptime(dateEnd, '%Y-%m-%d')

    #Check timedelta between start and end is greater than 1 year
    def yearsahead(years, start_date):
        try:
           return start_date.replace(year=start_date.year + years)
        except:   # Must be 2/29!
           assert from_date.month == 2 and from_date.day == 29 # can be removed
           return from_date.replace(month=2, day=28, year=start_date.year+years)
    if dateEnd_dt > yearsahead(1,dateStart_dt):
        sub_year_flag = True
        doyStart = 1
        doyEnd = 366
    else:
        sub_year_flag = False
        doyStart = dateStart_dt.timetuple().tm_yday
        doyEnd = dateEnd_dt.timetuple().tm_yday

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
    elif(statistic == 'Mean' or statistic == 'Total' or statistic == 'Median'):
        doy_filter = ee.Filter.calendarRange(doyStart, doyEnd, 'day_of_year')
        #FilterDate needs an extra day on the high end,Set yearEnd to Jan 1st of next year
        yearStartClimUTC = dt.datetime(int(yearStartClim), 1, 1)
        yearEndClimUTC = dt.datetime(int(yearEndClim)+1, 1, 1)
        climatology = collection.filterDate(yearStartClimUTC, yearEndClimUTC).filter(doy_filter)
        if sub_year_flag == False:
            climatology = get_statistic(climatology,statistic)
            if(statistic == 'Total'):
                num_years = int(yearEndClim) - int(yearStartClim) + 1
                climatology = climatology.divide(num_years)
        #else: #this is where charles inserts his magic
        #need to figure out how to make a collection of copies of climatology for each doy
        #in the dateStart to dateEnd range and then perform statistic over those images
            #climatology = get_statistic(climatology,statistic)

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

    climatologyNote = 'Climatology calculated from {0}-{1}'.format(
        yearStartClim, yearEndClim)

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
            collection = collection.multiply(0.02)  #convert from unsigned 16-bit integer
        if variable in ['tmmx', 'tmmn', 'tmean', 'LST_Day_1km']:
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
    new_val = val
    if var in ['LST_Day_1km']:
        new_val = val * 0.02  #convert from unsigned 16-bit integer
    if var in ['tmmx', 'tmmn', 'tmean', 'LST_Day_1km']:
        new_val = val - 273.15          #convert K to C
        if units == 'english':
            new_val = 1.8 * val + 32    #convert C to F
    elif var in ['pr', 'pet', 'wb'] and units == 'english':
        new_val = val / 25.4            #convert mm to inches
    elif var == 'vs' and units == 'english':
        new_val = 2.23694 * val         #convert m/s to mi/h
    return new_val

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
