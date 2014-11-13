import ee
import time
import datetime
import numpy

def get_collection(product,variable,dateStart,dateEnd):
  	if(variable=='NDVI'):
                #collectionName = 'MYD09GA_NDVI';
                collectionName = 'LE7_L1T_32DAY_NDVI';
		collection = ee.ImageCollection(collectionName).filterDate(dateStart,dateEnd).select([variable],[variable]);
  	elif(variable=='NDSI'):
                collectionName = 'LC8_L1T_32DAY_NDSI';
		collection = ee.ImageCollection(collectionName).filterDate(dateStart,dateEnd).select([variable],[variable]);
	return (collection);


def filter_domain(collection,domainType, domain):
	if(domainType=='point'):
		collection =collection.filterBounds(domain);
		fc = ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8');
		collection= collection.median().clip(fc.geometry());
	elif(domainType=='state'):
		fc = ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8').filter(ee.Filter.eq('Name', domain));
		collection= collection.median().clip(fc.geometry());


def map_collection(collection,minColorbar,maxColorbar,variable):

	if(variable=='NDVI'):
		colorbarPar = {
		    'min':minColorbar,
		    'max':maxColorbar,
		    'palette':"FFFFE5,F7FCB9,D9F0A3,ADDD8E,93D284,78C679,41AB5D,238443,006837,004529",
		    'opacity':".85", #range [0,1]
		}
	elif(variable=='NDSI'):
		colorbarPar = {
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

	#fc = ee.FeatureCollection('ft:1fRY18cjsHzDgGiJiS2nnpUU3v9JPDc2HNaR7Xk8');
	#collection= collection.median().clip(fc.geometry());
        mapid = collection.getMapId(colorbarPar)

	return mapid;

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
        variableList_filt = [x for x in variableList if x is not None]
        #meanNDVI = numpy.mean(variableList_filt,axis=0)
        #medianNDVI = numpy.median(variableList_filt,axis=0)
        #maxNDVI = numpy.max(variableList_filt,axis=0)
        #minNDVI = numpy.min(variableList_filt,axis=0)

	######################################################
        #### RETURN 
	######################################################
	return (timeSeries)
