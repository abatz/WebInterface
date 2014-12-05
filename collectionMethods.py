import ee
import time
import datetime
import numpy

#===========================================
#   GET_IMAGES 
#===========================================
def get_images(opacity,pointLat,pointLong,NELat,NELong,SWLat,SWLong,ppost,variable,state,domainType,\
    dateStart,dateEnd,anomOrValue,palette,minColorbar,maxColorbar):
	
        palette,minColorbar,maxColorbar,colorbarLabel=get_colorbar(variable,anomOrValue);
	
	collection,collectionName,collectionLongName,product,variableShortName,notes,statistic=get_collection(variable);
	title=statistic +' ' +variableShortName;

	if(anomOrValue=='anom'):
		title=title+' Anomaly from Climatology ';
	source=collectionLongName+' from '+dateStart+'-'+dateEnd+''

	if(domainType=='states'):
		subdomain=state;
		mapzoom=4; #would like to zoom in on that state
	elif(domainType=='full' and product=='modis'):
		subdomain = ee.Feature.Point(pointLong,pointLat);
		point = subdomain;
		mapzoom=4;
	elif(domainType=='full' and product=='gridded'):
		subdomain = ee.Feature.Point(pointLong,pointLat);
		point = subdomain;
		mapzoom=5;
	elif(domainType=='rectangle'):
		subdomain = ee.Feature.Rectangle(SWLong,SWLat,NELong,NELat);
		point = subdomain;
		mapzoom=4;
	else:
		subdomain = ee.Feature.Point(pointLong,pointLat);
		point = subdomain;
		mapzoom=4;

	collection = ee.ImageCollection(collectionName).filterDate(dateStart,dateEnd).select([variable],[variable]);
	#collection = filter_domain1(collection,domainType, subdomain);

	template_values = {}
	#if points selected, get timeseries before calculate statistic
	#       if(domainType=='points'):
	#               #timeSeriesData,timeSeriesGraphData,template_values = callTimeseries(collection,variable,domainType,point)
	#               timeSeriesData=get_timeseries(collection,point,variable)
	#               timeSeriesGraphData = []
	#               n_rows = numpy.array(timeSeriesData).shape[0];
	#               for i in range(2,n_rows):
	#                 entry = {'count':timeSeriesData[i][1],'name':timeSeriesData[i][0]};
	#                 timeSeriesGraphData.append(entry);
	#
	#               template_values = {
	#                   'timeSeriesData': timeSeriesData,
	#                   'timeSeriesGraphData': timeSeriesGraphData,
	#               }

	collection = get_statistic(collection,variable,statistic,anomOrValue);
	collection =filter_domain2(collection,domainType,subdomain)

	if(anomOrValue=='anom' or anomOrValue=='clim'):
		collection,climatologyNotes = get_anomaly(collection,product,variable,collectionName,dateStart,dateEnd,statistic,anomOrValue);
		template_values={'climatologyNotes': climatologyNotes,};

	#the earth engine call
	mapid =map_collection(collection,variable,anomOrValue,opacity,palette,minColorbar,maxColorbar)

	return (mapid,template_values,colorbarLabel,product,collectionLongName,notes,title,source,mapzoom,palette,minColorbar,maxColorbar);


#===========================================
#   INITIALIZE_FORM 
#===========================================
#def initialize_form(self,ppost):
    #if(ppost==1):
        #initialize forms
        #mapzoom=self.request.get('mapzoom');
        #pointLat=self.request.get('pointLat');
        #pointLong=self.request.get('pointLong');
        #state=self.request.get('state');
        #variable=self.request.get('variable');
        #domainType=self.request.get('domainType');
        #dateStart=self.request.get('dateStart');
        #dateEnd=self.request.get('dateEnd');
        #anomOrValue=self.request.get('anomOrValue');
        #opacity=self.request.get('opacity');
        #NELat=float(self.request.get('NELat'));
        #NELong=float(self.request.get('NELong'));
        #SWLat=float(self.request.get('SWLat'));
        #SWLong=float(self.request.get('SWLong'));
