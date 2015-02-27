#Modules needed for form checking
import datetime as dt
import numpy as np

#============================
#   formDayStart/formDayEnd, formYearStart/formYearEnd
#===========================
formDayStart=((str(x),x) for x in range(1,31+1))
formDayEnd=((str(x),x) for x in range(1,31+1))
formYearStart=((str(x),x) for x in range(1979,2014+1))
formYearEnd=((str(x),x) for x in range(1979,2014+1))

#============================
#   formatting of
#   template variables
#===========================
def format_state(state):
    for st in state_abbreviations:
        if state.upper() == st[0] or state == st[1]:
            return st[1]
    return state

#def format_mapzoom(mapzoom):
#    try:
#        int(mapzoom)
#    except:
#        return mapzoom
#    return int(mapzoom)

def format_dateStart(dateStart):
    #Put date into format yyyy-mm-dd
    dS = dateStart
    try:
        #convert to yyymmdd
        dS = dateStart.replace('/','').replace('-','').replace(':','') #any ther formats we want to support?
        if len(dS) != 8:
            return dS
        dS = dS[0:4] + '-' + dS[4:6] + '-' + dS[6:8]
    except:
        return dS
    return dS

def format_dateEnd(dateEnd):
    #Put date into format yyyy-mm-dd
    dE = dateEnd
    try:
        #convert to yyymmdd
        dE = dateEnd.replace('/','').replace('-','').replace(':','') #any ther formats we want to support?
        if len(dE) != 8:
            return dE
        dE = dE[0:4] + '-' + dE[4:6] + '-' + dE[6:8]
    except:
        return dE
    return dE

def format_point(point):
    p = str(point)
    #Strip white spaces
    p = p.replace(', ', ',')
    #Strip extra comma
    p = p.rstrip(',')
    return p

def format_pointsLongLat(pointsLongLat):
    pLL = pointsLongLat
    #if list, turn into string
    if isinstance(pLL, list):
        pLL = (',').join(pLL)
    #remove any extra spaces
    pLL = pLL.replace(', ', ',')
    #make sure its a comma separated list of Long/Lat coordinates
    pLL_list = pLL.split(',')
    try:
        Lons = np.array([float(pLL_list[i]) for i in range(0,len(pLL_list),2)])
        Lats = np.array([float(pLL_list[i]) for i in range(1,len(pLL_list) - 1,2)])
    except:
        return pLL
    if len(Lats) != len(Lons):
        return pLL
    if len(np.where(Lons >= 0)) == len(Lons) and len(np.where(Lons <= 0)) == len(Lons):
        #Lats/Lons mxied up
        Lons_temp = list(Lats)
        Lats = list(Lons)
        Lons = Lons_tem
        pLL = ''
        for idx in range(len(Lats)):
            pLL+= Lons[idx] + ',' + Lats[idx]
    return pLL

def format_NELat(NELat):
    nel = NELat
    try:
        float(nel)
    except:
        return nel
    return float(nel)

def format_NELong(NELong):
    nel = NELong
    try:
        float(nel)
    except:
        return nel
    return float(nel)

def format_SWLat(SWLat):
    swl = SWLat
    try:
        float(swl)
    except:
        return swl
    return float(swl)

def format_SWLong(SWLong):
    swl = SWLong
    try:
        float(swl)
    except:
        return swl
    return float(swl)


#============================
#   form field checks
#   mainly for the case that a
#   user entered a url parameter string
#   return err = None if no error encountered
#   else return error message
#===========================
#def check_Feb12014(dateStart,dateEnd,product):
#    err = None
#    if(product == 'G'):
#        dS = dt.datetime.strptime(dateStart,'%Y-%m-%d');
#        dE = dt.datetime.strptime(dateEnd,'%Y-%m-%d');
#        dDate = dt.datetime.strptime('2015-02-01','%Y-%m-%d');
#        if(dDate>=dS and dDate<=dE):
#              return 'Please select date range that does not include Feb 1,2015 for GridMet data as there is error on this date.'
#    return err

def check_dateMoreThanYear(dateStart,dateEnd,calculation,domainType):
    err = None
    dS = dt.datetime.strptime(dateStart,'%Y-%m-%d');
    dE = dt.datetime.strptime(dateEnd,'%Y-%m-%d');
    if calculation !='value' and domainType!='points':
        if  (dE-dS).total_seconds()>=365 * 24 * 3600:
            return 'Calculations requiring climatologies over day ranges > 365 days are not currently available.'
    if  (dE-dS).total_seconds()< 1 * 24 * 3600:
            return 'Note: you selected only 1 day of data.'
    return err

