from collections import defaultdict
import datetime
import logging

import ee
#===========================================
#  FORMAT_DATA_FOR_HIGHCHARTS
#===========================================
def set_time_series_data(dataList, template_values,timeSeriesTextData = [],timeSeriesGraphData = []):
    '''
    Args:
        dataList: nested list of data from EarthEngine getRegion method
        template_values: dictionary
        timeSeriesTextData: time series data for displaying as text,
                            if not empty, data in dataList will be appended
        timeSeriesGraphData: time series data for plotting,
                             if not empty, data in dataList will be appended
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
            #ts_dict[pnt].append([date_str, 'None'])
            #graph_dict[pnt].append([time_int, None])

    '''
    Note ee spits out data for points in one list,
    stringing the point data together
    '''
    #Check if timeSeriesTextData,timeSeriesGraphData not empty
    ts_text_append = False
    if timeSeriesTextData:ts_text_append = True
    ts_graph_append = False
    if timeSeriesTextData:ts_graph_append = True
    for pnt, ts_data in sorted(ts_dict.items()):
        if not ts_text_append:
            data_dict = {
                'LongLat': '{0:0.4f},{1:0.4f}'.format(*pnt),
                'Data':sorted(ts_data)
            }
            timeSeriesTextData.append(data_dict)
        else:
            #Find point in timeSeriesTextData and append data
            for p in timeSeriesTextData:
                if p['LongLat'] != '{0:0.4f},{1:0.4f}'.format(*pnt):
                    continue
                p['Data'].append(sorted(ts_data))

    for i, (pnt, graph_data) in enumerate(sorted(graph_dict.items())):
        if not ts_graph_append:
            data_dict_graph = {
                'MarkerColor':marker_colors[i],
                'LongLat': '{0:0.4f},{1:0.4f}'.format(*pnt),
                'Data':sorted(graph_data)
            }
            timeSeriesGraphData.append(data_dict_graph)
        else:
            #Find point in timeSeriesTextData and append data
            for p in timeSeriesGraphData:
                if p['LongLat'] != '{0:0.4f},{1:0.4f}'.format(*pnt):
                    continue
                p['Data'].append(sorted(graph_data))
    return timeSeriesTextData, timeSeriesGraphData
