import logging

import ee

#===========================================
#    GET_COLLECTION
#===========================================
def get_collection(product, variable):
    """Return an EarthEngine image collection for given product and variable

    Args:
        product: single character indicating the product (G, M, 8, or 5)
        variable: string indicating the variable/band to return
            (i.e. NDVI, EVI, pet, tmmn)
    Returns:
        Output from product collection functions
        Tuple of the following:
            EarthEngine image collection object
            String of the collection name
            String of the collection description
            String of the variable description (may be the input variable)
            String of additional notes about the collection
    """
    if product == 'G':        
        return get_gridmet_collection(variable)
    elif product == 'M':
        return get_modis_collection(variable)
    elif product == '8':
        return get_landsat8_daily_collection(variable)
    elif product == '5':
        return get_landsat5_daily_collection(variable)
        ##return get_landsat457_daily_collection(variable)
    ## How should this function fail gracefully if the inputs are bad?
    ## Should it return an exception?
    ##else:
    ##    pass

#===========================================
#    LANDSAT457 Daily
#===========================================
def get_landsat457_daily_collection(variable):
    """Return the daily merged image collection for Landsat 4, 5, and 7

    Args:
        variable: string indicating the variable/band to return
            (NDVI, NDSI, NDWI, or EVI)
    Returns:
        EarthEngine image collection object
        String of the collection name
        String of the collection description
        String of the input variable
        String of additional notes about the collection
    """
    ## This string could/should be built based on the date range or looking at
    ##   or looking atthe images in the collection
    coll_name = 'LT4_L1T_TOA,LT5_L1T_TOA,LE7_L1T_TOA'
    coll_desc = 'Landsat 4/5/7 Daily {0} (cloud mask applied)'.format(variable)
    var_desc = variable

    ## Select variable after calculating index
    collection = ee.ImageCollection([])
    collection = collection.merge(ee.ImageCollection('LT4_L1T_TOA'))
    collection = collection.merge(ee.ImageCollection('LT5_L1T_TOA'))
    collection = collection.merge(ee.ImageCollection('LE7_L1T_TOA'))
    ## Can this be done on the merged collection?
    collection = collection.map(landsat457_cloud_mask_func)
    if variable == 'NDVI':
        notes = "NDSI calculated from Norm. Diff. of Near-IR and Red bands"
        collection = collection.map(landsat457_ndvi_func)
    elif variable == 'NDSI':
        notes = "NDSI calculated from Norm. Diff. of Green and mid-IR bands"
        collection = collection.map(landsat457_ndsi_func)
    elif variable == 'NDWI':
        notes = "NDWI calculated from Norm. Diff. of near-IR and mid-IR bands"
        collection = collection.map(landsat457_ndwi_func)
    elif variable == 'EVI':
        notes = "EVI calculated from Near-IR, Red and Blue bands"
        collection = collection.map(landsat457_evi_func)
    ## How should this function fail gracefully if the inputs are bad?
    ## Should it return an exception?
    else:
        notes = ''
    collection = collection.select(variable)
    return collection, coll_name, coll_desc, var_desc, notes

#===========================================
#    LANDSAT5 Daily
#===========================================
def get_landsat5_daily_collection(variable):
    """Return the daily image collection for only Landsat 5

    Args:
        variable: string indicating the variable/band to return
            (NDVI, NDSI, NDWI, or EVI)
    Returns:
        EarthEngine image collection object
        String of the collection name
        String of the collection description
        String of the input variable
        String of additional notes about the collection
    """
    coll_name = 'LT5_L1T_TOA'
    coll_desc = 'Landsat 5, daily {0} (cloud mask applied)'.format(variable)
    var_desc = variable
    ## Select variable after calculating index
    collection = ee.ImageCollection(coll_name).map(landsat457_cloud_mask_func)
    if variable == 'NDVI':
        notes = "NDSI calculated from Norm. Diff. of Near-IR and Red bands"
        collection = collection.map(landsat457_ndvi_func)
    elif variable == 'NDSI':
        notes = "NDSI calculated from Norm. Diff. of Green and mid-IR bands"
        collection = collection.map(landsat457_ndsi_func)
    elif variable == 'NDWI':
        notes = "NDWI calculated from Norm. Diff. of near-IR and mid-IR bands"
        collection = collection.map(landsat457_ndwi_func)
    elif variable == 'EVI':
        notes = "EVI calculated from Near-IR, Red and Blue bands"
        collection = collection.map(landsat457_evi_func)
    ## How should this function fail gracefully if the inputs are bad?
    ## Should it return an exception?
    else:
        notes = ''
    collection = collection.select(variable)
    return collection, coll_name, coll_desc, var_desc, notes

