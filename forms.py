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

stateLong ={
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