#    #else:
#    initial_mapzoom=4;
#    initial_pointLat=42;
#    initial_pointLong=-112;
#    initial_state='Calfornia';
#    initial_variable='pr';
#    initial_domainType='full';
#    initial_dateStart='2013-01-01';
#    initial_dateEnd='2013-03-31';
#    initial_anomOrValue='anom';
#    initial_opacity=str(14*0.05);
#    initial_NELat=45;
#    initial_NELong=-95;
#    initial_SWLat=40;
#    initial_SWLong=-111;

#    #initialize forms
#    mapzoom=self.request.get('mapzoom',initial_mapzoom);
#    pointLat=self.request.get('pointLat',initial_pointLat);
#    pointLong=self.request.get('pointLong',initial_pointLong);
#    state=self.request.get('state',initial_state);
#    variable=self.request.get('variable',initial_variable);
#    domainType=self.request.get('domainType',initial_domainType);
#    dateStart=self.request.get('dateStart',initial_dateStart);
#    dateEnd=self.request.get('dateEnd',initial_dateEnd);
#    anomOrValue=self.request.get('anomOrValue',initial_anomOrValue);
#    opacity=self.request.get('opacity',initial_opacity);
#    NELat=float(self.request.get('NELat',initial_NELat));
#    NELong=float(self.request.get('NELong',initial_NELong));
#    SWLat=float(self.request.get('SWLat',initial_SWLat));
#    SWLong=float(self.request.get('SWLong',initial_SWLong));

#    return( mapzoom,pointLat,pointLong,state,variable,domainType,dateStart,dateEnd,anomOrValue,\
#        opacity,NELat,NELong,SWLat,SWLong);

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

    collection = ee.ImageCollection(collectionName).select([variable],[variable]);

    return (collection,collectionName,collectionLongName,product,variableShortName,notes,statistic);

#===========================================
#    GET_TIMESERIES
#===========================================
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

#===========================================
#    GET_ANOMALY
#===========================================
def get_anomaly(collection,product,variable,collectionName,dateStart,dateEnd,statistic,anomOrValue):
    doyStart = ee.Number(ee.Algorithms.Date(dateStart).getRelative('day', 'year')).add(1); #removed double()
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
    climatology = ee.ImageCollection(collectionName).filterDate(yearStartClim, yearEndClim).filter(doy_filter).select([variable],[variable]);

    if(statistic=='Total' and variable=='pr'):
         climatology = ee.Image(climatology.sum().divide(num_years));
    elif(statistic=='Median'):
         climatology = ee.Image(climatology.median());
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
        elif(statistic=='Median'):
            collection = ee.Image(collection.subtract(climatology)); #anomaly
        elif(statistic=='Mean' and variable=='sph'):
            collection = ee.Image(collection.subtract(climatology).divide(climatology).multiply(100));
        elif(statistic=='Mean'):
            collection = ee.Image(collection.subtract(climatology));

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
            #colorbarLabel='mm'
            colorbarLabel=''
    elif(variable=='tmmx' or variable=='tmmn'):
        if(anomOrValue=='anom'):
            palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
            minColorbar=-5
            maxColorbar=5
            colorbarLabel='Difference from climatology'
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
            colorbarLabel='%'
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
            colorbarLabel='Difference from climatology'
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
            colorbarLabel='Difference from climatology'
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
 
    return (palette,minColorbar,maxColorbar,colorbarLabel);

#===========================================
#   MAP_COLLECTION 
#===========================================
def map_collection(collection,variable,anomOrValue,opacity,palette,minColorbar,maxColorbar):
    #palette = palette.replace('#','')   #might need this to account for difference with svg colorbar palette and GAE palette
    colorbarOptions = {
        'min':minColorbar,
        'max':maxColorbar,
        'palette':palette,
        'opacity':opacity, #range [0,1]
    }
    mapid = collection.getMapId(colorbarOptions)

    return mapid;

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