#===========================================
#    LANDSAT8 Daily
#===========================================
def get_landsat8_daily_collection(variable):
    """Return the daily image collection for only Landsat 8

    Args:
        variable: string indicating the variable/band to return
            (NDVI, NDSI, NDWI, or EVI)
    Returns:
        EarthEngine image collection object
        String of the collection name
        String of the collection description
        String of the input variable
        String of additional notes about the collection
    """
    coll_name = 'LC8_L1T_TOA'
    coll_desc = 'Landsat 8, daily {0} (cloud mask applied)'.format(variable)
    var_desc = variable

    ## Select variable after calculating index
    collection = ee.ImageCollection(coll_name)
    ## Need to code in Landsat 8 cloud masking
    ##collection = ee.ImageCollection(coll_name).map(landsat8_cloud_mask_func)
    if variable == 'NDVI':
        notes = "NDSI calculated from Norm. Diff. of Near-IR and Red bands"
        collection = collection.map(landsat8_ndvi_func)
    elif variable == 'NDSI':
        notes = "NDSI calculated from Norm. Diff. of Green and mid-IR bands"
        collection = collection.map(landsat8_ndsi_func)
    elif variable == 'NDWI':
        notes = "NDWI calculated from Norm. Diff. of near-IR and mid-IR bands"
        collection = collection.map(landsat8_ndwi_func)
    elif variable == 'EVI':
        notes = "EVI calculated from Near-IR, Red and Blue bands"
        collection = collection.map(landsat8_evi_func)
    ## How should this function fail gracefully if the inputs are bad?
    ## Should it return an exception?
    else:
        notes = ''
    collection = collection.select(variable)
    return collection, coll_name, coll_desc, var_desc, notes

#===========================================
#    LANDSAT8 8-day
#===========================================
## Landsat 8 Day collection functions
##def get_landsat457_8day_collection(variable):
##    """Return the merged 8 day composite image coll. for Landsats 4, 5, and 7
##
##    Args:
##        variable: string indicating the variable/band to return
##            (NDVI, NDSI, NDWI, or EVI)
##    Returns:
##        EarthEngine image collection
##        String of the collection name object
##        String of the collection description
##        String of the input variable
##        String of additional notes about the collection
##    """
##    coll_name = 'LT4_L1T_8DAY_{0},LT5_L1T_8DAY_{0},LE7_L1T_8DAY_{0}'.format(variable)
##    coll_desc = 'Landsat 4/5/7 8-day {0} Composite'.format(variable)
##    collection4 = ee.ImageCollection('LT4_L1T_8DAY_{0}'.format(variable))
##    collection5 = ee.ImageCollection('LT5_L1T_8DAY_{0}'.format(variable))
##    collection7 = ee.ImageCollection('LE7_L1T_8DAY_{0}'.format(variable))
##    collection = ee.ImageCollection(collection4.merge(collection5).merge(collection7))
##    collection = collection.select(variable)
##    if variable == 'NDVI':
##        notes = "NDVI calculated from Norm. Diff. of Near-IR and Red bands"
##    elif variable == 'NDSI':
##        notes = "NDSI calculated from Norm. Diff. of Green and mid-IR bands"
##    elif variable == 'NDWI':
##        notes = "NDWI calculated from Norm. Diff. of near-IR and mid-IR bands"
##    elif variable == 'EVI':
##        notes = "EVI calculated from Near-IR, Red and Blue bands"
##    ## How should this function fail gracefully if the inputs are bad?
##    ## Should it return an exception?
##    else:
##        notes = ''
##    return collection, coll_name, coll_desc, product, variable, notes
##
##def get_landsat8_8day_collection(variable):
##    """Return the 8 day composite image collection for only Landsat 8
##
##    Args:
##        variable: string indicating the variable/band to return
##            (NDVI, NDSI, NDWI, or EVI)
##    Returns:
##        EarthEngine image collection object
##        String of the collection name
##        String of the collection description
##        String of the input variable
##        String of additional notes about the collection
##    """
##    coll_name = 'LT5_L1T_8DAY_{0}'.format(variable)
##    coll_desc = 'Landsat 5, 8-day {0} Composite'.format(variable)
##    collection = ee.ImageCollection('LT5_L1T_8DAY_{0}'.format(variable)).select(variable)
##    if variable == 'NDVI':
##        notes = "NDSI calculated from Norm. Diff. of Near-IR and Red bands"
##    elif variable == 'NDSI':
##        notes = "NDSI calculated from Norm. Diff. of Green and mid-IR bands"
##    elif variable == 'NDWI':
##        notes = "NDWI calculated from Norm. Diff. of near-IR and mid-IR bands"
##    elif variable == 'EVI':
##        notes = "EVI calculated from Near-IR,Red and Blue bands"
##    ## How should this function fail gracefully if the inputs are bad?
##    ## Should it return an exception?
##    else:
##        notes = ''
##    return collection, coll_name, coll_desc, variable, notes
    
