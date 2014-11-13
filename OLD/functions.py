#############################################
##       FUNCTIONS                         ##
#############################################
import ee


# A mapping from a common name to the sensor-specific bands.
#var LC8_BANDS = ['B2',   'B3',    'B4',  'B5',  'B6',    'B7',    'B10'];
#var STD_NAMES = ['blue', 'green', 'red', 'nir', 'swir1', 'swir2', 'temp'];

#for Landsat5 or 7, infrared=B4, red=B3
def get_ndvi_L5L7(collection):
    var_img = collection.select("B4", "B3").normalizedDifference().select([0],['NDVI'])
    return ee.Image(var_img.copyProperties(collection,['system:index','system:time_start','system_time_end']))

def get_satvi_L5L7(collection):
    band3 = collection.select("B3").select([0],['B3'])
    #band5 = collection.select("B5").select([0],['B5'])
    #band7 = collection.select("B7").select([0],['B7'])
    
    #var_img = collection.select("B4", "B3").normalizedDifference().select([0],['SATVI'])
    var_img=band3;
    return ee.Image(var_img.copyProperties(collection,['system:index','system:time_start','system_time_end']))




#for Landsat8, infrared=B5, red=B4
def get_ndvi_L8(collection):
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
