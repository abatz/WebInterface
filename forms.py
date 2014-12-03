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
	#('erc','ERC (Energy Release Component)'),
	#('bi','BI (Burning Index)'),
	('tmmn','TMIN (Min Temperature)'),
	('tmmx','TMAX (Max Temperature)'),
	('rmin','RMIN (Min Rel. Humidity)'),
	('rmax','RMAX (Max Rel. Humidity)'),
	('pr','PPT (Precipitation)'),
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
	('anom','Anomaly'),
	('clim','Climatology'),
]

#============================
#    formLocation
#============================
formLocation=[
	('full','Full Domain'),
	('conus','CONUS'),
	('states','States'),
	('points','Points'),
	# ('polygon','Polygon'),
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

#============================
#   formDayStart/formDayEnd, formYearStart/formYearEnd
#===========================
formDayStart=((str(x),x) for x in range(1,31+1))
formDayEnd=((str(x),x) for x in range(1,31+1))
formYearStart=((str(x),x) for x in range(1979,2014+1))
formYearEnd=((str(x),x) for x in range(1979,2014+1))
