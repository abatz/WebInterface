from collections import defaultdict

import datetime

import json
import time

import ee
import numpy

import collectionMethods
#===========================================
#  FORMAT_DATA_FOR_HIGHCHARTS
#===========================================
def set_time_series_data(dataList,template_values):
    '''
    Args:
        dataList: nested list of data from EarthEngine getRegion method
        template_values: dictionary

    Returns:
        time series data for displaying as text
        time series data for plotting
    '''

    var = template_values['variable']
    units = template_values['units']
    marker_colors = template_values['marker_colors']

    # Format data for highcharts
    # Group data by point while reading
    ts_dict = defaultdict(list)
    graph_dict = defaultdict(list)
    for row in dataList:
        pnt = (float(row[1]), float(row[2]))
        ##pnt = '{0:0.4f},{1:0.4f}'.format(*pnt)
        time_int = int(row[3])
        date_obj = datetime.datetime.utcfromtimestamp(float(time_int) / 1000)
        date_str = date_obj.strftime('%Y-%m-%d')
        try:
            val = float(row[4])
            ts_dict[pnt].append([date_str, '{0:0.4f}'.format(val)])
            graph_dict[pnt].append([time_int, val])
        except:
            ts_dict[pnt].append([date_str, 'None'])
            graph_dict[pnt].append([time_int, None])

    '''
    Note ee spits out data for points in one list,
    stringing the point data together
    '''
    timeSeriesData = []
    timeSeriesGraphData = []  
    for pnt, ts_data in sorted(ts_dict.items()):
        data_dict = {
            'LongLat': '{0:0.4f},{1:0.4f}'.format(*pnt),
            'Data':ts_data
        }
        timeSeriesData.append(data_dict)
    for i, (pnt, graph_data) in enumerate(sorted(graph_dict.items())):
        data_dict_graph = {
            'MarkerColor':marker_colors[i],
             'LongLat': '{0:0.4f},{1:0.4f}'.format(*pnt),
             'Data':graph_data
        }
        timeSeriesGraphData.append(data_dict_graph)
    return timeSeriesData, timeSeriesGraphData


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

#==================================================
#   JOIN TIME SERIES DATA
#==================================================

def join_time_series_data(dataList,dataList2,timeSeriesData,
                          timeSeriesGraphData,template_values):
    """

    Args:
        dataList:
        dataList2:
        timeSeriesData:
        timeSeriesGraphData:
        template_values:

    Returns:
        time series data for displaying as text
        time series data for plotting
    """

    var = template_values['variable']
    units = template_values['units']
    for idx, data in enumerate(dataList):
        LongLat = '{0:0.4f},{1:0.4f}'.format(data[1], data[2])
        #=============
        #extract the time,date_string,val
        #=============
        time,date_string,val=collectionMethods.extract_data_from_timeseries_element(
            idx,data,var,dataList2)
        val = collectionMethods.check_units_in_timeseries(val,var,units);
        #Find point in timeSeriesData and append data
        for p_idx,p_datadict in enumerate(timeSeriesData):
            if p_datadict['LongLat'] != LongLat:
                continue
            timeSeriesData[p_idx]['Data'].append([date_string,val])
            if isinstance(val, basestring):
                timeSeriesGraphData[p_idx]['Data'].append([time,None])
            else:
                timeSeriesGraphData[p_idx]['Data'].append([time,val])
    return timeSeriesData, timeSeriesGraphData
