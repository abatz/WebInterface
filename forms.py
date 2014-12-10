#Modules needed for form check
import datetime as dt
import numpy as np
#############################################
##       CURRENT FORMS BEING USED          ##
#############################################
#============================
#    formVariableGrid
#============================
formVariableGrid=[
    #('pdsi','PDSI (Palm. Drought Sev. Ind.)'),
    #('spi','SPI (Stand. Prec. Ind.)'),
    #('spei','SPEI (Stand. Prec-Evap. Ind.)'),
    #('eto','ETo (Potential EvapTrans.)'),
    #('eddi','EDDI (Evap Dem. Drought Ind.)'),
    ('erc','ERC (Energy Release Component)'),
    #('bi','BI (Burning Index)'),
    ('tmmn','TMIN (Min Temperature)'),
    ('tmmx','TMAX (Max Temperature)'),
    ('rmin','RMIN (Min Rel. Humidity)'),
    ('rmax','RMAX (Max Rel. Humidity)'),
    ('pr','PPT (Precipitation)'),
    ('pet','PET (Potential Evapotranspiration)'),
    ('wb','Water Balance (PPT-PT)'),
    #('dpr','Change in PPT (Precipitation)'),
    ('srad','SRAD (Downward Radiation)'),
    ('vs','VS (Wind Speed)'),
    #('th','TH (Wind Direction)'),
    ('sph','SPH (Specific Humidity)'),
]

#============================
#    formVariableLandsat
#============================
formVariableLandsat=[
    #('eto','ETo (Potential Evapotranspiration)'),
    #('eddi','EDDI (Evap. Demand Drought Index)'),
    ('NDVI','NDVI (Vegetation Index)'),
    #('bi','BI (Burning Index)'),
    ('EVI','EVI (Enhanced Vegetation Index)'),
    ('NDSI','NDSI (Snow Index)'),
    #('NBRT','NBRT (Norm. Burn Rat. Thm. Ind)'),
    #('BAI','BAI (Burning Area Index)'),
    ('NDWI','NDWI (Water Index)'),
]
#============================
#    formAnomOrValue
#============================
formAnomOrValue=[
    ('value','Values'),
    ('clim','Climatology'),
    ('anom','Anomaly'),
]

#============================
#    formLocation
#============================
formLocation=[
    ('full','Full Domain'),
    ('conus','CONUS'),
    ('rectangle','Rectangle'),
    ('states','States'),
    ('points','Points'),
]

#============================
#    formOpacity
#============================
formOpacity=[(str(x*0.05),str(1.0-x*0.05)) for x in range(20,-1,-1)]

#============================
#    formStates
#============================
formStates=[
    ('Alabama','Alabama'),
    ('Arizona','Arizona'),
    ('Arkansas','Arkansas'),
    ('California','California'),
    ('Colorado','Colorado'),
    ('Connecticut','Connecticut'),
    ('Delaware','Delaware'),
    ('District of Columbia','District of Columbia'),
    ('Florida','Florida'),
    ('Georgia','Georgia'),
    ('Idaho','Idaho'),
    ('Illinois','Illinois'),
    ('Indiana','Indiana'),
    ('Iowa','Iowa'),
    ('Kansas','Kansas'),
    ('Kentucky','Kentucky'),
    ('Louisiana','Louisiana'),
    ('Maine','Maine'),
    ('Maryland','Maryland'),
    ('Massachusetts','Massachusetts'),
    ('Michigan','Michigan'),
    ('Minnesota','Minnesota'),
    ('Mississippi','Mississippi'),
    ('Missouri','Missouri'),
    ('Montana','Montana'),
    ('Nebraska','Nebraska'),
    ('Nevada','Nevada'),
    ('New Hampshire','New Hampshire'),
    ('New Jersey','New Jersey'),
    ('New Mexico','New Mexico'),
    ('New York','New York'),
    ('North Carolina','North Carolina'),
    ('North Dakota','North Dakota'),
    ('Ohio','Ohio'),
    ('Oklahoma','Oklahoma'),
    ('Oregon','Oregon'),
    ('Pennsylvania','Pennsylvania'),
    ('Rhode Island','Rhode Island'),
    ('South Carolina','South Carolina'),
    ('South Dakota','South Dakota'),
    ('Tennessee','Tennessee'),
    ('Texax','Texas'),
    ('Utah','Utah'),
    ('Vermont','Vermont'),
    ('Virginia','Virginia'),
    ('Washington','Washington'),
    ('West Virginia','West Virginia'),
    ('Wisconsin','Wisconsin'),
    ('Wyoming','Wyoming'),
]

