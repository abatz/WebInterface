#############################################
##       FUNCTIONS                         ##
#############################################
import ee
def ndvi_calc_L5L7(collection):
    ndvi_img = collection.select("B4", "B3").normalizedDifference().select([0],['NDVI'])
    return ee.Image(ndvi_img.copyProperties(collection,['system:index','system:time_start','system_time_end']))

def ndvi_calc_L8(collection):
    ndvi_img = collection.select("B5", "B4").normalizedDifference().select([0],['NDVI'])
    return ee.Image(ndvi_img.copyProperties(collection,['system:index','system:time_start','system_time_end']))

def get_ppt(collection):
    ppt_img = collection.select(['pr'], ['PPT'])
    return ee.Image(ppt_img.copyProperties(collection,['system:index','system:time_start','system_time_end']))

def gridmet_ppt_func(gridmet_image):
        doy = ee.Number(ee.Algorithms.Date(gridmet_image.get("system:time_start")).getRelative('day', 'year')).add(1).double()
        return gridmet_image.select(['pr'], ['PPT']).set({
            'DOY':doy, 'system:index':gridmet_image.get('system:index'),
            'system:time_start':gridmet_image.get('system:time_start'),
            'system:time_end':gridmet_image.get('system:time_end')})

#not sure how to handle multiple arguments with function call
#def get_variable(collection,variable,band1,band2):
#    collection = collection.select(band1, band2).normalizedDifference().select([0],[variable])
#    return ee.Image(collection.copyProperties(collection,['system:index','system:time_start','system_time_end']))
