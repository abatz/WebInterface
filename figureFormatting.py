import ee
import time
import datetime
import numpy
import json
import collectionMethods
#===========================================
#  FORMAT_DATA_FOR_HIGHCHARTS
#===========================================
def set_time_series_data(dataList,template_values):
    '''
    dataList -- main collection
    '''
    var = template_values['variable']
    units = template_values['units']
    marker_colors = template_values['marker_colors']
    timeSeriesData = [];timeSeriesGraphData = []
    dates = list(zip(*dataList)[0])
    lons = list(zip(*dataList)[1])
    lats = list(zip(*dataList)[2])
    times = list(zip(*dataList)[3])
    data = list(zip(*dataList)[4])

    #Format data for highcharts
    ts_data = []
    graph_data =[]
    for idx,d in enumerate(data):
        date_string = dates[idx]
        if(date_string[0:7]=='MCD43A4'):
            date_string = date_string[12:16] + '-' + date_string[17:19] + '-' + date_string[20:22]
        elif(date_string[0:3]=='LT5'): #LT50380312011091PAC01
            date_string =date_string; #messed up
        else:
            i=date_string.rfind('_');
            if(i==-1):
                date_string = date_string[0:4] + '-' + date_string[4:6] + '-' + date_string[6:8]
            else:
                date_string = date_string[i+1:i+5] + '-' + date_string[i+5:i+7] + '-' + date_string[i+7:i+9]
        try:
            val= round(float(data[idx]),4)
        except:
            val = None
        if val is None:
            ts_data.append([date_string,'None'])
        else:
            ts_data.append([date_string,val])
        try:
            graph_data.append([int(times[idx]),val])
        except:
            #Vars wb, tmean do not return times.
            #Need to convert date_string to integer time
            #FIX ME: conversion not done correctly, posted to g-group
            time_tuple = (int(date_string[0:4]),int(date_string[5:7]),int(date_string[8:10]),13, 59, 27, 2, 317, 0)
            timestamp = int(time.mktime(time_tuple))
            graph_data.append([timestamp,val])

    '''
    Note ee spits out data for points in one list,
    stringing the point data together
    '''
    #Find unique lats, i.e unique points points
    unique_lats = list(set(lats))
    #Find the indices in the data where points change
    point_indices = []
    for lat in unique_lats:
        point_indices.append(lats.index(lat))
    point_indices = sorted(point_indices)
    #Loop over points and compile data and graph data
    timeSeriesData = []
    timeSeriesGraphData = []
    for i,p_idx in enumerate(point_indices):
        i_start = p_idx
        if i == len(point_indices) -1:
            i_end = len(data)
        else:
            i_end = point_indices[i+1]
        data_dict = {
            'LongLat': str(round(lons[p_idx],4)) + ',' + str(round(lats[p_idx],4)),
            'Data':ts_data[i_start:i_end]
        }
        data_dict_graph = {
            'MarkerColor':marker_colors[i],
            'LongLat': str(round(lons[p_idx],4)) + ',' + str(round(lats[p_idx],4)),
            'Data':graph_data[i_start:i_end]
        }
        timeSeriesData.append(data_dict)
        timeSeriesGraphData.append(data_dict_graph)
    return timeSeriesData, timeSeriesGraphData


#Old code used when data requests where split up into 6year chunks.
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
        if isinstance(val,basestring):
            data_dict_graph['Data'].append([time,None])
        else:
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
            if isinstance(val,basestring):
                timeSeriesGraphData[p_idx]['Data'].append([time,None])
            else:
                timeSeriesGraphData[p_idx]['Data'].append([time,val])
    return timeSeriesData,timeSeriesGraphData