#===========================================
#    MODIS 
#===========================================
def get_modis_collection(variable):
    """Return the 8 or 16 day composite image collection for MODIS

    Args:
        variable: string indicating the variable/band to return
            (LST_Day_1km, NDVI, NDSI, NDWI, or EVI)
    Returns:
        EarthEngine image collection object
        String of the collection name
        String of the collection description
        String of the input variable
        String of additional notes about the collection
    """
    coll_name = 'MCD43A4_{0}'.format(variable)
    coll_desc = 'MODIS 16-day {0}'.format(variable)
    var_desc = variable

    if variable == 'NDVI':
        notes = "NDSI calculated from Norm. Diff. of Near-IR and Red bands"
    elif variable == 'NDSI':
        notes = "NDSI calculated from Norm. Diff. of Green and mid-IR bands"
    elif variable == 'NDWI':
        notes = "NDWI calculated from Norm. Diff. of near-IR and mid-IR bands"
    elif variable == 'EVI':
        notes = "EVI calculated from Near-IR,Red and Blue bands"
    elif variable == 'LST_Day_1km':
        notes = "Level 2 LST projected in a Sinusoidal Grid by mapping to 1-km grid"
        coll_name = 'MOD11A2'
        coll_desc = 'MODIS 8-day {0}'.format(variable)
        var_desc = 'Land Surface Temperature during Day'
    ## How should this function fail gracefully if the inputs are bad?
    ## Should it return an exception?
    else:
        notes = ''
    collection = ee.ImageCollection(coll_name).select(variable)
    return collection, coll_name, coll_desc, var_desc, notes
    
#===========================================
#    GRIDMET
#===========================================
def get_gridmet_collection(variable):
    """Return the daily image collection for GRIDMET

    Args:
        variable: string indicating the variable/band to return
            (i.e. pr, tmmx, rmin, vs, pet, etc.)
    Returns:
        EarthEngine image collection object
        String of the collection name
        String of the collection description
        String of the variable description
        String of additional notes about the collection
    """
    coll_name = 'IDAHO_EPSCOR/GRIDMET'
    coll_desc = 'gridMET 4-km observational dataset(University of Idaho)'
    # Don't select variable here since Tmean or WB need to be mapped/calculated first
    collection = ee.ImageCollection(coll_name)
    notes = ""
    if variable == 'pr':
        var_desc = 'Precipitation'
    elif variable == 'tmmx':
        var_desc = 'Maximum Temperature'
    elif variable == 'tmmn':
        var_desc = 'Minimum Temperature'
    elif variable == 'rmin':
        var_desc = 'Minimum Relative Humidity'
    elif variable == 'rmax':
        var_desc = 'Maximum Relative Humidity'
    elif variable == 'srad':
        var_desc = 'Downwelling Shortwave Radiation'
    elif variable == 'vs':
        var_desc = 'Wind Speed Near Surface'
    elif variable == 'sph':
        var_desc = 'Specific Humidity'
    elif variable == 'erc':
        var_desc = 'Energy Release Component'
    elif variable == 'pet':
        notes = "ASCE Standardized Reference ET, estimated using the Penmann Monteith method. See Equation 1 in http://www.kimberly.uidaho.edu/water/asceewri/ascestzdetmain2005.pdf"
        var_desc = 'Reference Evapotranspiration'
    elif variable == 'tmean':
        collection = collection.map(gridmet_tmean_func)
        notes = "Calculated as Average of Min/Max Daily Temperature"
        var_desc = 'Average Temperature'
    elif variable == 'wb':
        collection = collection.map(gridmet_wb_func)
        notes = "Calculated as the difference between precipitation and reference evapotranspiration"
        var_desc = 'Water Balance (PPT-PET)'
    elif variable == 'pdsi':
        ## Rebuild PDSI collection since it isn't technically in the GRIDMET coll.
        coll_name = 'IDAHO_EPSCOR/PDSI'
        collection = ee.ImageCollection(coll_name)
        notes = ""
        var_desc = 'Palmer Drought Severity Index (PDSI)'
    ## How should this function fail gracefully if the inputs are bad?
    ## Should it return an exception?
    else:
        var_desc = ""
    collection = collection.select(variable)
    return collection, coll_name, coll_desc, var_desc, notes

