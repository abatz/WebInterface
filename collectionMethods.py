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
    dS = TV['dateStart']; dE = TV['dateEnd'];
    units=TV['units'];
    palette=TV['palette'];
    #get map palette options
    colorbarmap,colorbarsize,minColorbar,maxColorbar,colorbarLabel,varUnits=get_colorbar(str(var),str(aOV),units)

    #Override max/minColorbar if user entered custom value
    if 'minColorbar' in template_values.keys():
        minColorbar = template_values['minColorbar']
    if 'maxColorbar' in template_values.keys():
        maxColorbar = template_values['maxColorbar']
    if 'colorbarmap' in template_values.keys():
        colorbarmap = template_values['colorbarmap']
    if 'colorbarsize' in template_values.keys():
        colorbarsize = template_values['colorbarsize']

    #Get initial collection
    collection,collectionName,collectionLongName,product,variableShortName,notes,statistic=get_collection(var);
    if aOV in ['anom','clim']:
        collectionSource=collection;

    #remove starting character which indicates the product
    var = var[1:]

    #Set title
    title = statistic + ' ' + variableShortName;
    if(aOV == 'anom'):
        title = title + ' Anomaly from Climatology ';

    #Set source, domain, subdomain
    source = collectionLongName + ' from ' + dS + '-' + dE + '';
    subdomain = None;
    if(dT == 'states'):
        subdomain = template_values['state']
    if(dT=='rectangle'):
        subdomain = ee.Feature.Rectangle(float(TV['SWLong']),float(TV['SWLat']),float(TV['NELong']),float(TV['NELat']));

    #Format collection
    mapid = {'mapid':[],'token':[]}
    if var == 'wb':
        collection_pr = collection.filterDate(dS,dE).select('pr');
        collection_pet = collection.filterDate(dS,dE).select('pet');
        collection_pr = get_statistic(collection_pr,'pr',statistic,'value');
        collection_pet = get_statistic(collection_pet,'pet',statistic,'value');
        collection = collection_pr.subtract(collection_pet); #water balance
    elif var =='tmean':
        collection_tmax = collection.filterDate(dS,dE).select('tmmx');
        collection_tmin = collection.filterDate(dS,dE).select('tmmn');
        collection_tmax= get_statistic(collection_tmax,'tmmx',statistic,'value');
        collection_tmin = get_statistic(collection_tmin,'tmmn',statistic,'value');
        collection = collection_tmax.add(collection_tmin).multiply(0.5); #tmean
    else:
        collection = collection.filterDate(dS,dE).select(var)
        collection = get_statistic(collection,var,statistic,aOV)

    #Anomaly
	if aOV in ['anom','clim']:
	    collection,climatologyNotes = get_anomaly(collection,product,var,collectionName,dS,dE,statistic,aOV,collectionSource)
	    TV['climatologyNotes'] = climatologyNotes
	#Units
    collection=check_units(collection,var,aOV,units);

    #Get mapid
    mapid = map_collection(collection,TV['opacity'],palette,minColorbar,maxColorbar)

    #==============
    #Update template values
    extra_template_values = {
        'source': source,
        'product':product,
        'productLongName': collectionLongName,
        'variableShortName': variableShortName,
        'title': title,
        'colorbarLabel': colorbarLabel,
        'minColorbar': minColorbar,
        'maxColorbar': maxColorbar,
        'varUnits': varUnits
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
#currently this doesn't work with wb and tmean

    TV = {};
    for key, val in template_values.iteritems():
        TV[key] = val
    var = TV['variable'];mc = TV['marker_colors'];
    dS = TV['dateStart'];dE = TV['dateEnd'];
    units=TV['units'];
    pointsLongLat = str(TV['pointsLongLat']) #string of comma separates llon,lat pairs
    pointsLongLatList = pointsLongLat.replace(' ','').split(',');
    pointsLongLatTuples = [[float(pointsLongLatList[i]),float(pointsLongLatList[i+1])] for i in range(0,len(pointsLongLatList) - 1,2)];
    timeSeriesData = [];timeSeriesGraphData =[];
    points = ee.Feature.MultiPoint(pointsLongLatTuples);

    #get the collection
    #Note get_collecton needs full var name with prefix
    collection,collectionName,collectionLongName,product,variableShortName,notes,statistic=get_collection(var);

    #Next we strip data type of variable name
    var = var[1:];

    #extracting data
    #remove first row of list ["id","longitude","latitude","time",variable]
    if(var=='wb'):
        dataList = collection.filterDate(dS,dE).select('pr').getRegion(points,1).getInfo(); #pr
        datapet = collection.filterDate(dS,dE).select('pet').getRegion(points,1).getInfo();
	datapet.pop(0);
    elif(var=='tmean'):
        dataList = collection.filterDate(dS,dE).select('tmmx').getRegion(points,1).getInfo(); #tmax
        datatmin = collection.filterDate(dS,dE).select('tmmn').getRegion(points,1).getInfo();
	datatmin.pop(0);
    else:
        dataList = collection.filterDate(dS,dE).select(var).getRegion(points,1).getInfo();

    dataList.pop(0);

    source = collectionLongName + ' from ' + dS + '-' + dE + '';

    ######################################################
    #### Format data for highcharts figure and data tabs
    #### Each point gets it's own dictionary
    #### timeSeriesData[idx] = {MarkerColor:marker_colors[idx],LongLat:ll_string, Data:[[Date1,val1],[Date2, val2]]}
    ######################################################
    #Format data
    point_cnt = 0;
    for idx, data in enumerate(dataList):
        lon = round(data[1],4);
        lat = round(data[2],4);
        if idx == 0:
            #To keep track of when data point changes
            lon_init = lon;
            lat_init = lat;
            data_dict = {};
            data_dict_graph = {};
            point_cnt+=1;
        else:
            if abs(float(lon) - float(lon_init)) >0.0001 or abs(float(lat) - float(lat_init)) > 0.0001:
                #New data point
                lon_init = lon;
                lat_init = lat;
                timeSeriesData.append(data_dict);
                timeSeriesGraphData.append(data_dict_graph);
                data_dict = {};
                data_dict_graph = {};
                point_cnt+=1;
        if not data_dict:
            data_dict = {
                'LongLat': str(lon) + ',' + str(lat),
                'Data': []
            }
            data_dict_graph = {
                'MarkerColor':mc[point_cnt - 1],
                'LongLat': str(lon) + ',' + str(lat),
                'Data': []
            }
	#=============
        #extract the time
	#=============
        time = int(data[3]);
	#=============
        #extract the date
	#=============
        date_string = str(data[0]);
        try:
            date_string = date_string[0:4] + '-' + date_string[4:6] + '-' + date_string[6:8];
        except:
            pass
	#=============
        #extract the data
	#=============
        if(var=='wb'):
           try:
               prval = round(data[4],4);
           except:
               prval = data[4];

           try:
               petval = round(datapet[idx][4],4);
           except:
               petval = datapet[idx][4];
	   val = prval-petval;
        elif(var=='tmean'):
           try:
               tmaxval = round(data[4],4);
           except:
               tmaxval = data[4];

           try:
               tminval = round(datatmin[idx][4],4);
           except:
               tminval = datatmin[idx][4];
	   val = (tmaxval+tminval)/2;
	else:
           try:
               val = round(data[4],4);
           except:
               val = data[4];
	#=============
	# check units
	#=============
	if(var=='tmmx' or var=='tmmn' or var=='tmean'):
            val=val-273.15;  #convert K to C
            if(units=='english'):
                val=1.8*val+32;    #convert C to F
        if(var=='pr' or var=='pet' or var=='wb'):
            if(units=='english'): 
                val=val/25.4; #convert mm to inches
        if(var=='vs' and units=='english'):
            val=2.23694*val; #convert m/s to mi/h
	#=============
        data_dict['Data'].append([date_string,val])
        data_dict_graph['Data'].append([time,val])


    timeSeriesData.append(data_dict)
    timeSeriesGraphData.append(data_dict_graph)
    timeSeriesGraphData = json.dumps(timeSeriesGraphData)
    #Update template values
    extra_template_values = {
        'source':source,
        'product':product,
        'productLongName':collectionLongName,
        'variableShortName':variableShortName,
        'timeSeriesData':timeSeriesData,
        'timeSeriesGraphData':timeSeriesGraphData
    }
    TV.update(extra_template_values)
    return TV
#===========================================
#    GET_COLLECTION
#===========================================
def get_collection(variable):
    #strip off product and variable names
    product = variable[:1]
    if(product=='G'):
        product = 'gridded'
    elif(product=='L'):
        product = 'landsat'
    elif(product=='M'):
        product='modis'
    variable=variable[1:]

    if(variable=='NDVI'):
        notes="NDSI calculated from Norm. Diff. of Near-IR and Red bands"
        statistic='Median'
        variableShortName=variable;
	if(product=='modis'):
            collectionName = 'MCD43A4_NDVI';
            collectionLongName = 'MODIS 16-day NDVI'
        elif(product=='landsat'):
            collectionName = 'LT4_L1T_8DAY_NDVI,LT5_L1T_8DAY_NDVI,LE7_L1T_8DAY_NDVI,LC8_L1T_8DAY_NDVI';
            collectionLongName = 'Landsat4/5/7/8 8-day NDVI Composite'
            collection4 = ee.ImageCollection('LT4_L1T_8DAY_NDVI');
            collection5 = ee.ImageCollection('LT5_L1T_8DAY_NDVI');
            collection7 = ee.ImageCollection('LE7_L1T_8DAY_NDVI');
            #collection8 = ee.ImageCollection('LC8_L1T_8DAY_NDVI');
    elif(variable=='NDSI'):
        notes="NDSI calculated from Norm. Diff. of Green and mid-IR bands"
        statistic='Median'
        variableShortName=variable;
	if(product=='modis'):
            collectionName = 'MCD43A4_NDSI';
            collectionLongName = 'MODIS 16-day NDSI'
        elif(product=='landsat'):
	    collectionName = 'LT4_L1T_8DAY_NDSI,LT5_L1T_8DAY_NDSI,LE7_L1T_8DAY_NDSI,LC8_L1T_8DAY_NDSI';
            collectionLongName = 'Landsat4/5/7/8 8-day NDSI Composite'
            collection4 = ee.ImageCollection('LT4_L1T_8DAY_NDSI');
            collection5 = ee.ImageCollection('LT5_L1T_8DAY_NDSI');
            collection7 = ee.ImageCollection('LE7_L1T_8DAY_NDSI');
            #collection8 = ee.ImageCollection('LC8_L1T_8DAY_NDSI');
    elif(variable=='NDWI'):
        notes="NDWI calculated from near-IR and a second IR bands"
        statistic='Median'
        variableShortName=variable;
	if(product=='modis'):
            collectionName = 'MCD43A4_NDWI';
            collectionLongName = 'MODIS 16-day NDWI Composite'
        elif(product=='landsat'):
	    collectionName = 'LT5_L1T_8DAY_NDWI,LT5_L1T_8DAY_NDWI,LE7_L1T_8DAY_NDWI,LC8_L1T_8DAY_NDWI';
            collectionLongName = 'Landsat5/7/8 8-day NDWI Composite'
            collection4 = ee.ImageCollection('LT5_L1T_8DAY_NDWI');
            collection5 = ee.ImageCollection('LT5_L1T_8DAY_NDWI');
            collection7 = ee.ImageCollection('LE7_L1T_8DAY_NDWI');
            #collection8 = ee.ImageCollection('LC8_L1T_8DAY_NDWI');
    elif(variable=='EVI'):
        notes="EVI calculated from Near-IR,Red and Blue bands"
        statistic='Median'
        variableShortName=variable;
	if(product=='modis'):
            collectionName = 'MCD43A4_EVI';
            collectionLongName = 'MODIS 16-day EVI Composite'
        elif(product=='landsat'):
	    collectionName = 'LT4_L1T_8DAY_EVI,LT5_L1T_8DAY_EVI,LE7_L1T_8DAY_EVI';
	    #collectionName = 'LT4_L1T_8DAY_EVI,LT5_L1T_8DAY_EVI,LE7_L1T_8DAY_EVI,LC8_L1T_8DAY_EVI';
            collectionLongName = 'Landsat4/5/7/8 8-day EVI Composite'
            collection4 = ee.ImageCollection('LT4_L1T_8DAY_EVI');
            collection5 = ee.ImageCollection('LT5_L1T_8DAY_EVI');
            collection7 = ee.ImageCollection('LE7_L1T_8DAY_EVI');
            #collection8 = ee.ImageCollection('LC8_L1T_8DAY_EVI');
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
    elif(variable=='tmean'):
        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes="Calculated as Average of Min/Max Daily Temperature"
        statistic='Mean'
        variableShortName='Mean Temperature'
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
        collectionName = 'IDAHO_EPSCOR/PDSI';
        collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
        product = 'gridded'
        notes=""
        statistic='Mean'
        variableShortName='Palmer Drought Severity Index (PDSI)'

    if(product=='gridded' or product=='modis'):
       	collection = ee.ImageCollection(collectionName);
    elif(product=='landsat'):
	collection = ee.ImageCollection(collection4.merge(collection5).merge(collection7));
	#collection = ee.ImageCollection(collection4.merge(collection5).merge(collection7).merge(collection8));

    return (collection,collectionName,collectionLongName,product,variableShortName,notes,statistic);

#===========================================
#    GET_ANOMALY
#===========================================
def get_anomaly(collection,product,variable,collectionName,dateStart,dateEnd,statistic,anomOrValue,collectionSource):
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
        climatology_pr = collectionSource.filterDate(yearStartClim, yearEndClim).filter(doy_filter).\
           select('pr');
        climatology_pet = collectionSource.filterDate(yearStartClim, yearEndClim).filter(doy_filter).\
           select('pet');
    elif(variable=='tmean'):
        climatology_tmax = collectionSource.filterDate(yearStartClim, yearEndClim).filter(doy_filter).\
           select('tmmx');
        climatology_tmin = collectionSource.filterDate(yearStartClim, yearEndClim).filter(doy_filter).\
           select('tmmn');
    else:
        climatology = collectionSource.filterDate(yearStartClim, yearEndClim).filter(doy_filter).select(variable);

    if(variable=='wb'):
         climatology_pr = ee.Image(climatology_pr.sum().divide(num_years));
         climatology_pet = ee.Image(climatology_pet.sum().divide(num_years));
	 climatology = climatology_pr.subtract(climatology_pet);
    elif(variable=='tmean'):
         climatology_tmax = ee.Image(climatology_tmax.mean());
         climatology_tmin = ee.Image(climatology_tmin.mean());
	 climatology = climatology_tmax.add(climatology_tmin).multiply(.5);
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
            collection = ee.Image(collection.subtract(climatology).divide(climatology).multiply(100));
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
    return (collection);

#===========================================
#   CHECK_UNITS
#===========================================
def check_units(collection,variable,anomOrValue,units):
    #anomOrValue = 'anom' or 'value'... not the variable being passed

    if(variable=='tmmx' or variable=='tmmn' or variable =='tmean'):
        if(anomOrValue=='value' or anomOrValue=='clim'):
            collection=collection.subtract(273.15)  #convert K to C
        if(units=='english'):
            collection=collection.multiply(1.8);    #convert C anom to F anom
	if(units=='english' and (anomOrValue=='value' or anomOrValue=='clim')):
	    collection = collection.add(32);        #convert C values to F values
    if(variable=='pr' or variable=='pet' or variable=='wb'):
        if(units=='english' and (anomOrValue=='value' or anomOrValue=='clim')):  #don't need to convert for anom
            collection=collection.divide(25.4); #convert mm to inches
    if(variable=='vs'):
        if(units=='english'):
            collection=collection.multiply(2.23694); #convert m/s to mi/h

    return(collection);

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
def get_colorbar(variable,anomOrValue,units):
    #Set defaults to avoid error
    palette = ""
    minColorbar = 999
    maxColorbar = 999
    colorbarLabel = ''
    #remove first character which identifies the product
    variable = variable[1:]

    if(variable=='NDVI' or variable=='EVI'):
        if(anomOrValue=='anom'):
            palette="A50026,D73027,F46D43,FDAE61,FEE08B,FFFFBF,D9EF8B,A6D96A,66BD63,1A9850,006837"
            minColorbar=-.4
            maxColorbar=.4
            colorbarLabel=variable+' Difference from climatology'
            colorbarmap='RdYlGn'
            colorbarsize='8';
            varUnits='';
        else:
            palette="FFFFE5,F7FCB9,D9F0A3,ADDD8E,93D284,78C679,41AB5D,238443,006837,004529"
            minColorbar=-.1
            maxColorbar=.9
            colorbarLabel=variable;
            colorbarmap='YlGn'
            colorbarsize='9';
            varUnits='';
    elif(variable=='NDSI' or variable=='NDWI'):
        if(anomOrValue=='anom'):
            palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
            minColorbar=-.5
            maxColorbar=.5
            colorbarLabel=variable+' Difference from climatology'
            colorbarmap='RdYlBu'
            colorbarsize='88888888';
            varUnits='';
        else:
            palette="08306B,08519C,2171B5,4292C6,6BAED6,9ECAE1,C6DBEF,DEEBF7,F7FBFF"
            minColorbar=-.2
            maxColorbar=.7
            colorbarLabel=variable;
            colorbarmap='invBlues'
            colorbarsize='8';
            varUnits='';
    elif(variable=='pr'):
        if(anomOrValue=='anom'):
            minColorbar=0
            maxColorbar=200; #%
            palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
            colorbarLabel='Precipitation Amount as Percent of climatology'
            colorbarmap='RdYlBu'
            colorbarsize='8';
            varUnits='%';
        else:
            minColorbar=0
            palette="FFFFD9,EDF8B1,C7E9B4,7FCDBB,41B6C4,1D91C0,225EA8,0C2C84"
	    if(units=='metric'):
           	 colorbarLabel='Precipitation Amount( '+'mm'+' )';
                 maxColorbar=400;
                 varUnits='mm';
	    elif(units=='english'):
           	 colorbarLabel='Precipitation Amount( '+'in'+' )';
                 maxColorbar=16;
                 varUnits='in';
            colorbarmap='YlGnBu'
            colorbarsize='8';
    elif(variable=='tmmx' or variable=='tmmn' or variable=='tmean'):
        if(anomOrValue=='anom'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
	    if(units=='metric'):
		 colorbarLabel='Temperature Difference from climatology (deg C)'
                 minColorbar=-5
                 maxColorbar=5
                 varUnits='deg C';
	    elif(units=='english'):
		 colorbarLabel='Temperature Difference from climatology (deg F)'
                 minColorbar=-10
                 maxColorbar=10
                 varUnits='deg F';
            colorbarmap='BuYlRd'
            colorbarsize='8';
        elif(variable=='tmmx'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
	    if(units=='metric'):
		 colorbarLabel='Temperature (deg C)'
                 minColorbar=-20
                 maxColorbar=30
                 varUnits='deg C';
	    elif(units=='english'):
		 colorbarLabel='Temperature (deg F)'
                 minColorbar=0
                 maxColorbar=100
                 varUnits='deg F';
            colorbarmap='BuRd'
            colorbarsize='8';
        elif(variable=='tmmn'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
	    if(units=='metric'):
		 colorbarLabel='Temperature (deg C)'
	         minColorbar=-20
	         maxColorbar=20
                 varUnits='deg C';
	    elif(units=='english'):
		 colorbarLabel='Temperature (deg F)'
	         minColorbar=0
	         maxColorbar=80
                 varUnits='deg F';
            colorbarmap='BuRd'
            colorbarsize='8';
        elif(variable=='tmean'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            if(units=='metric'):
                 colorbarLabel='Temperature (deg C)'
                 minColorbar=-20
                 maxColorbar=20
                 varUnits='deg C';
            elif(units=='english'):
                 colorbarLabel='Temperature (deg F)'
                 minColorbar=0
                 maxColorbar=80
                 varUnits='deg F';
            colorbarmap='BuRd'
            colorbarsize='8';
    elif(variable=='rmin' or variable=='rmax'):
        if(anomOrValue=='anom'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=-25
            maxColorbar=25
            colorbarLabel='Difference from climatology'
            colorbarmap='BuYlRd'
            colorbarsize='8';
            varUnits='deg %';
        elif(variable=='rmin'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=0
            maxColorbar=100
            colorbarLabel='Percent'
            colorbarmap='BuRd'
            colorbarsize='8';
            varUnits='deg %';
        elif(variable=='rmax'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=0
            maxColorbar=100
            colorbarLabel='%'
            colorbarmap='BuRd'
            colorbarsize='8';
            varUnits='deg %';
    elif(variable=='srad'):
        if(anomOrValue=='anom'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=-25
            maxColorbar=25
	    if(units=='metric'):
            	colorbarLabel='Radiation Difference from climatology (W/m^2)'
	    elif(units=='english'):
            	colorbarLabel='Radiation Difference from climatology (W/m^2)'
            varUnits='W/m^2';
            colorbarmap='BuYlRd'
            colorbarsize='8';
        else:
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=100
            maxColorbar=350
	    if(units=='metric'):
		colorbarLabel='Radiation(' +'W /m2'+' )';
	    elif(units=='english'):
            	colorbarLabel='Radiation(' +'W /m2'+' )';
            colorbarmap='BuRd'
            colorbarsize='8';
            varUnits='W/m^2';
    elif(variable=='vs'):
        if(anomOrValue=='anom'):
            palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
	    if(units=='metric'):
		colorbarLabel='Wind Speed Difference from climatology(' +'m/s'+' )';
                minColorbar=-2.5;
                maxColorbar=2.5;
                varUnits='m/s';
	    elif(units=='english'):
		colorbarLabel='Wind Speed Difference from climatology(' +'mi/hr'+' )';
                minColorbar=-5;
                maxColorbar=5;
                varUnits='mi/hr';
            colorbarmap='BuYlRd'
            colorbarsize='8';
        else:
            palette="FFFFD9,EDF8B1,C7E9B4,7FCDBB,5DC2C1,41B6C4,1D91C0,225EA8,253494,081D58"
            minColorbar=0
	    if(units=='metric'):
		colorbarLabel='Wind Speed(' +'m/s'+' )';
                maxColorbar=5;
                varUnits='m/s';
	    elif(units=='english'):
		colorbarLabel='Wind Speed(' +'mi/hr'+' )';
                maxColorbar=10;
                varUnits='mi/hr';
            colorbarmap='YlGnBu'
            colorbarsize='8';
    elif(variable=='sph'):
        if(anomOrValue=='anom'):
            minColorbar=-30
            maxColorbar=30
            palette="053061,2166AC,4393C3,67ADD1,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,E88465,D6604D,B2182B,67001F"
            colorbarLabel='Percent Difference from climatology'
            colorbarmap='BuYlRd'
            colorbarsize='8';
            varUnits='kg/kg';
        else:
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026,D6604D,B2182B,67001F"
            minColorbar=0
            maxColorbar=0.02
            colorbarLabel='kg / kg'
            colorbarmap='BuRd'
            colorbarsize='8';
            varUnits='kg/kg';
    elif(variable=='erc'):
        if(anomOrValue=='anom'):
            minColorbar=-20
            maxColorbar=20
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
            colorbarLabel='Difference from climatology'
            colorbarmap='BuYlRd'
            colorbarsize='8';
            varUnits='';
        else:
            palette="FFFFFF,FFFFCC,FFEDA0,FED976,FEB24C,FD8D3C,FC4E2A,E31A1C,BD0026,800026,000000"
            minColorbar=10
            maxColorbar=120
            colorbarLabel=''
            colorbarmap='YlOrRd'
            colorbarsize='8';
            varUnits='';
    elif(variable=='pet'): #mm
        if(anomOrValue=='anom'):
            minColorbar=80
            maxColorbar=120
            palette="053061,2166AC,4393C3,92C5DE,D1E5F0,F7F7F7,FDDBC7,F4A582,D6604D,B2182B,67001F"
            colorbarLabel='PET Percent of climatology'
            colorbarmap='BuYlRd'
            colorbarsize='8';
            varUnits='%';
        else:
            minColorbar=300
            maxColorbar=800
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FFF6A7,FEE090,FDAE61,F46D43,D73027,A50026"
	    if(units=='metric'):
		colorbarLabel='PET(' +'mm'+' )';
                minColorbar=300
                maxColorbar=800
                varUnits='mm';
	    elif(units=='english'):
		colorbarLabel='PET(' +'in'+' )';
                minColorbar=10
                maxColorbar=30
                varUnits='in';
            colorbarmap='BuRd'
            colorbarsize='8';
    elif(variable=='wb'): #mm
        if(anomOrValue=='anom'):
            minColorbar=-100
            maxColorbar=100
            palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
            colorbarLabel='Water Balance Percent change from climatology'
            colorbarmap='RdYlBu'
            colorbarsize='8';
            varUnits='%';
        else:
            palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
	    if(units=='metric'):
		colorbarLabel='Water Balance(' +'mm'+' )';
                minColorbar=-220
                maxColorbar=220
                varUnits='mm';
	    elif(units=='english'):
		colorbarLabel='Water Balance(' +'in'+' )';
                minColorbar=-10
                maxColorbar=10
                varUnits='in';
            colorbarmap='RdBu'
            colorbarsize='8';
    elif(variable=='pdsi'):
        if(anomOrValue=='anom'):
            minColorbar=-6
            maxColorbar=6
            palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
            colorbarLabel='PDSI Percent of climatology'
            colorbarmap='RdYlBu'
            colorbarsize='8';
            varUnits='%';
        else:
            minColorbar=-6
            maxColorbar=6
            palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061";
            colorbarLabel='PDSI'
            colorbarmap='RdYlBu'
            colorbarsize='8';
            varUnits='';

    return (colorbarmap,colorbarsize,minColorbar,maxColorbar,colorbarLabel,varUnits);

#===========================================
#   MAP_COLLECTION
#===========================================
def map_collection(collection,opacity,palette,minColorbar,maxColorbar):
    colorbarOptions = {
        'min':minColorbar,
        'max':maxColorbar,
        'palette':palette,
        'opacity':opacity, #range [0,1]
    }
    mapid = collection.getMapId(colorbarOptions)

    return mapid;

