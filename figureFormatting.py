import ee
import time
import datetime
import numpy
import json
import collectionMethods
#===========================================
#  FORMAT_DATA_FOR_HIGHCHARTS
#===========================================
def set_initial_time_series_data(dataList,dataList2,template_values):
    '''
    dataList -- main collection
    dataList2 -- extra collections for derived variables tmean, wb
    '''
    var = template_values['variable']
    units = template_values['units']
    marker_colors = template_values['marker_colors']
    timeSeriesData = [];timeSeriesGraphData = []
    #Format data
    point_cnt = 0
    for idx, data in enumerate(dataList):
        lon = round(data[1],4);lat = round(data[2],4)
        if idx == 0:
            #To keep track of when data point changes
            lon_init = lon;lat_init = lat
            data_dict = {}
            data_dict_graph = {}
            point_cnt+=1
        else:
            if abs(float(lon) - float(lon_init)) >0.0001 or abs(float(lat) - float(lat_init)) > 0.0001:
                #New data point
                lon_init = lon;lat_init = lat
                timeSeriesData.append(data_dict)
                timeSeriesGraphData.append(data_dict_graph)
                data_dict = {};data_dict_graph = {}
                point_cnt+=1
        if not data_dict:
            data_dict = {
                'LongLat': str(lon) + ',' + str(lat),
                'Data': []
            }
            data_dict_graph = {
                'MarkerColor':marker_colors[point_cnt - 1],
                'LongLat': str(lon) + ',' + str(lat),
                'Data': []
            }
        #=============
        #extract the time,date_string,val
        #=============
        time,date_string,val = collectionMethods.extract_data_from_timeseries_element(\
            idx,data,var,dataList2);
        #=============
        # check units
        #=============
        val = collectionMethods.check_units_in_timeseries(val,var,units)
        data_dict['Data'].append([date_string,val])
        data_dict_graph['Data'].append([time,val])
    timeSeriesData.append(data_dict)
    timeSeriesGraphData.append(data_dict_graph)
    return timeSeriesData,timeSeriesGraphData

def join_time_series_data(dataList,dataList2,timeSeriesData,timeSeriesGraphData,template_values):
    var = template_values['variable']
    units = template_values['units']
    for idx, data in enumerate(dataList):
        lon = round(data[1],4);
        lat = round(data[2],4);
        LongLat = str(lon) + ',' + str(lat)
        #=============
        #extract the time,date_string,val
        #=============
        time,date_string,val=collectionMethods.extract_data_from_timeseries_element(\
            idx,data,var,dataList2)
        val = collectionMethods.check_units_in_timeseries(val,var,units);
        #Find point in timeSeriesData and append data
        for p_idx,p_datadict in enumerate(timeSeriesData):
            if p_datadict['LongLat'] != LongLat:
                continue
            timeSeriesData[p_idx]['Data'].append([date_string,val])
            timeSeriesGraphData[p_idx]['Data'].append([time,val])
    return timeSeriesData,timeSeriesGraphData

