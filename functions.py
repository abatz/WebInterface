#############################################
##       FUNCTIONS                         ##
#############################################

import ee
def ndvi_calc_L5L7(refl_toa):
    ndvi_img = refl_toa.select("B4", "B3").normalizedDifference().select([0],['NDVI'])
    return ee.Image(ndvi_img.copyProperties(refl_toa,['system:index','system:time_start','system_time_end']))

def ndvi_calc_L8(refl_toa):
    ndvi_img = refl_toa.select("B5", "B4").normalizedDifference().select([0],['NDVI'])
    return ee.Image(ndvi_img.copyProperties(refl_toa,['system:index','system:time_start','system_time_end']))


def gridmet_ppt_func(gridmet_image):
        doy = ee.Number(ee.Algorithms.Date(gridmet_image.get("system:time_start")).getRelative('day', 'year')).add(1).double()
        return gridmet_image.select(['pr'], ['PPT']).set({
            'DOY':doy, 'system:index':gridmet_image.get('system:index'),
            'system:time_start':gridmet_image.get('system:time_start'),
            'system:time_end':gridmet_image.get('system:time_end')})


#def get_variable(collection,variable,band1,band2):
#    collection = collection.select(band1, band2).normalizedDifference().select([0],[variable])
#    return ee.Image(collection.copyProperties(collection,['system:index','system:time_start','system_time_end']))
