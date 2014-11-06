import ee
import time
import datetime
import numpy
		
def get_collection(product,variable,dateStart,dateEnd):
	#from functions import gridmet_ppt_func
	from functions import get_ppt

	######################################################
	#### GET COLLECTION FOR LAT/LON POINT
	######################################################
	collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collection = ee.ImageCollection(collectionName).filterDate(dateStart,dateEnd);
        #collection= collection.map(gridmet_ppt_func)
        collection= collection.map(get_ppt)

	return (collection);

def get_climatologycollection(product,variable,dateStart,dateEnd):
	from functions import gridmet_ppt_func
        from functions import get_ppt

	dayStart = 1;
	dayEnd = 31;
	doy_filter = ee.Filter(ee.Filter.calendarRange(
        	dayStart, dayEnd, 'day_of_year'))
	
	yearStart = 2006 
	yearEnd=2010

        collectionName = 'IDAHO_EPSCOR/GRIDMET';
        collection = ee.ImageCollection(collectionName).filterDate(yearStart,yearEnd).filter(doy_filter);
        collection= collection.map(gridmet_ppt_func)

        return (collection);


def get_anomalycollection(product,variable,dateStart,dateEnd):
	collClim = get_climatologycollection(product,variable,dateStart,dateEnd)
	coll = get_collection(product,variable,dateStart,dateEnd)


#	def get_mean_difference(collection):
#		return ppt_image.subtract(
#            	ee.Image(ee.ImageCollection.fromImages(collection.get('doy_match')).mean()))
#
#    anomaly_coll = ee.ImageCollection(ppt_join_coll.map(anomaly_func))
	

def map_collection(collection,minColorbar,maxColorbar):

 	colorbarOptions = {
            'min':minColorbar,
            'max':maxColorbar,
            'palette':"FFFFD9,EDF8B1,C7E9B4,7FCDBB,41B6C4,1D91C0,225EA8,0C2C84",
	    'opacity':".85", #range [0,1]
        }
        mapid = collection.sum().getMapId(colorbarOptions)

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

        #### FILTER OUT "None" VALUES
        variableList_filt = [x for x in variableList if x is not None]

	######################################################
        #### CALCULATE NDVI STATS
	######################################################
        #meanNDVI = numpy.mean(variableList_filt,axis=0)
        #medianNDVI = numpy.median(variableList_filt,axis=0)
        #maxNDVI = numpy.max(variableList_filt,axis=0)
        #minNDVI = numpy.min(variableList_filt,axis=0)

	######################################################
        #### RETURN 
	######################################################
	return (timeSeries)
