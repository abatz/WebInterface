from collections import defaultdict
import datetime
import logging

import ee

import processingMethods

#===========================================
#  FORMAT_DATA_FOR_HIGHCHARTS
#===========================================
def set_time_series_data(dataList, template_values):
    """
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
    """

    var = template_values['variable'][1:]
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
            #val = float(row[4])
            val = processingMethods.modify_units_in_timeseries(float(row[4]),var,units)
            ts_dict[pnt].append([date_str, '{0:0.4f}'.format(val)])
            graph_dict[pnt].append([time_int, val])
        except:
            continue
            ts_dict[pnt].append([date_str, 'None'])
            #graph_dict[pnt].append([time_int, None])

    '''
    Note ee spits out data for points in one list,
    stringing the point data together
    '''
    timeSeriesTextData = [];timeSeriesGraphData = []
    for pnt, ts_data in sorted(ts_dict.items()):
        data_dict = {
            'LongLat': '{0:0.4f},{1:0.4f}'.format(*pnt),
            'Data':sorted(ts_data)
        }
        timeSeriesTextData.append(data_dict)

    for i, (pnt, graph_data) in enumerate(sorted(graph_dict.items())):
        data_dict_graph = {
            'MarkerColor':marker_colors[i],
            'LongLat': '{0:0.4f},{1:0.4f}'.format(*pnt),
            'Data':sorted(graph_data)
        }
        timeSeriesGraphData.append(data_dict_graph)
    return timeSeriesTextData, timeSeriesGraphData
