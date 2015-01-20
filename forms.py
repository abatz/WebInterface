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
    #('spi','SPI (Stand. Prec. Ind.)'),
    #('spei','SPEI (Stand. Prec-Evap. Ind.)'),
    #('eto','ETo (Potential EvapTrans.)'),
    #('eddi','EDDI (Evap Dem. Drought Ind.)'),
    #('th','TH (Wind Direction)'),
    ('erc','ERC (Energy Release Component)'),
    ('pdsi','PDSI (Palm. Drought Sev. Ind.)'),
    ('pet','PET (Potential Evapotranspiration)'),
    ('pr','PPT (Precipitation)'),
    ('rmin','RMIN (Min Rel. Humidity)'),
    ('rmax','RMAX (Max Rel. Humidity)'),
    ('sph','SPH (Specific Humidity)'),
    ('srad','SRAD (Downward Radiation)'),
    ('tmmn','TMIN (Min Temperature)'),
    ('tmmx','TMAX (Max Temperature)'),
    ('vs','VS (Wind Speed)'),
    ('wb','Water Balance (PPT-PET)'),
]

#============================
#    formVariableLandsat
#============================
formVariableLandsat=[
    #('eto','ETo (Potential Evapotranspiration)'),
    #('eddi','EDDI (Evap. Demand Drought Index)'),
    #('bi','BI (Burning Index)'),
    #('NBRT','NBRT (Norm. Burn Rat. Thm. Ind)'),
    #('BAI','BAI (Burning Area Index)'),
    ('LEVI','EVI (Enhanced Vegetation Index)'),
    ('NDSI','NDSI (Snow Index)'),
    ('NDVI','NDVI (Vegetation Index)'),
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
#    formTimeSeriesCalc
#============================
formTimeSeriesCalc=[
    ('season','Time Series of Seasonal '),
    ('days','Time Series of Daily '),
]


#============================
#    formBackground
#============================
formBackground=[
    ('whitebackground','White Background'),
]



#============================
#    formMonth
#============================
formMonth=[
    ('1','Jan '),
    ('2','Feb '),
    ('3','Mar '),
    ('4','Apr '),
    ('5','May '),
    ('6','Jun '),
    ('7','Jul '),
    ('8','Aug '),
    ('9','Sept '),
    ('10','Oct '),
    ('11','Nov '),
    ('12','Dec '),
]

#============================
#    formDay
#============================
formDay=[(str(x),str(x)) for x in range(1,32,1)]

#============================
#    formYear
#============================
formYear=[(str(x),str(x)) for x in range(1979,2015,1)]

#============================
#    formLocation
#============================
formLocation=[
    ('full','Full Domain'),
    #('conus','CONUS'),
    ('rectangle','Rectangle'),
    ('states','States'),
    ('points','Points'),
]

#============================
#    formOpacity
#============================
formOpacity=[(str(x*0.05),str((1.0-x*0.05)*100)+'%') for x in range(20,-1,-1)]


#============================
#    formUnits
#============================
formUnits=[
    ('metric','Metric (ie. C,mm,m/s,W/m2)'),
    ('english','English (ie. F,in,mi/hr)'),
]

#============================
#    formPaletteMap
#============================
formPaletteSeqMap=[
    ('Greens','Greens'),
    ('Blues','Blues'),
    ('invBlues','invBlues'),
    ('Oranges','Oranges'),
    ('Reds','Reds'),
    ('YlGn','Yellow-Green'),
    ('GnBu','Green-Blue'),
    ('BuGn','Blue-Green'),
    ('PuBuGn','Purple-Blue-Green'),
    ('PuBu','Purple-Blue'),
    ('BuPu','Blue-Purple'),
    ('RdPu','Red-Purple'),
    ('PuRd','Purple-Red'),
    ('OrRd','Orange-Red'),
    ('YlOrRd','Yellow-Orange-Red'),
    ('YlOrBr','Yellow-Orange-Brown'),
    ('YlGnBu','Yellow-Green-Blue'),
    ('PuBuGn','Purple-Blue-Green'),
    ('Purples','Purples'),
    ('Greys','Greys'),
]

formPaletteDivMap=[
    ('RdBu','Red-Blue'),
    ('BuRd','Blue-Red'),
    ('RdYlBu','Red-Yellow-Blue'),
    ('BuYlRd','Blue-Yellow-Red'),
    ('RdYlGn','Red-Yellow-Green'),
    ('PuOr','Purple-Orange'),
    ('BrBG','Brown-BG'),
    ('PRGn','PR-Green'),
    ('PiYG','Pi-YG'),
    ('RdGy','Red-Grey'),
    ('Spectral','Spectral'),
]

#============================
#    formPaletteSize
#============================
formPaletteSize=[(str(x),str(x)) for x in range(3,10,1)]
#============================
#    formMapZoom
#============================
formMapZoom=[(str(x),str(x)) for x in range(2,13,1)]


#============================
#   formDayStart/formDayEnd, formYearStart/formYearEnd
#===========================
formDayStart=((str(x),x) for x in range(1,31+1))
formDayEnd=((str(x),x) for x in range(1,31+1))
formYearStart=((str(x),x) for x in range(1979,2014+1))
formYearEnd=((str(x),x) for x in range(1979,2014+1))


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

stateLong = {
    'Alaska':-152.2683,
    'Alabama':-86.8073,
    'Arizona':-92.3809,
    'Arkansas':-170.7197,
    'Arizona':-111.3877,
    'California':-119.7462,
    'Colorado':-105.3272,
    'Conneticut':-72.7622,
    'District of Columbia':-77.0262,
    'Delaware':-75.5148,
    'Florida':-81.7170,
    'Georgia':-83.6487,
    'Hawaii':-157.5311,
    'Iowa':-93.2140,
    'Idaho':-114.5103,
    'Illinois':-89.0022,
    'Indiana':-86.2604,
    'Kansas':-96.8005,
    'Kentucky':-84.6514,
    'Louisiana':-91.8749,
    'Massachusetts':-71.5314,
    'Maryland':-76.7902,
    'Maine':-69.3977,
    'Michigan':-84.5603,
    'Minnesota':-93.9196,
    'Missouri':-92.3020,
    'Mississippi':-89.6812,
    'Montana':-110.3261,
    'North Carolina':-79.8431,
    'North Dakota':-99.7930,
    'Nebraska':-98.2883,
    'New Hampshire':-71.5653,
    'New Jersey':-74.5089,
    'New Mexico':-106.2371,
    'Nevada':-117.1219,
    'New York':-74.9384,
    'Ohio':-82.7755,
    'Oklahoma':-96.9247,
    'Oregon':-122.1269,
    'Pennsylvania':-77.2640,
    'Rhode Island':-71.5101,
    'South Carolina':-80.9066,
    'South Dakota':-99.4632,
    'Tennessee':-86.7489,
    'Texas':-97.6475,
    'Utah':-111.8535,
    'Virginia':-78.2057,
    'Vermont':-72.7093,
    'Washington':-121.5708,
    'Wisconsin':-89.6385,
    'West Virginia':-80.9696,
    'Wyoming':-107.2085
}

stateLat = {
    'Alaska':61.3850,
    'Alabama':32.7990,
    'Arizona':34.9513,
    'Arkansas':14.2417,
    'Arizona':33.7712,
    'California':36.1700,
    'Colorado':39.0646,
    'Conneticut':41.5834,
    'District of Columbia':38.8964,
    'Delaware':39.3498,
    'Florida':27.8333,
    'Georgia':32.9866,
    'Hawaii':21.1098,
    'Iowa':42.0046,
    'Idaho':44.2394,
    'Illinois':40.3363,
    'Indiana':39.8647,
    'Kansas':38.5111,
    'Kentucky':37.6690,
    'Louisiana':31.1801,
    'Massachusetts':42.2373,
    'Maryland':39.0724,
    'Maine':44.6074,
    'Michigan':43.3504,
    'Minnesota':45.7326,
    'Missouri':38.4623,
    'Mississippi':32.7673,
    'Montana':46.9048,
    'North Carolina':35.6411,
    'North Dakota':47.5362,
    'Nebraska':41.1289,
    'New Hampshire':43.4108,
    'New Jersey':40.3140,
    'New Mexico':34.8375,
    'Nevada':38.4199,
    'New York':42.1497,
    'Ohio':40.3736,
    'Oklahoma':35.5376,
    'Oregon':44.5672,
    'Pennsylvania':40.5773,
    'Rhode Island':41.6772,
    'South Carolina':33.8191,
    'South Dakota':44.2853,
    'Tennessee':35.7449,
    'Texas':31.1060,
    'Utah':40.1135,
    'Virginia':37.7680,
    'Vermont':44.0407,
    'Washington':47.3917,
    'Wisconsin':44.2563,
    'West Virginia':38.4680,
    'Wyoming':42.7475
}

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

def check_variable(variable):
    err = None
    vrs = formVariableGrid + formVariableLandsat
    options = [v[0] for v in vrs]
    if variable not in options:
        return 'Variable should be one of: %s. You entered: %s' %(','.join(options),str(variable))
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

#def check_units(units):

