import ee
import time
import datetime
import numpy
#===========================================
#    GET_COLLECTION
#===========================================
def get_collection(product,variable,dateStart,dateEnd):

  	if(variable=='NDVI'):
                collectionName = 'LE7_L1T_32DAY_NDVI';
		collectionLongName = 'Landsat 7 L1T TOA 32-Day NDVI Composite'

                #collectionName = 'MCD43A4_NDVI';
		#collectionLongName = 'MODIS 16-day NDVI'
		def ndvi_calc_L5L7(refl_toa): 
		    ndvi_img = refl_toa.select("B4", "B3").normalizedDifference().select([0],['NDVI'])
		    return ee.Image(ndvi_img.copyProperties(refl_toa,['system:index','system:time_start','system_time_end']))

                collectionName = 'LE7_L1T_TOA';
		collectionLongName = 'Landsat 7 L1T TOA, ND of IR and R bands';
		collection = ee.ImageCollection(collectionName).filterDate(dateStart,dateEnd).map(ndvi_calc_L5L7);
  	elif(variable=='NDSI'):
                #collectionName = 'LC8_L1T_32DAY_NDSI';
		#collectionLongName = 'Landsat 8 L1T TOA 32-Day NDSI Composite'

                collectionName = 'MCD43A4_NDSI';
		collectionLongName = 'MODIS 16-day NDSI Composite'
		collection = ee.ImageCollection(collectionName).filterDate(dateStart,dateEnd).select([variable],[variable]);
  	elif(variable=='pr'):
		collectionName = 'IDAHO_EPSCOR/GRIDMET';
		collectionLongName = 'gridMET 4-km observational dataset(University of Idaho)';
		collection = ee.ImageCollection(collectionName).filterDate(dateStart,dateEnd).select([variable],[variable]);

	return (collection,collectionLongName);


#===========================================
#   FIRST_FILTER_DOMAIN(for filterBounds)
#===========================================
def filter_domain1(collection,domainType, subdomain):
        if(domainType=='points'):
                collection =collection.filterBounds(subdomain);
        #elif(domainType=='states'):
        #elif(domainType=='conus'):
        #elif(domainType=='polygon'):
                #collection =collection.filterBounds(subdomain);

        return (collection);

#===========================================
#   GET_STATISTIC 
#===========================================
def get_statistic(collection,variable):
	if(variable=='NDVI'):
		collection = collection.median();
	elif(variable=='NDSI'):
		collection = collection.median();
	elif(variable=='pr'):
		collection = collection.sum();

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
def map_collection(collection,minColorbar,maxColorbar,variable):
	if(variable=='NDVI'):
		colorbarOptions = {
		    'min':minColorbar,
		    'max':maxColorbar,
		    'palette':"FFFFE5,F7FCB9,D9F0A3,ADDD8E,93D284,78C679,41AB5D,238443,006837,004529",
		    'opacity':".85", #range [0,1]
		}
	elif(variable=='NDSI'):
		colorbarOptions = {
		    'min':minColorbar,
		    'max':maxColorbar,
		    'palette':"08306B,08519C,2171B5,4292C6,6BAED6,9ECAE1,C6DBEF,DEEBF7,F7FBFF",
		    'opacity':".85", #range [0,1]
		}
	elif(variable=='pr'):
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
