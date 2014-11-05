import ee
import time
import datetime
import numpy


def get_collection(product,variable,point,dateStart,dateEnd):
	from functions import ndvi_calc_L5L7,ndvi_calc_L8

	######################################################
	#### GET COLLECTION FOR LAT/LON POINT
	######################################################
	collectionName = 'LT5_L1T_TOA';
	band1='B4'
	band2='B3'
        l5_coll = ee.ImageCollection(collectionName).filterBounds(point).filterDate(dateStart,dateEnd);
        l5_coll_ndvi = l5_coll.map(ndvi_calc_L5L7)
	del l5_coll;

	collectionName = 'LE7_L1T_TOA';
        l7_coll = ee.ImageCollection(collectionName).filterBounds(point).filterDate(dateStart, dateEnd);
        l7_coll_ndvi = l7_coll.map(ndvi_calc_L5L7)
	del l7_coll;

	collectionName = 'LC8_L1T_TOA';
        l8_coll = ee.ImageCollection(collectionName).filterBounds(point).filterDate(dateStart,dateEnd);
        l8_coll_ndvi = l8_coll.map(ndvi_calc_L8)
	del l8_coll;
	######################################################
        #### Merge image collections
	######################################################
        collection = ee.ImageCollection(l5_coll_ndvi.merge(l7_coll_ndvi));
	del l7_coll_ndvi;
        collection= ee.ImageCollection(collection.merge(l8_coll_ndvi));
	del l8_coll_ndvi;

	return (collection);

def map_collection(collection,minColorbar,maxColorbar):

 	colorbarPar = {
            'min':minColorbar,
            'max':maxColorbar,
            'palette':"FFFFE5,F7FCB9,D9F0A3,ADDD8E,93D284,78C679,41AB5D,238443,006837,004529",
	    'opacity':".85", #range [0,1]
        }
        mapid = collection.median().getMapId(colorbarPar)

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
