import ee
import time
import datetime
import numpy


#===========================================
#   INITIALIZE_FIGURE 
#===========================================
def initializeFigure(variable):
        if(variable=='NDVI'):
                product = 'modis'
                productLongName = 'MCD43A4_NDVI'
                notes="NDVI calculated from Norm. Diff. of Infrared and Red bands"
		statistic='Median'
		variableShortName=variable;
        elif(variable=='NDSI'):
                product = 'modis'
                productLongName = 'MCD43A4_NDSI'
                notes="NDSI calculated from Norm. Diff. of Green and mid-IR bands"
		statistic='Median'
		variableShortName=variable;
	elif(variable=='EVI'):
                product = 'modis'
                productLongName = 'MCD43A4_EVI';
                notes="EVI calculated from Near-IR,Red and Blue bands"
                statistic='Median'
                variableShortName=variable;
	elif(variable=='BAI'):
                product = 'modis'
                productLongName = 'MYD09GA_BAI'
                notes="BAI calculated from Red and Near-IR bands"
                statistic='Median'
                variableShortName=variable;
	elif(variable=='NBRT'):
                product = 'landsat'
                productLongName = 'LE7_L1T_32DAY_NBRT'
                notes="NBR calculated from Near-IR,mid-IR and thermal bands"
                statistic='Median'
                variableShortName=variable;
        elif(variable=='pr'):
                product = 'gridded'
                productLongName = 'gridMET 4-km (Abatzoglou)'
                notes=""
		statistic='Total'
		variableShortName='Precipitation'
	return (product,productLongName,variableShortName,notes,statistic);

#===========================================
#    GET_TIMESERIES
#===========================================
def callTimeseries(collection,collectionLongName,variable,domainType,point):
	if(domainType=='points'):
		#timeSeriesData=collectionMethods.get_timeseries(collection,point,variable)
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
	if(variable=='pr'):
		title='Total ';
	else:
		title='Median ';
	title=title +variable;
	source=collectionLongName+' from '+dateStart+'-'+dateEnd+''
	return (timeSeriesData,timeSeriesGraphData,template_values,title,source);

#===========================================
#    GET_ANOMALY
#===========================================
def get_anomaly(collection,product,variable,collectionName,dateStart,dateEnd,statistic,anomOrValue):
                doyStart = ee.Number(ee.Algorithms.Date(dateStart).getRelative('day', 'year')).add(1); #removed double()
                doyEnd = ee.Number(ee.Algorithms.Date(dateEnd).getRelative('day', 'year')).add(1);
                doy_filter = ee.Filter.calendarRange(doyStart, doyEnd, 'day_of_year');
		if(product=='gridded'):
			yearStartClim ='1980';
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
		mask = collection.gt(0);

		if(anomOrValue=='clim'):
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
#    GET_COLLECTION
#===========================================
def get_collection(product,variable):
  	if(variable=='NDVI'):
                collectionName = 'MCD43A4_NDVI';
		collectionLongName = 'MODIS 16-day NDVI'
  	elif(variable=='NDSI'):
                collectionName = 'MCD43A4_NDSI';
		collectionLongName = 'MODIS 16-day NDSI Composite'
  	elif(variable=='EVI'):
                collectionName = 'MCD43A4_EVI';
		collectionLongName = 'MODIS 16-day EVI Composite'
  	elif(variable=='BAI'):
                collectionName = 'LC8_L1T_32DAY_BAI';
		collectionLongName = 'Landsat 8 L1T TOA 32-day BAI Composite'
  	elif(variable=='NBRT'):
                collectionName = 'LE7_L1T_32DAY_NBRT';
		collectionLongName = 'Landsat 7 L1T TOA 32-day BAI Composite'
  	elif(variable=='pr'):
		collectionName = 'IDAHO_EPSCOR/GRIDMET';
		collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
	collection = ee.ImageCollection(collectionName).select([variable],[variable]);

	return (collection,collectionName,collectionLongName);

def filter_time(collection,dateStart,dateEnd,CLIMATOLOGY):
	if(CLIMATOLOGY==1):
		collection = collection.filterDate(dateStart,dateEnd);
	else:
		collection = collection.filterDate(dateStart,dateEnd);

	return(collection);

#===========================================
#   FIRST_FILTER_DOMAIN(for filterBounds)
#===========================================
#def filter_domain1(collection,domainType, subdomain):
        #if(domainType=='points'):
                #collection =collection.filterBounds(subdomain);
        #elif(domainType=='states'):
        #elif(domainType=='conus'):
        #elif(domainType=='polygon'):
                #collection =collection.filterBounds(subdomain);