state_abbreviations = [
    ('AK', 'Alaska'),
    ('AL', 'Alabama'),
    ('AZ', 'Arizona'),
    ('AR', 'Arkansas'),
    ('CA', 'California'),
    ('CO', 'Colorado'),
    ('CT', 'Connecticut'),
    ('DE', 'Delaware'),
    ('FL', 'Florida'),
    ('GA', 'Georgia'),
    ('HI', 'Hawaii'),
    ('ID', 'Idaho'),
    ('IL', 'Illinois'),
    ('IN', 'Indiana'),
    ('IA', 'Iowa'),
    ('KS', 'Kansas'),
    ('KY', 'Kentucky'),
    ('LA', 'Louisiana'),
    ('ME', 'Maine'),
    ('MD', 'Maryland'),
    ('MA', 'Massachusetts'),
    ('MI', 'Michigan'),
    ('MN', 'Minnesota'),
    ('MS', 'Mississippi'),
    ('MO', 'Missouri'),
    ('MT', 'Montana'),
    ('NE', 'Nebraska'),
    ('NV', 'Nevada'),
    ('NH', 'New Hampshire'),
    ('NJ', 'New Jersey'),
    ('NM', 'New Mexico'),
    ('NY', 'New York'),
    ('NC', 'North Carolina'),
    ('ND', 'North Dakota'),
    ('OH', 'Ohio'),
    ('OK', 'Oklahoma'),
    ('OR', 'Oregon'),
    ('PA', 'Pennsylvania'),
    ('RI', 'Rhode Island'),
    ('SC', 'South Carolina'),
    ('SD', 'South Dakota'),
    ('TN', 'Tennessee'),
    ('TX', 'Texas'),
    ('UT', 'Utah'),
    ('VT', 'Vermont'),
    ('VA', 'Virginia'),
    ('WA', 'Washington'),
    ('DC', 'Washington D.C.'),
    ('WV', 'West Virginia'),
    ('WI', 'Wisconsin'),
    ('WY', 'Wyoming')
]


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

def format_mapzoom(mapzoom):
    try:
        int(mapzoom)
    except:
        return mapzoom
    return int(mapzoom)

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

def check_basicvariable(basicvariable):
    err = None
    vrs = formVariableGrid + formVariableLandsat
    options = [v[0] for v in vrs]
    if basicvariable not in options:
        return 'Variable should be one of: %s. You entered: %s' %(','.join(options),str(basicvariable))
        pass
    return err

def check_anomOrValue(anomOrValue):
    err = None
    options = [o[0] for o in formAnomOrValue]
    if anomOrValue not in options:
        return 'Calculation should be one of: %s. You entered: %s' %(','.join(options), str(anomOrValue))
    return err

def check_domainType(domainType):
    options = [l[0] for l in formLocation]
    if domainType not in options:
        return 'Domain should be one of: %s. You entered: %s' %(','.join(options), str(domainType))

def check_pointsLongLat(pointsLongLat):
    err = None
    pLL = pointsLongLat
    #make sure its a comma separated list of Long/Lat coordinates
    try:
        pLL_list = pLL.split(',')
    except:
        return 'Points must be neterd as a comma separated list of Long,Lat pairs! You entered: %' %str(pointsLongLat)
    try:
        Lons = np.array([float(pLL_list[i]) for i in range(0,len(pLL_list),2)])
        Lats = np.array([float(pLL_list[i]) for i in range(1,len(pLL_list),2)])
    except:
        return 'Points needs to be comma separated list of one or more Long,Lat pairs. You entered: %s' %str(pLL)
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

