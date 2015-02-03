import ee
import time
import datetime
import numpy
import json
import collectionMethods
#===========================================
#  FORMAT_DATA_FOR_HIGHCHARTS 
#===========================================
def format_data_for_highcharts(mc,units,dataList,var,dataList2,timeSeriesData,timeSeriesGraphData,product):
######################################################
#### Format data for highcharts figure and data tabs
#### Each point gets it's own dictionary
#### timeSeriesData[idx] = {MarkerColor:marker_colors[idx],LongLat:ll_string, Data:[[Date1,val1],[Date2, val2]]}
######################################################
    #Format data
    point_cnt = 0;
    for idx, data in enumerate(dataList):
        lon = round(data[1],4);
        lat = round(data[2],4);
        if idx == 0:
        #To keep track of when data point changes
            lon_init = lon;
            lat_init = lat;
            data_dict = {};
            data_dict_graph = {};
            point_cnt+=1;
        else:
            if abs(float(lon) - float(lon_init)) >0.0001 or abs(float(lat) - float(lat_init)) > 0.0001:
                #New data point
                lon_init = lon;
                lat_init = lat;
                timeSeriesData.append(data_dict);
                timeSeriesGraphData.append(data_dict_graph);
                data_dict = {};
                data_dict_graph = {};
                point_cnt+=1;
        if not data_dict:
            data_dict = {
                'LongLat': str(lon) + ',' + str(lat),
                'Data': []
            }
            data_dict_graph = {
                'MarkerColor':mc[point_cnt - 1],
                'LongLat': str(lon) + ',' + str(lat),
                'Data': []
            }
        #=============
        #extract the time,date_string,val
        #=============
        time,date_string,val=collectionMethods.extract_data_from_timeseries_element(\
            idx,data,var,dataList2,product);
        #=============
        # check units
        #=============
        val=collectionMethods.check_units_in_timeseries(val,var,units);
        #=============
        data_dict['Data'].append([date_string,val])
        data_dict_graph['Data'].append([time,val])

    timeSeriesData.append(data_dict)
    timeSeriesGraphData.append(data_dict_graph)

    return (timeSeriesData,timeSeriesGraphData);
