#############################################
##       CURRENT FORMS BEING USED IN HTML  ##
#############################################
#============================
#    formVariableGrid
#============================
formVariableGrid=[
    ('Gerc','ERC (Energy Release Component)'),
    ('Gpdsi','PDSI (Palm. Drought Sev. Ind.)'),
    ('Gpet','PET (Reference Evapotranspiration)'),
    ('Gpr','PPT (Precipitation)'),
    ('Grmin','RMIN (Min Rel. Humidity)'),
    ('Grmax','RMAX (Max Rel. Humidity)'),
    ('Gsph','SPH (Specific Humidity)'),
    ('Gsrad','SRAD (Downward Radiation)'),
    ('Gtmean','TMEAN (Mean Temperature)'),
    ('Gtmmn','TMIN (Min Temperature)'),
    ('Gtmmx','TMAX (Max Temperature)'),
    ('Gvs','VS (Wind Speed)'),
    ('Gwb','Water Balance (PPT-PET)'),
]

#============================
#    formVariableLandsat
#============================
formVariableLandsat=[
    ('5EVI','Landsat 5 EVI (Enhanced Vegetation Index)'),
    ('5NDSI','Landsat 5 NDSI (Snow Index)'),
    ('5NDVI','Landsat 5 NDVI (Vegetation Index)'),
    ('5NDWI','Landsat 5 NDWI (Water Index)'),
    ('8EVI','Landsat 8 EVI (Enhanced Vegetation Index)'),
    ('8NDSI','Landsat 8 NDSI (Snow Index)'),
    ('8NDVI','Landsat 8 NDVI (Vegetation Index)'),
    ('8NDWI','Landsat 8 NDWI (Water Index)'),
]
#============================
#    formVariableModis
#============================
formVariableModis=[
    ('MEVI','MODIS EVI (Enhanced Vegetation Index)'),
    ('MLST_Day_1km','MODIS LST (Land Surface Temperature in Day)'),
    ('MNDSI','MODIS NDSI (Snow Index)'),
    ('MNDVI','MODIS NDVI (Vegetation Index)'),
    ('MNDWI','MODIS NDWI (Water Index)'),
]

#============================
#    formCalculation
#============================
formCalculation=[
    ('value','Values'),
    ('clim','Climatology'),
    ('anom','Difference From Climatology'),
    ('anompercentchange','Percent Difference From Climatology'),
    ('anompercentof','Percent Of Climatology'),
]

#============================
#    formStatistic
#============================
formStatistic=[
    ('Mean','Mean'),
    ('Median','Median'),
    ('Max','Maximum'),
    ('Min','Minimum'),
    ('Total','Total'),
]
#============================
#    formChartType
#============================
formChartType=[
    ('scatter','Scatter Plot'),
    ('line','Line Plot'),
    ('spline','Spline Plot'),
    ('column','Bar Chart'),
    #('areaspline','Transparent Area Plot '), #not transparent for some reason?
    ('area','Stacked Area Plot '),
]
#============================
#============================
#    formLayers
#============================
formLayers=[
    ('none','None'),
    ('stateoverlayer','US States Layer'),
    ('countyoverlayer','US Counties Layer'),
    ('hucoverlayer','US Hydrologic Unit Code(HUC) Layer'),
    ('climatedivoverlayer','US Climate Divisions Layer'),
    ('psaoverlayer','US Predictive Service Areas Layer'),
    ('kmloverlayer','Custom KML/KMZ Layer (Enter URL)'),
]

#============================
#    formTimeSeriesCalc
#============================
formTimeSeriesCalc=[
    #('season','Time Series of Seasonal '),
    ('days','Time Series of Daily'),
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
formGridMetYear=[(str(x),str(x)) for x in range(1979,2025,1)]
formLandsat5Year=[(str(x),str(x)) for x in range(1984,2013,1)]
formLandsat8Year=[(str(x),str(x)) for x in range(2013,2025,1)]
formModisYear=[(str(x),str(x)) for x in range(2000,2025,1)]

#============================
#    formLocation
#============================
formLocation=[
    ('full','Full Domain'),
    #('conus','CONUS'),
    ('rectangle','Rectangle'),
    ('states','States'),
    ('points','Points'),
    ('singlemappoint','Single Map Point'),
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
    ('BrBG','Brown-Blue-Green'),
    ('GBBr','Green-Blue-Brown'),
    ('PRGn','PR-Green'),
    ('PiYG','Pi-YG'),
    ('RdGy','Red-Grey'),
    ('Spectral','Spectral'),
]
formPaletteCustomMap=[
    ('USDM','US Drought Monitor White-Yellow-Tan-Orange-Red'),
    ('invUSDM','US Drought Monitor Red-Orange-Tan-Yellow-White'),
]

#============================
#    formPaletteSize
#============================
formPaletteSize=[(str(x),str(x)) for x in range(3,10,1)]
#============================
#    formMapZoom
#============================
formMapZoom=[(str(x),str(x)) for x in range(1,20,1)]


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