def check_climatologyyears(yearStartClim,yearEndClim,domainType):
    err = None
    if domainType!='points' and int(yearStartClim)>int(yearEndClim):
        return 'Start year needs to be less than End year.'
    return err

def check_state(state):
    err = None
    options = [s[0] for s in formStates]
    if state not in options:
        return '%s is not a valid US state.' %state
def check_mapzoom(mapzoom):
    err = None
    try:
        int(mapzoom)
    except:
        return mapzoom
    return err

def check_dateStart(dateStart):
    #Check that date is of format yyyy-mm-dd
    err = None
    try:
        dt.datetime.strptime(dateStart, "%Y-%m-%d")
    except:
        return 'Wrong date format or invalid Start Date: %s'%str(dateStart)
    return err

def check_dateEnd(dateEnd):
    #Check that date is of format yyyy-mm-dd
    err = None
    try:
        dt.datetime.strptime(dateEnd, "%Y-%m-%d")
    except:
        return 'Wrong date format or invalid End Date: %s'%str(dateEnd)
    return err

def check_variable(variable):
    err = None
    vrs = formVariableGrid + formVariableLandsat+formVariableModis
    options = [v[0] for v in vrs]
    if variable not in options:
        return 'Variable should be one of: %s. You entered: %s' %(','.join(options),str(variable))
        pass
    return err

def check_calculation(calculation):
    err = None
    options = [o[0] for o in formCalculation]
    if calculation not in options:
        return 'Calculation should be one of: %s. You entered: %s' %(','.join(options), str(calculation))
    return err

def check_domainType(domainType):
    options = [l[0] for l in formLocation]
    if domainType not in options:
        return 'Domain should be one of: %s. You entered: %s' %(','.join(options), str(domainType))
def check_point(point):
    err = None
    #Make sure point is lon, lat string
    p = str(point)
    p_list = p.split(',')
    if len(p_list) <= 1:
        return 'Point must be entered as a Long,Lat pair. You entered: %s' %str(point)
    if len(p_list) > 2:
        return 'Please enter a single point as Long,Lat coordinate. You entered: %s' %str(point)
    return err


def check_pointsLongLat(pointsLongLat):
    err = None
    pLL = pointsLongLat
    if not pLL:
        return err
    #make sure its a comma separated list of Long/Lat coordinates
    try:
        pLL_list = pLL.split(',')
    except:
        return 'Error in point selection. Check for extra commas, etc. Each point should be entered as Long,Lat pair.'
    try:
        Lons = np.array([float(pLL_list[i]) for i in range(0,len(pLL_list),2)])
        Lats = np.array([float(pLL_list[i]) for i in range(1,len(pLL_list),2)])
    except:
        return 'Error in point selection. Check for extra commas, etc. Each point should be entered as Long,Lat pair.'
    if len(Lats) != len(Lons):
        return 'Number of Latitudes not equal number of latitudes'
    return err

def check_NELat(NELat):
    err = None
    try:
        float(NELat)
    except:
        return 'Rectangle coordinates should be floats. You entered: %s' %str(NELat)
    if float(NELat) < 0:
        return 'NE corner latitude must be positive. You entered: %s' %str(NELat)
    return err

def check_NELong(NELong):
    err = None
    try:
        float(NELong)
    except:
        return 'Rectangle coordinates should be floats. You entered: %s' %str(NELong)
    if float(NELong) > 0:
        return 'NE corner longitude must be negative. You entered: %s' %str(NELong)
    return err

def check_SWLat(SWLat):
    err = None
    try:
        float(SWLat)
    except:
        return 'Rectangle coordinates should be floats. You entered: %s' %str(SWLat)
    if float(SWLat) < 0:
        return 'SW corner latitude must be positive. You entered: %s' %str(SWLat)
    return err

def check_SWLong(SWLong):
    err = None
    try:
        float(SWLong)
    except:
        return 'Rectangle coordinates should be floats. You entered: %s' %str(SWLong)
    if float(SWLong) > 0:
        return 'SW corner longitude must be negative. You entered: %s' %str(SWLong)
    return err

def check_opacity(opacity):
    op = formOpacity
    options = []
    for tple  in  op:
        options.append(str(tple[0]))
    if str(opacity) not in options:
        return 'Opacity should be one of: %s. You entered: %s' %(','.join(options), str(opacity))

#def check_units(units):

