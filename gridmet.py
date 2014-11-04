def get_ppt_anomaly(start_dt, end_dt):
    """Calculate PPT anomalies for a given time period.
    The climatology is currently calculated for 2006 - 2010
    Args:
        start_dt: Starting datetime object (inclusive)
        end_dt: Ending datetime object (inclusive)
    Returns:
        An EarthEngine mapid object
    """

    ## Create a filter object that selects data based on the day-of-year
    doy_filter = ee.Filter(ee.Filter.calendarRange(
        int(start_dt.strftime('%j')), int(end_dt.strftime('%j')), 'day_of_year'))

    ## Shortened GRIDMET collecction for calculating anomaly
    gridmet_test_coll = ee.ImageCollection(
        'IDAHO_EPSCOR/GRIDMET').filterDate(start_dt, end_dt)
        ##'IDAHO_EPSCOR/GRIDMET').filterDate("2013", "2014").filter(doy_filter)

    ## Full GRIDMET collection for calculating climatology
    gridmet_full_coll = ee.ImageCollection(
        'IDAHO_EPSCOR/GRIDMET').filterDate("2006", "2010").filter(doy_filter)

    def gridmet_ppt_func(gridmet_image):
        doy = ee.Number(ee.Algorithms.Date(gridmet_image.get("system:time_start")).getRelative('day', 'year')).add(1).double()
        return gridmet_image.select(['pr'], ['PPT']).set({
            'DOY':doy, 'system:index':gridmet_image.get('system:index'),
            'system:time_start':gridmet_image.get('system:time_start'),
            'system:time_end':gridmet_image.get('system:time_end')})
    ## Calculate PPT for the full GRIDMET climatology period and the anomaly period separately
    ppt_full_coll = gridmet_full_coll.map(gridmet_ppt_func)
    ppt_test_coll = gridmet_test_coll.map(gridmet_ppt_func)

    ## For each PPT image in the anomaly time period (ppt_test_coll),
    ##   get a list of PPT images from the full time period (ppt_full_coll) for the same DOY
    ## Link these two collections by DOY using the join method (which was calculated and set in the PPT function)
    ##doy_match_filter = ee.Filter.equals(leftField='DOY', rightField='DOY')
    doy_match_filter = ee.Filter.equals('DOY', None, 'DOY', None)
    ppt_join_coll = ee.ImageCollection(
        ee.Join.saveAll('doy_match').apply(
            ppt_test_coll, ppt_full_coll, doy_match_filter))

    # Calculate the mean PPT (i.e. climatology) for each DOY in the anomaly period
    #   (PPT images were saved to the doy_match property in the join collection)
    def mean_func(ppt_image):
        return ee.Image(ee.ImageCollection.fromImages(
            ppt_image.get('doy_match')).mean())
    mean_coll = ppt_join_coll.map(mean_func)

    ## Calculate the PPT anomaly (i.e. PPT - PPT_mean) for each DOY in the anomaly period
    ## This seems very redundant.  Is there a way to do an image wise subtraction between two collections
    ##   in order to avoid calculating the mean for the collection twice?
    def anomaly_func(ppt_image):
        return ppt_image.subtract(
            ee.Image(ee.ImageCollection.fromImages(ppt_image.get('doy_match')).mean()))
    anomaly_coll = ee.ImageCollection(ppt_join_coll.map(anomaly_func))

    ## Sum of the PPT anomalies divided by the sum of the mean PPT (i.e. sum of the daily climatology)
    ##   for all images in the anomaly time period
    index_image = ee.Image(anomaly_coll.sum()).divide(ee.Image(mean_coll.sum()))

    return index_image