#        return (collection);

#===========================================
#   GET_STATISTIC 
#===========================================
def get_statistic(collection,variable,statistic):
	if(statistic=='Mean'):
		collection = collection.mean();
	elif(statistic=='Median'):
		collection = collection.median();
	elif(statistic=='Total'):
		collection = collection.sum();

	return (collection);

#===========================================
#   SECOND_FILTER_DOMAIN (for clipping/masking)
#===========================================
def filter_domain2(collection,domainType, subdomain):
	if(domainType=='points'):
		fc = ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8');
		collection= collection.clip(fc.geometry());
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
def map_collection(collection,variable,anomOrValue):
	if(variable=='NDVI' or variable=='EVI' or variable=='BAI'):
		if(anomOrValue=='anom'):
			minColorbar=-.4
			maxColorbar=.4
			colorbarOptions = {
			    'min':minColorbar,
			    'max':maxColorbar,
			    'palette':"A50026,D73027,F46D43,FDAE61,FEE08B,FFFFBF,D9EF8B,A6D96A,66BD63,1A9850,006837",
			    'opacity':".85", #range [0,1]
			}
		else:
			minColorbar=-.1
			maxColorbar=.9
			colorbarOptions = {
			    'min':minColorbar,
			    'max':maxColorbar,
			    'palette':"FFFFE5,F7FCB9,D9F0A3,ADDD8E,93D284,78C679,41AB5D,238443,006837,004529",
			    'opacity':".85", #range [0,1]
			}
	elif(variable=='NDSI'):
		if(anomOrValue=='anom'):
			minColorbar=-.5
			maxColorbar=.5
			colorbarOptions = {
			    'min':minColorbar,
			    'max':maxColorbar,
			    'palette':"A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695",
			    'opacity':".85", #range [0,1]
			}
		else:
			minColorbar=-.1
			maxColorbar=.9
			colorbarOptions = {
			    'min':minColorbar,
			    'max':maxColorbar,
			    'palette':"08306B,08519C,2171B5,4292C6,6BAED6,9ECAE1,C6DBEF,DEEBF7,F7FBFF",
			    'opacity':".85", #range [0,1]
			}
	elif(variable=='BAI'):
                if(anomOrValue=='anom'):
                        minColorbar=-.5
                        maxColorbar=.5
                        colorbarOptions = {
                            'min':minColorbar,
                            'max':maxColorbar,
                            'palette':"A50026,D73027,F46D43,FDAE61,FEE090,FFFFBF,E0F3F8,ABD9E9,74ADD1,4575B4,313695",
                            'opacity':".85", #range [0,1]
                        }
                else:
                        minColorbar=-.1
                        maxColorbar=.9
                        colorbarOptions = {
                            'min':minColorbar,
                            'max':maxColorbar,
                            'palette':"08306B,08519C,2171B5,4292C6,6BAED6,9ECAE1,C6DBEF,DEEBF7,F7FBFF",
                            'opacity':".85", #range [0,1]
                        }
	elif(variable=='NBRT'):
                if(anomOrValue=='anom'):
                        minColorbar=-.02
                        maxColorbar=.02
                        colorbarOptions = {
                            'min':minColorbar,
                            'max':maxColorbar,
                            'palette':"006837,1A9850,66BD63,A6D96A,D9EF8B,FFFFBF,FEE08B,FDAE61,F46D43,D73027,A50026",
                            'opacity':".85", #range [0,1]
                        }
                else:
                        minColorbar=.95;
                        maxColorbar=1.0;
                        colorbarOptions = {
                            'min':minColorbar,
                            'max':maxColorbar,
                            'palette':"FFFFFF,F0F0F0,D9D9D9,BDBDBD,AAAAAA,969696,737373,525252,252525,000000",
                            'opacity':".85", #range [0,1]
                        }

	elif(variable=='pr'):
                minColorbar=0
                maxColorbar=200
		if(anomOrValue=='anom'):
		 	colorbarOptions = {
			    'min':minColorbar,
			    'max':maxColorbar,
			    'palette':"67001F,B2182B,D6604D,F4A582,FDDBC7,F7F7F7,D1E5F0,92C5DE,4393C3,2166AC,053061",
			    'opacity':".85", #range [0,1]
			}
		else:
		 	colorbarOptions = {
			    'min':minColorbar,
			    'max':maxColorbar,
			    'palette':"FFFFD9,EDF8B1,C7E9B4,7FCDBB,41B6C4,1D91C0,225EA8,0C2C84",
			    'opacity':".85", #range [0,1]
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
        timeSeries= [['Dates','NDVI']] + timeSeries

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