#===========================================
#    Collection Functions
#===========================================
property_list = ['system:index','system:time_start', 'system:time_end']
def landsat457_cloud_mask_func(img):
    """Apply basic ACCA cloud mask to a daily Landsat 4, 5, or 7 image"""
    cloud_mask = ee.Algorithms.Landsat.simpleCloudScore(img).\
        select(['cloud']).lt(ee.Image.constant(50))
    return img.mask(cloud_mask.mask(cloud_mask))

def landsat457_ndvi_func(img):
    """Calculate NDVI for a daily Landsat 4, 5, or 7 image"""
    ## Remove .clamp(-0.1, 1)
    return img.normalizedDifference(["B4","B3"]).select([0], ['NDVI'])\
        .copyProperties(img, property_list)

def landsat457_ndsi_func(img):
    """Calculate NDSI for a daily Landsat 4, 5, or 7 image"""
    ## Removed .clamp(-0.1, 1)
    return img.normalizedDifference(["B2", "B5"]).select([0], ['NDSI'])\
        .copyProperties(img, property_list)

def landsat457_ndwi_func(img):
    """Calculate NDWI (Gao 1996 formulation) for a daily Landsat 4, 5, or 7 image"""
    ## Removed .clamp(-0.1, 1)
    return img.normalizedDifference(["B4", "B5"]).select([0], ['NDWI'])\
        .copyProperties(img, property_list)

def landsat457_evi_func(img):
    """Calculate EVI for a daily Landsat 4, 5, or 7 image"""
    return img.expression('(2.5 * (b("B4") - b("B3"))) / (b("B4") + 6 * b("B3") - 7.5 * b("B1") + 1)')\
        .select([0], ['EVI']).copyProperties(img, property_list)

## DEADBEEF - Need to code in Landsat 8 cloud masking
def landsat8_cloud_mask_func(img):
    return img

def landsat8_ndvi_func(img):
    """Calculate NDVI for a daily Landsat 8 image"""
    ## Removed .clamp(-0.1, 1)
    return img.normalizedDifference(["B5","B4"]).select([0], ['NDVI'])\
        .copyProperties(img, property_list)

def landsat8_ndsi_func(img):
    """Calculate NDSI for a daily Landsat 8 image"""
    ## Removed .clamp(-0.1, 1)
    return img.normalizedDifference(["B3","B6"]).select([0], ['NDSI'])\
        .copyProperties(img, property_list)

def landsat8_ndwi_func(img):
    """Calculate NDWI for a daily Landsat 8 image"""
    ## Removed .clamp(-0.1, 1)
    return img.normalizedDifference(["B6","B5"]).select([0], ['NDWI'])\
        .copyProperties(img, property_list)

def landsat8_evi_func(img):
    """Calculate EVI for a daily Landsat 8 image"""
    ##This formulation should be double checked
    return img.expression('(2.5 * (b("B5") - b("B4"))) / (b("B5") + 6 * b("B4") - 7.5 * b("B2") + 1)')\
        .select([0], ['EVI']).copyProperties(img, property_list)

def gridmet_wb_func(img):
    """Calculate water balance from precip and PET for GRIDMET collection"""
    ##return img.expression("b('pr') - b('pet')")\
    ##    .select([0], ['wb']).copyProperties(img, property_list)
    pr_img = img.select('pr')
    pet_img = img.select('pet')
    return pr_img.subtract(pet_img).select([0], ['wb'])\
        .copyProperties(img, property_list)

def gridmet_tmean_func(img):
    """Calculate Tmean image from Tmin and Tmax for GRIDMET collection"""
    ##return img.expression("0.5 * (b('tmmx') + b('tmmx'))")\
    ##    .select([0],['tmean']).copyProperties(img, property_list)
    tmax_img = img.select('tmmx')
    tmin_img = img.select('tmmn')
    return tmax_img.add(tmin_img).multiply(0.5).select([0],['tmean'])\
        .copyProperties(img, property_list)
