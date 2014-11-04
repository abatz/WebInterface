#############################################
##       FORMS                             ##
#############################################
#============================
#   formBasicVariable 
#============================
formBasicVariable=[
        ('','--select variable--'),
        ('eto','ETo (Potential Evapotranspiration)'),
        ('eddi','EDDI (Evap. Demand Drought Index)'),
        ('NDVI','NDVI (Norm. Diff. Veg. Index)'),
        ('bi','BI (Burning Index)'),
        ('evi','EVI (Enhanced Veg. Index)'),
        ('ndsi','NDSI (Snow Index)'),
        ('nbrt','NBRT (Norm. Burn Rat. Thm. Ind)'),
        ('bai','BAI (Burning Area Index)'),
        ('ndwi','NDWI (Water Index)'),
        ]
#============================
#   formProduct 
#============================
formProduct=[
        ('','--select source--'),
        ('gridded','gridMET gridded observations'),
        ('landsat','Landsat remote sensing'),
        ('modis','MODIS remote sensing'),
        ]

#============================
#    formLocation
#============================
formLocation=[
        ('','--select domain--'),
        ('points','Points'),
        ('states','States'),
        ('counties','Counties'),
        ('hucs','Hydrologic Units'),
        ('divs','Climate Divisions'),
        ('psas','Predictive Service Areas'),
        ('ushcns','USHCN Station'),
        ]


#============================
#    formVariableGrid
#============================
formVariableGrid=[
        ('','--select variable--'),
        ('','--select variable--'),
        ('pdsi','PDSI (Palm. Drought Sev. Ind.)'),
        ('spi','SPI (Stand. Prec. Ind.)'),
        ('spei','SPEI (Stand. Prec-Evap. Ind.)'),
        ('eto','ETo (Potential EvapTrans.)'),
        ('eddi','EDDI (Evap Dem. Drought Ind.)'),
        ('erc','ERC (Energy Release Component)'),
        ('bi','BI (Burning Index)'),
        ('tmmn','TMAX (Min Temperature)'),
        ('tmmx','TMAX (Max Temperature)'),
        ('rmax','RMIN (Min Rel. Humidity)'),
        ('rmin','RMAX (Max Rel. Humidity)'),
        ('pr','PPT (Precipitation)'),
        ('srad','SRAD (Downward Radiation)'),
        ('vs','VS (Wind Speed)'),
        ('th','TH (Wind Direction)'),
        ]

#============================
#    formVariableLandsat
#============================
formVariableLandsat=[
        ('','--select variable--'),
        ('eto','ETo (Potential Evapotranspiration)'),
        ('eddi','EDDI (Evap. Demand Drought Index)'),
        ('NDVI','NDVI (Norm. Diff. Veg. Index)'),
        ('bi','BI (Burning Index)'),
        ('evi','EVI (Enhanced Veg. Index)'),
        ('ndsi','NDSI (Snow Index)'),
        ('nbrt','NBRT (Norm. Burn Rat. Thm. Ind)'),
        ('bai','BAI (Burning Area Index)'),
        ('ndwi','NDWI (Water Index)'),
        ]
#============================
#    formVariableModis
#============================
formVariableModis=[
        ('','--select variable--'),
        ('eto','ETo (Potential Evapotranspiration)'),
        ('eddi','EDDI (Evap. Demand Drought Index)'),
        ('NDVI','NDVI (Norm. Diff. Veg. Index)'),
        ('bi','BI (Burning Index)'),
        ('evi','EVI (Enhanced Veg. Index)'),
        ('ndsi','NDSI (Snow Index)'),
        ('nbrt','NBRT (Norm. Burn Rat. Thm. Ind)'),
        ('bai','BAI (Burning Area Index)'),
        ('ndwi','NDWI (Water Index)'),
        ]

#============================
#    DayTimeChoiceForm
#============================
formDayTimeChoice=[
        ('','--make a choice--'),
        ('timespan','Time Span'),
        ('daysonly','Selected Days Only'),
     ]

#============================
#    MonthTimeChoiceForm
#============================
formMonthTimeChoice=[
        ('','--make a choice--'),
        ('timespan','Time Span'),
        ('monthsonly','Selected Months Only'),
     ]


#============================
#    GridTimeSpanForm
#============================
formGridTimeSpan=[
        ('','--select frequency--'),
        ('dailyCal','Daily'),
        ('monthlyCal','Monthly'),
        ('yearlyCal','Annual'),
     ]

#============================
#    LandsatTimeSpanForm
#============================
formLandsatTimeSpan=[
        ('','--select frequency--'),
        ('dailyCal','Daily'),
        ('monthlyCal','Monthly'),
        ('yearlyCal','Yearly'),
     ]

#============================
#    ModisTimeSpanForm
#============================
formModisTimeSpan=[
        ('','--select frequency--'),
        ('dailyCal','Daily'),
        ('monthlyCal','Monthly'),
        ('yearlyCal','Yearly'),
     ]


#============================
# MonthChoiceForm
#===========================
formMonthTimeChoice=[
        ('','--make a choice--'),
        ('allmonths','All Months'),
        ('1','1-Month'),
        ('2','2-Months'),
        ('3','3-Months'),
        ('4','4-Months'),
        ('5','5-Months'),
        ('6','6-Months'),
        ('7','7-Months'),
        ('8','8-Months'),
        ('9','9-Months'),
        ('10','10-Months'),
        ('11','11-Months'),
        ]


#============================
# DayChoiceForm
#===========================
formDayTimeChoice=[
        ('','--make a choice--'),
        ('1','1-day avg'),
        ('3','3-day avg'),
        ('5','5-day avg'),
        ('7','7-day avg'),
        ('10','10-day avg'),
        ('14','14-day avg'),
        ('21','21-day avg'),
        ]


#============================
#   formMonthStart/formMonthEnd
#===========================

formMonthStart=[
        ('jan','January'),
        ('feb','February'),
        ('mar','March'),
        ('apr','April'),
        ('may','May'),
        ('june','June'),
        ('july','July'),
        ('aug','August'),
        ('sept','September'),
        ('oct','October'),
        ('nov','November'),
        ('dec','December'),
        ]
formMonthEnd=[
        ('jan','January'),
        ('feb','February'),
        ('mar','March'),
        ('apr','April'),
        ('may','May'),
        ('june','June'),
        ('july','July'),
        ('aug','August'),
        ('sept','September'),
        ('oct','October'),
        ('nov','November'),
        ('dec','December'),
        ]

#============================
#   formDayStart/formDayEnd, formYearStart/formYearEnd
#===========================
formDayStart=((str(x),x) for x in range(1,31+1))
formDayEnd=((str(x),x) for x in range(1,31+1))
formYearStart=((str(x),x) for x in range(1979,2014+1))
formYearEnd=((str(x),x) for x in range(1979,2014+1))



#============================
#   formDisplay 
#===========================
formDisplay=[
        ('','--select display type--'),
        ('timeseries','Time Series'),
        ('overlay','Map Overlay'),
        ]

#============================
#    formMetric
#===========================
formMetric=[
        ('','--select metric--'),
        ('raw','Raw Values'),
        ('anom','Difference from Climatology'),
        ('clim','Climatology'),
        ]

#============================
#    formStatistic
#===========================
formStatistic=[
        ('','--select statistic--'),
        ('mean','Average Value over Time Period'),
        ('max','Maximum over Time Period'),
        ('min','Minimum over Time Period'),
        ('stdev','Standard Deviation of Values'),
        ]