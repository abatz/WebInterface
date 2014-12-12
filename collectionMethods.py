import ee
import time
import datetime
import numpy
import json

#===========================================
#   GET_IMAGES
#===========================================
def get_images(template_values):
    from forms import stateLat, stateLong

    TV = {}
    for key, val in template_values.iteritems():
        TV[key] = val
    var = TV['variable'];aOV = TV['anomOrValue']
    dT = TV['domainType']
    dS = TV['dateStart']; dE = TV['dateEnd']
    pointsLongLat = str(TV['pointsLongLat']) #string of comma separates llon,lat pairs
    pointsLongLatList = pointsLongLat.split(',')
    pointsLongLatTuples = [[float(pointsLongLatList[i]),float(pointsLongLatList[i+1])] for i in range(0,len(pointsLongLatList) - 1,2)]
    #get map palette options
    palette,minColorbar,maxColorbar,colorbarLabel=get_colorbar(str(var),str(aOV))
    #Override max/minColorbar if user entered custom value
    if 'minColorbar' in template_values.keys():
        minColorbar = template_values['minColorbar']
    if 'maxColorbar' in template_values.keys():
        maxColorbar = template_values['maxColorbar']
    if 'palette' in template_values.keys():
        palette = template_values['palette']
    #get collection
    collection,collectionName,collectionLongName,product,variableShortName,notes,statistic=get_collection(var);
    #Set title
    title = statistic + ' ' + variableShortName;
    if(aOV == 'anom'):
        title = title + ' Anomaly from Climatology ';
    #Set source, domain, subdomain
    source = collectionLongName + ' from ' + dS + '-' + dE + ''
    points = None
    subdomain = ee.Feature.MultiPoint(pointsLongLatTuples)
    if(dT == 'states'):
        subdomain = template_values['state']
        mapzoom=4; #would like to zoom in on that state
    elif(dT == 'full' and product == 'modis'):
        points = subdomain
        mapzoom=4
    elif(dT=='full' and product=='gridded'):
        points = subdomain
        mapzoom=5
    elif(dT=='rectangle'):
        subdomain = ee.Feature.Rectangle(float(TV['SWLong']),float(TV['SWLat']),float(TV['NELong']),float(TV['NELat']))
        points = subdomain
        mapzoom=4
    else:
        points = subdomain
        mapzoom=4
    timeSeriesData = [];timeSeriesGraphData =[]
    mapid = {'mapid':[],'token':[]}
    if var == 'wb':
        #FIX ME: implement time series for wb
        collection_pr = ee.ImageCollection(collectionName).filterDate(dS,dE).select(['pr'],['pr'])
        collection_pet = ee.ImageCollection(collectionName).filterDate(dS,dE).select(['pet'],['pet'])
        collection_pr = get_statistic(collection_pr,'pr',statistic,'value');
        collection_pet = get_statistic(collection_pet,'pet',statistic,'value')
        collection_pr =filter_domain2(collection_pr,dT,subdomain)
        collection_pet =filter_domain2(collection_pet,dT,subdomain)
        #form water balance
        collection = collection_pr.subtract(collection_pet)
        if  aOV in ['anom','clim']:
            collection,climatologyNotes = get_anomaly(collection,product,var,collectionName,dS,dE,statistic,aOV)
            TV['climatologyNotes'] = climatologyNotes
        #the earth engine call
        mapid = map_collection(collection,TV['opacity'],palette,minColorbar,maxColorbar)
    else:
        collection = ee.ImageCollection(collectionName).filterDate(dS,dE).select([var],[var])
        #Time Series
        if  dT == 'points' and points:
            timeSeriesData, timeSeriesGraphData = get_time_series(collection,var,pointsLongLatTuples)
        #collection = filter_domain1(collection,dT, subdomain)
        else:
            collection = get_statistic(collection,var,statistic,aOV);
            collection = filter_domain2(collection,dT,subdomain)
            if  aOV in ['anom','clim']:
                collection,climatologyNotes = get_anomaly(collection,product,var,collectionName,dS,dE,statistic,aOV)
                TV['climatologyNotes'] = climatologyNotes
            #the earth engine call
            mapid = map_collection(collection,TV['opacity'],palette,minColorbar,maxColorbar)
    #Update template values
    extra_template_values = {
        'source': source,
        'product':product,
        'productLongName': collectionLongName,
        'title': title,
        'palette': palette,
        'colorbarLabel': colorbarLabel,
        'minColorbar': minColorbar,
        'maxColorbar': maxColorbar
    }
    if mapid and mapid['mapid'] and mapid['token']:
        extra_template_values['mapid'] = mapid['mapid']
        extra_template_values['token'] = mapid['token']
    elif timeSeriesGraphData and timeSeriesData:
        extra_template_values['timeSeriesData'] = timeSeriesData
        extra_template_values['timeSeriesGraphData'] = timeSeriesGraphData
    TV.update(extra_template_values)
    return TV
