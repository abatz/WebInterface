from collections import defaultdict
import datetime
import json
import logging
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
            continue
            ##ts_dict[pnt].append([date_str, 'None'])
            ##graph_dict[pnt].append([time_int, None])

    '''
    Note ee spits out data for points in one list,
    stringing the point data together
    '''
    timeSeriesData = []
    timeSeriesGraphData = []  
    for pnt, ts_data in sorted(ts_dict.items()):
        data_dict = {
            'LongLat': '{0:0.4f},{1:0.4f}'.format(*pnt),
            'Data':sorted(ts_data)
        }
        timeSeriesData.append(data_dict)
    for i, (pnt, graph_data) in enumerate(sorted(graph_dict.items())):
        data_dict_graph = {
            'MarkerColor':marker_colors[i],
             'LongLat': '{0:0.4f},{1:0.4f}'.format(*pnt),
             'Data':sorted(graph_data)
        }
        timeSeriesGraphData.append(data_dict_graph)
    return timeSeriesData, timeSeriesGraphData

#==================================================
#   JOIN TIME SERIES DATA
#==================================================

def join_time_series_data(dataList,timeSeriesData,
                          timeSeriesGraphData,template_values):
    """

    Args:
        dataList:
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
