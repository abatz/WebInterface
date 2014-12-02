import ee
import time
import datetime
import numpy

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

	if(statistic=='Total'):
		climatology = ee.Image(climatology.sum().divide(num_years));
	elif(statistic=='Median'):
		climatology = ee.Image(climatology.median());
	elif(statistic=='Mean'):
		climatology = ee.Image(climatology.mean());

	if(anomOrValue=='clim'):
		if((variable=='tmmx' or variable=='tmmn')):
			climatology=climatology.subtract(273.15);
		mask = collection.gt(-9999);
		climatology = climatology.mask(mask);
		collection=climatology;
	elif(anomOrValue=='anom'):
		#calculate anomaly
		if(statistic=='Total'):
			collection = ee.Image(collection.divide(climatology).multiply(100)); #anomaly
		elif(statistic=='Median'):
			collection = ee.Image(collection.subtract(climatology)); #anomaly
		elif(statistic=='Mean'):
			collection = ee.Image(collection.subtract(climatology));

	return(collection,climatologyNote);

#===========================================
#   FIRST_FILTER_DOMAIN(for filterBounds)
#===========================================
#def filter_domain1(collection,domainType, subdomain):
#	if(domainType=='points'):
#		collection =collection.filterBounds(subdomain);
#	elif(domainType=='states'):
#	elif(domainType=='conus'):
#	elif(domainType=='polygon'):
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
		collection=collection.subtract(273.15);

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

	return (collection);

#===========================================
#   MAP_COLLECTION 
#===========================================
def map_collection(collection,variable,anomOrValue,opacity):
	#opacity=".85";
	if(variable=='NDVI' or variable=='EVI'):
		if(anomOrValue=='anom'):
			palette="A50026,D73027,F46D43,FDAE61,FEE08B,FFFFBF,D9EF8B,A6D96A,66BD63,1A9850,006837"
			minColorbar=-.4
			maxColorbar=.4
		else:
			palette="FFFFE5,F7FCB9,D9F0A3,ADDD8E,93D284,78C679,41AB5D,238443,006837,004529"
			minColorbar=-.1
			maxColorbar=.9
	elif(variable=='NDSI' or variable=='NDWI'):
		if(anomOrValue=='anom'):
			palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
			minColorbar=-.5
			maxColorbar=.5
		else:
			palette="08306B,08519C,2171B5,4292C6,6BAED6,9ECAE1,C6DBEF,DEEBF7,F7FBFF"
			minColorbar=-.1
			maxColorbar=.9
	elif(variable=='BAI'):
		if(anomOrValue=='anom'):
			palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
			minColorbar=-.5
			maxColorbar=.5
		else:
			palette="08306B,08519C,2171B5,4292C6,6BAED6,9ECAE1,C6DBEF,DEEBF7,F7FBFF"
			minColorbar=-.1
			maxColorbar=.9
	elif(variable=='NBRT'):
		if(anomOrValue=='anom'):
			palette="006837,1A9850,66BD63,A6D96A,D9EF8B,FFFFBF,FEE08B,FDAE61,F46D43,D73027,A50026"
			minColorbar=-.02
			maxColorbar=.02
		else:
			palette="FFFFFF,F0F0F0,D9D9D9,BDBDBD,AAAAAA,969696,737373,525252,252525,000000"
			minColorbar=.95;
			maxColorbar=1.0;
	elif(variable=='pr'):
		minColorbar=0
		maxColorbar=200
		if(anomOrValue=='anom'):
			palette="67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061"
		else:
			palette="FFFFD9,EDF8B1,C7E9B4,7FCDBB,41B6C4,1D91C0,225EA8,0C2C84"
	elif(variable=='tmmx' or variable=='tmmn'):
		if(anomOrValue=='anom'):
			palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
			minColorbar=-5
			maxColorbar=5
		elif(variable=='tmmx'):
			palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			minColorbar=-20
			maxColorbar=30
		elif(variable=='tmmn'):
			palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			minColorbar=-30
			maxColorbar=20
	elif(variable=='rmin' or variable=='rmax'):
		if(anomOrValue=='anom'):
			palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
			minColorbar=-25
			maxColorbar=25
		elif(variable=='rmin'):
			palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			minColorbar=0
			maxColorbar=100
		elif(variable=='rmax'):
			palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			minColorbar=0
			maxColorbar=100
	elif(variable=='srad'):
		if(anomOrValue=='anom'):
			palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FFFFBF,FEE090,FDAE61,F46D43,D73027,A50026"
			minColorbar=-25
			maxColorbar=25
		else:
			palette="313695,4575B4,74ADD1,ABD9E9,E0F3F8,FEE090,FDAE61,F46D43,D73027,A50026"
			minColorbar=100
			maxColorbar=350
	elif(variable=='vs'):
		if(anomOrValue=='anom'):
			palette="A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695"
			minColorbar=-2.5
			maxColorbar=2.5
		else:
			palette="FFFFD9,EDF8B1,C7E9B4,7FCDBB,5DC2C1,41B6C4,1D91C0,225EA8,253494,081D58"
			minColorbar=0
			maxColorbar=5

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