'''
def get_images(template_values):
    from forms import stateLat, stateLong;

    TV = {}
    for key, val in template_values.iteritems():
        TV[key] = val
    var = TV['variable'];aOV = TV['anomOrValue']
    dT = TV['domainType']
    dS = TV['dateStart']; dE = TV['dateEnd']
    pointsLongLat = TV['pointsLongLat'] #string of comma separates llon,lat pairs
    pointsLongLatList = pointsLongLat.split(',')
    pointsLongLatTuples = [(float(pointsLongLatList[i]),float(pointsLongLatList[i+1])) for i in range(0,len(pointsLongLatList) - 1,2)]
    multi_point = False
    if len(pointsLongLatList) > 2:
        multi_point = True
        subdomain = ee.Feature.MultiPoint(pointsLongLatTuples)
    else:
        subdomain = ee.Feature.Point(float(pointsLongLatList[0]),float(pointsLongLatList[1]))
    #get map palette options
    palette,minColorbar,maxColorbar,colorbarLabel=get_colorbar(str(var),str(aOV))
    #Override max/minColorbar if user entered custom value
    if 'minColorbar' in template_values.keys():
        minColorbar = template_values['minColorbar']
    if 'maxColorbar' in template_values.keys():
        maxColorbar = template_values['maxColorbar']
    if 'palette' in template_values.keys():
        palette = template_values['palette']
    #get collection
    collection,collectionName,collectionLongName,product,variableShortName,notes,statistic=get_collection(var);
    #Set title
    title = statistic + ' ' + variableShortName;
    if(aOV == 'anom'):
        title = title + ' Anomaly from Climatology ';
    #Set source, domain, subdomain
    source = collectionLongName + ' from ' + dS + '-' + dE + ''
    points = None
    if(dT == 'states'):
        subdomain = template_values['state']
        mapzoom='7'; #would like to zoom in on that state
    elif(dT == 'full' and product == 'modis'):
        points = subdomain
        mapzoom='4'
    elif(dT=='full' and product=='gridded'):
        points = subdomain
        mapzoom='5'
    elif(dT=='rectangle'):
        subdomain = ee.Feature.Rectangle(float(TV['SWLong']),float(TV['SWLat']),float(TV['NELong']),float(TV['NELat']))
        points = subdomain
        mapzoom='4'
    else:
        points = subdomain
        mapzoom='4'

    timeSeriesDataPoints = []
    if var == 'wb':
        #FIX ME: implements tiem series for wb
        collection_pr = ee.ImageCollection(collectionName).filterDate(dS,dE).select(['pr'],['pr'])
        collection_pet = ee.ImageCollection(collectionName).filterDate(dS,dE).select(['pet'],['pet'])
        collection_pr = get_statistic(collection_pr,'pr',statistic,'value');
        collection_pet = get_statistic(collection_pet,'pet',statistic,'value');
        collection_pr =filter_domain2(collection_pr,dT,subdomain)
        collection_pet =filter_domain2(collection_pet,dT,subdomain)
        #form water balance
        collection = collection_pr.subtract(collection_pet);
    else:
        collection = ee.ImageCollection(collectionName).filterDate(dS,dE).select([var],[var])
        #Time Series
        if  dT == 'points' and points:
            #FIX ME, can we get TS data for MultiPoint and oly have to query once?
            #get data for each point
            for p in pointsLongLatTuples:
                point = ee.Feature.Point(p[0],p[1])
                timeSeriesData, timeSeriesGraphData = get_time_series(collection,var,point)
                data = {
                    'LongLat':str(p[0]) +',' + str(p[1]),
                    'timeSeriesData':timeSeriesData,
                    'timeSeriesGraphData':timeSeriesGraphData
                }
                timeSeriesDataPoints.append(data)
        #collection = filter_domain1(collection,dT, subdomain)
        collection = get_statistic(collection,var,statistic,aOV);
        collection = filter_domain2(collection,dT,subdomain)
    if  aOV in ['anom','clim']:
        collection,climatologyNotes = get_anomaly(collection,product,var,collectionName,dS,dE,statistic,aOV)
        TV['climatologyNotes'] = climatologyNotes

    #the earth engine call
    mapid = map_collection(collection,TV['opacity'],palette,minColorbar,maxColorbar)
    #mapid = map_collection(collection,var,aOV,TV['opacity'],palette,minColorbar,maxColorbar)


    extra_template_values = {
        'mapid': mapid['mapid'],
        'token': mapid['token'],
        'timeSeriesDataPoints':timeSeriesDataPoints,
        'source': source,
        'product':product,
        'productLongName': collectionLongName,
        'title': title,
        'palette': palette,
        'colorbarLabel': colorbarLabel,
        'minColorbar': minColorbar,
        'maxColorbar': maxColorbar
    }
    TV.update(extra_template_values)
    return TV
'''
#===========================================
#    GET_COLLECTION
#===========================================
def get_collection(variable):
    if(variable=='NDVI'):
        collectionName = 'MCD43A4_NDVI';
        collectionLongName = 'MODIS 16-day NDVI'
        product = 'modis'
        notes="NDVI calculated from Norm. Diff. of Infrared and Red bands"
        statistic='Median'
        variableShortName=variable;
    elif(variable=='NDSI'):
        collectionName = 'MCD43A4_NDSI';
        collectionLongName = 'MODIS 16-day NDSI Composite'
        product = 'modis'
        notes="NDSI calculated from Norm. Diff. of Green and mid-IR bands"
        statistic='Median'
        variableShortName=variable;
    elif(variable=='NDWI'):
        collectionName = 'MCD43A4_NDWI';
        collectionLongName = 'MODIS 16-day NDWI Composite'
        product = 'modis'
        notes="NDWI calculated from near-IR and a second IR bands"
        statistic='Median'
        variableShortName=variable;
    elif(variable=='EVI'):
        collectionName = 'MCD43A4_EVI';
        collectionLongName = 'MODIS 16-day EVI Composite'
        product = 'modis'
        notes="EVI calculated from Near-IR,Red and Blue bands"
        statistic='Median'
        variableShortName=variable;
    elif(variable=='pr'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Total'
        variableShortName='Precipitation'
    elif(variable=='tmmx'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Mean'
        variableShortName='Maximum Temperature'
    elif(variable=='tmmn'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Mean'
        variableShortName='Minimum Temperature'
    elif(variable=='rmin'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Mean'
        variableShortName='Minimum Relative Humidity'
    elif(variable=='rmax'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Mean'
        variableShortName='Maximum Relative Humidity'
    elif(variable=='srad'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Mean'
        variableShortName='Downwelling Shortwave Radiation'
    elif(variable=='vs'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Mean'
        variableShortName='Wind Speed Near Surface'
    elif(variable=='sph'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Mean'
        variableShortName='Specific Humidity'
    elif(variable=='erc'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Mean'
        variableShortName='Energy Release Component'
    elif(variable=='pet'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Total'
        variableShortName='Potential Evapotranspiration'
    elif(variable=='wb'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Total'
        variableShortName='Water Balance (PPT-PET)'
    elif(variable=='pdsi'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Mean'
        variableShortName='Water Balance (PPT-PET)'

    collection = ee.ImageCollection(collectionName).select([variable],[variable]);

    return (collection,collectionName,collectionLongName,product,variableShortName,notes,statistic);

#===========================================
#    GET_TIMESERIES
#===========================================
def get_time_series(collection, variable, pointsLongLatTuples):
    ######################################################
    #### Data in list format
    ######################################################
    timeSeriesData = []
    timeSeriesGraphData = []
    points = ee.Feature.MultiPoint(pointsLongLatTuples)
    dataList = collection.getRegion(points,1).getInfo()
    '''
    try:
        dataList = collection.getRegion(points,1).getInfo()
    except:
        return timeSeriesData
    '''
    dataList.pop(0) #remove first row of list ["id","longitude","latitude","time",variable]
    ######################################################
    #### Format data for figure and data tabs
    #### Ech point gets it's own dictionary
    #### timeSeriesData = {LongLat:ll_string, Data:[[Date1,val1],[Date2, val2]]}
    ######################################################
    #Format data
    for idx, data in enumerate(dataList):
        lon = round(data[1],4);lat = round(data[2],4)
        if idx == 0:
            #To keep track of when data point changes
            lon_init = lon;lat_init = lat
            data_dict = {}
            data_dict_graph = {}
        else:
            if abs(float(lon) - float(lon_init)) >0.0001 or abs(float(lat) - float(lat_init)) > 0.0001:
                #New data point
                lon_init = lon;lat_init = lat
                timeSeriesData.append(data_dict)
                timeSeriesGraphData.append(data_dict_graph)
                data_dict = {};data_dict_graph = {}
        if not data_dict:
            data_dict = {
                'LongLat': str(lon) + ',' + str(lat),
                'Data': []
            }
            data_dict_graph = {
                'LongLat': str(lon) + ',' + str(lat),
                'Data': []
            }
        date_string = str(data[0])
        time = int(data[3])
        try:
            date_string = date_string[0:4] + '-' + date_string[4:6] + '-' + date_string[6:8]
        except:
            pass
        val = data[4]
        data_dict['Data'].append([date_string,val])
        data_dict_graph['Data'].append([time,val])
    timeSeriesData.append(data_dict)
    timeSeriesGraphData.append(data_dict_graph)
    return timeSeriesData,timeSeriesGraphData
'''
def get_time_series(collection, variable, point):
    ######################################################
    #### Data in list format
    ######################################################
    dataString = collection.getRegion(point,1).getInfo()
    dataString.pop(0) #remove first row of list ["id","longitude","latitude","time",variable]
    timeList = [row[3] for row in dataString]
    variableList = [row[4] for row in dataString]
    ######################################################
    #### CREATE TIME SERIES ARRAY WITH DATE IN COL 1 AND VALUE IN COL 2
    ######################################################
    timeSeriesData = []
    for i in range(0,len(variableList),1):
        time_ms = (ee.Algorithms.Date(dataString[i][3])).getInfo()['value']
        data1 = time.strftime('%m/%d/%Y',  time.gmtime(time_ms/1000))
        data2 = (dataString[i][4])
        if data2 is not None:
            timeSeriesData.append([data1,data2])
    ######################################################
    #### SORT IN CHRONOLOGICAL ORDER
    ######################################################
    timeSeriesData.sort(key=lambda date: datetime.datetime.strptime(date[0], "%m/%d/%Y"))
    ######################################################
    #### ADD HEADER TO SORTED LIST
    ######################################################
    timeSeriesData = [['Dates','Values']] + timeSeriesData
    ######################################################
    #### GET GRAPH DATA
    ######################################################
    timeSeriesGraphData = []
    n_rows = numpy.array(timeSeriesData).shape[0]
    for i in range(2,n_rows):
        entry = {'count':timeSeriesData[i][1],'name':timeSeriesData[i][0]}
        timeSeriesGraphData.append(entry)
    return timeSeriesData, timeSeriesGraphData


def callTimeseries(collection,variable,domainType,point):
    if(domainType=='points'):
        timeSeriesData=get_timeseries(collection,point,variable)
        timeSeriesGraphData = []
        n_rows = numpy.array(timeSeriesData).shape[0];
        for i in range(2,n_rows):
            entry = {'count':timeSeriesData[i][1],'name':timeSeriesData[i][0]};
            timeSeriesGraphData.append(entry);

    template_values = {
        'timeSeriesData': timeSeriesData,
        'timeSeriesGraphData': timeSeriesGraphData,
    }
    return (timeSeriesData,timeSeriesGraphData,template_values);
'''
#===========================================
#    GET_ANOMALY
#===========================================
def get_anomaly(collection,product,variable,collectionName,dateStart,dateEnd,statistic,anomOrValue):
    doyStart = ee.Number(ee.Algorithms.Date(dateStart).getRelative('day', 'year')).add(1);
    doyEnd = ee.Number(ee.Algorithms.Date(dateEnd).getRelative('day', 'year')).add(1);
    doy_filter = ee.Filter.calendarRange(doyStart, doyEnd, 'day_of_year');

    if(product=='gridded'):
        yearStartClim ='1981';
        yearEndClim='2010';
    elif(product=='landsat'):
        yearStartClim ='1999';
        yearEndClim='2010';
    elif(product=='modis'):
        yearStartClim ='2000';
        yearEndClim='2010';
    num_years = int(yearEndClim) - int(yearStartClim) + 1;
    climatologyNote='Climatology calculated from '+yearStartClim+'-'+yearEndClim;

    #calculate climatology
    if(variable=='wb'):
        climatology_pr = ee.ImageCollection(collectionName).filterDate(yearStartClim, yearEndClim).filter(doy_filter).\
           select(['pr'],['pr']);
        climatology_pet = ee.ImageCollection(collectionName).filterDate(yearStartClim, yearEndClim).filter(doy_filter).\
           select(['pet'],['pet']);
    else:
        climatology = ee.ImageCollection(collectionName).filterDate(yearStartClim, yearEndClim).filter(doy_filter).select([variable],[variable]);

    if(variable=='wb'):
         climatology_pr = ee.Image(climatology_pr.sum().divide(num_years));
         climatology_pet = ee.Image(climatology_pet.sum().divide(num_years));
	 climatology = climatology_pr.subtract(climatology_pet);
	 climatology_sd = climatology.reduce(ee.Reducer.stdDev());
    elif(statistic=='Total' and variable=='pr'):
         climatology = ee.Image(climatology.sum().divide(num_years));
    elif(statistic=='Total' and variable=='pet'):
         climatology = ee.Image(climatology.sum().divide(num_years));
    elif(statistic=='Median'):
         climatology = ee.Image(climatology.median());
    elif(statistic=='Mean' and variable=='erc'):
         climatology = ee.Image(climatology.mean());
    elif(statistic=='Mean'):
         climatology = ee.Image(climatology.mean());

    if(anomOrValue=='clim'):
        if((variable=='tmmx' or variable=='tmmn')):
            climatology=climatology.subtract(273.15)   #convert to C
            #climatology=climatology.subtract(273.15).multiply(1.8).add(32); #convert to F
        mask = collection.gt(-9999);
        climatology = climatology.mask(mask);
        collection=climatology;
    elif(anomOrValue=='anom'):
        #calculate anomaly
        if(statistic=='Total' and variable=='pr'):
            collection = ee.Image(collection.divide(climatology).multiply(100)); #anomaly
        elif(statistic=='Total' and variable=='pet'):
            collection = ee.Image(collection.divide(climatology).multiply(100)); #anomaly
        elif(statistic=='Median'):
            collection = ee.Image(collection.subtract(climatology)); #anomaly
        elif(statistic=='Mean' and variable=='sph'):
            collection = ee.Image(collection.subtract(climatology).divide(climatology).multiply(100));
        elif(statistic=='Mean'):
            collection = ee.Image(collection.subtract(climatology));
        elif(variable=='wb'):
            collection = ee.Image(collection.subtract(climatology).divide(climatology_sd));

    return(collection,climatologyNote);

#===========================================
#   FIRST_FILTER_DOMAIN(for filterBounds)
# I've decided this is sort of a useless function... only good for landsat bands I think
#===========================================
#def filter_domain1(collection,domainType, subdomain):
#	if(domainType=='points'):
#		collection =collection.filterBounds(subdomain);
#	return (collection);

#===========================================
#   GET_STATISTIC
#===========================================
def get_statistic(collection,variable,statistic,anomOrValue):
    if(statistic=='Mean'):
         collection = collection.mean();
    elif(statistic=='Median'):
         collection = collection.median();
    elif(statistic=='Total'):
         collection = collection.sum();

    if((anomOrValue=='value' or anomOrValue=='clim') and (variable=='tmmx' or variable=='tmmn')):
        collection=collection.subtract(273.15)  #convert to C
        #collection=collection.subtract(273.15).multiply(1.8).add(32); #convert to F

    return (collection);

#===========================================
#   SECOND_FILTER_DOMAIN (for clipping/masking)
#===========================================
def filter_domain2(collection,domainType, subdomain):
    if(domainType=='points'):
        fc = ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8');
        #collection= collection.clip(fc.geometry());
    elif(domainType=='states'):
        fc = ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8').filter(ee.Filter.eq('Name', subdomain));
        collection= collection.clip(fc.geometry());
    elif(domainType=='conus'):
        fc = ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8');
        collection= collection.clip(fc.geometry());
    elif(domainType=='rectangle'):
        collection= collection.clip(subdomain);

    return (collection);

#===========================================
#   GET_COLORBAR
#===========================================
def get_colorbar(variable,anomOrValue):
    #Set defaults to avoid error
    palette = ""
    minColorbar = 999
    maxColorbar = 999
    colorbarLabel = ''
    if(variable=='NDVI' or variable=='EVI'):
        if(anomOrValue=='anom'):
            palette="A50026,D73027,F46D43,FDAE61,FEE08B,FFFFBF,D9EF8B,A6D96A,66BD63,1A9850,006837"
            minColorbar=-.4
            maxColorbar=.4
            colorbarLabel='Difference from climatology'
        else:
            palette="FFFFE5,F7FCB9,D9F0A3,ADDD8E,93D284,78C679,41AB5D,238443,006837,004529"
            minColorbar=-.1
            maxColorbar=.9
            colorbarLabel=''
    elif(variable=='NDSI' or variable=='NDWI'):
        if(anomOrValue=='anom'):
            palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
            minColorbar=-.5
            maxColorbar=.5
            colorbarLabel='Difference from climatology'
        else:
            palette="08306B,08519C,2171B5,4292C6,6BAED6,9ECAE1,C6DBEF,DEEBF7,F7FBFF"
            minColorbar=-.2
            maxColorbar=.7
            colorbarLabel=''
    elif(variable=='pr'):
        if(anomOrValue=='anom'):
            minColorbar=0
            maxColorbar=200
            palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
            colorbarLabel='Percent of climatology'
        else:
            minColorbar=0
            maxColorbar=400
            palette="FFFFD9,EDF8B1,C7E9B4,7FCDBB,41B6C4,1D91C0,225EA8,0C2C84"
            colorbarLabel='mm'
    elif(variable=='tmmx' or variable=='tmmn'):
        if(anomOrValue=='anom'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=-5
            maxColorbar=5
            colorbarLabel='Difference from climatology (deg C)'
        elif(variable=='tmmx'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=-20
            maxColorbar=30
            colorbarLabel='deg C'
            #palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
            #minColorbar=-10
            #maxColorbar=110
            #colorbarLabel='deg F'
        elif(variable=='tmmn'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=-30
            maxColorbar=20
            colorbarLabel='deg C'
    elif(variable=='rmin' or variable=='rmax'):
        if(anomOrValue=='anom'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=-25
            maxColorbar=25
            colorbarLabel='Difference from climatology'
        elif(variable=='rmin'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=0
            maxColorbar=100
            colorbarLabel='Percent'
        elif(variable=='rmax'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=0
            maxColorbar=100
            colorbarLabel='%'
    elif(variable=='srad'):
        if(anomOrValue=='anom'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=-25
            maxColorbar=25
            colorbarLabel='Difference from climatology (W/m2)'
        else:
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=100
            maxColorbar=350
            colorbarLabel='W /m2'
    elif(variable=='vs'):
        if(anomOrValue=='anom'):
            palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
            minColorbar=-2.5
            maxColorbar=2.5
            colorbarLabel='Difference from climatology (m/s)'
        else:
            palette="FFFFD9,EDF8B1,C7E9B4,7FCDBB,5DC2C1,41B6C4,1D91C0,225EA8,253494,081D58"
            minColorbar=0
            maxColorbar=5
            colorbarLabel='m/s'
    elif(variable=='sph'):
        if(anomOrValue=='anom'):
            minColorbar=-30
            maxColorbar=30
            palette="053061,2166AC,4393C3,67ADD1,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,E88465,D6604D,B2182B,67001F"
            colorbarLabel='Percent Difference from climatology'
        else:
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026,D6604D,B2182B,67001F"
            minColorbar=0
            maxColorbar=0.02
            colorbarLabel='kg / kg'
    elif(variable=='erc'):
        if(anomOrValue=='anom'):
            minColorbar=-50
            maxColorbar=50
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            colorbarLabel='Difference from climatology'
        else:
            palette="FFFFFF,FFFFCC,FFEDA0,FED976,FEB24C,FD8D3C,FC4E2A,E31A1C,BD0026,800026,000000"
            minColorbar=10
            maxColorbar=120
            colorbarLabel=''
    elif(variable=='pet'): #mm
        if(anomOrValue=='anom'):
            minColorbar=80
            maxColorbar=120
            palette="053061,2166AC,4393C3,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,D6604D,B2182B,67001F"
            colorbarLabel='Percent of climatology'
        else:
            minColorbar=300
            maxColorbar=800
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
            colorbarLabel='mm'
    elif(variable=='wb'): #mm
        if(anomOrValue=='anom'):
            minColorbar=-3
            maxColorbar=3
            palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
            colorbarLabel='Percent of climatology'
        else:
            minColorbar=-220
            maxColorbar=220
            palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
            colorbarLabel='mm'
    elif(variable=='pdsi'): #mm
        if(anomOrValue=='anom'):
            minColorbar=-3
            maxColorbar=3
            palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
            colorbarLabel='Percent of climatology'
        else:
            minColorbar=-220
            maxColorbar=220
            palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
            colorbarLabel='mm'

    return (palette,minColorbar,maxColorbar,colorbarLabel);

#===========================================
#   MAP_COLLECTION
#===========================================
def map_collection(collection,opacity,palette,minColorbar,maxColorbar):
    #palette = palette.replace('#','')   #might need this to account for difference with svg colorbar palette and GAE palette
    colorbarOptions = {
        'min':minColorbar,
        'max':maxColorbar,
        'palette':palette,
        'opacity':opacity, #range [0,1]
    }
    mapid = collection.getMapId(colorbarOptions)

    return mapid;

'''
#===========================================
#   GET_TIMESERIES
#===========================================
def get_timeseries(collection,point,variable):
######################################################
#### Data in list format
######################################################
    dataString = collection.getRegion(point,1).getInfo();
    dataString.pop(0) #remove first row of list ["id","longitude","latitude","time",variable]

    timeList = [row[3] for row in dataString]
    variableList = [row[4] for row in dataString]

#newarray=[['Dates','NDVI']]
#for x in zip(timeList,variableList):
#    if x[1] is not None:
#        newarray.append([x[0],x[1]])

######################################################
#### CREATE TIME SERIES ARRAY WITH DATE IN COL 1 AND VALUE IN COL 2
######################################################
    timeSeries = []
    for i in range(0,len(variableList),1):
        time_ms = (ee.Algorithms.Date(dataString[i][3])).getInfo()['value']
        data1 = time.strftime('%m/%d/%Y',  time.gmtime(time_ms/1000))
        data2 = (dataString[i][4])
        if data2 is not None:
            timeSeries.append([data1,data2])

######################################################
#### SORT IN CHRONOLOGICAL ORDER
######################################################
    timeSeries.sort(key=lambda date: datetime.datetime.strptime(date[0], "%m/%d/%Y"))

######################################################
#### ADD HEADER TO SORTED LIST
######################################################
    timeSeries= [['Dates','Values']] + timeSeries

######################################################
#### CALCULATE NDVI STATS
######################################################
#### FILTER OUT "None" VALUES
#variableList_filt = [x for x in variableList if x is not None]
#meanNDVI = numpy.mean(variableList_filt,axis=0)
#medianNDVI = numpy.median(variableList_filt,axis=0)
#maxNDVI = numpy.max(variableList_filt,axis=0)
#minNDVI = numpy.min(variableList_filt,axis=0)

######################################################
#### RETURN
######################################################
    return (timeSeries)
'''
