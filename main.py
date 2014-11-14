#############################################
##       MAIN HANDLER FILE FOR VIEWS       ##
#############################################
import os
import cgi
import config
import ee
import jinja2
import webapp2
import datetime
import numpy
import json

from forms import *
import collectionMethods

template_dir = os.path.join(os.path.dirname(__file__),'templates')
JINJA_ENVIRONMENT= jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(template_dir))

#############################################
##       HOME PAGE                         ##
#############################################
class MainPage(webapp2.RequestHandler):
    def get(self):   
        template = JINJA_ENVIRONMENT.get_template('home.html')
        self.response.out.write(template.render({}))

#############################################
##       DROUGHT TOOL PAGE                 ##
#############################################
class DroughtTool(webapp2.RequestHandler):
    def get(self):                             # pylint: disable=g-bad-name
        ee.Initialize(config.EE_CREDENTIALS, config.EE_URL)
	ppost=0	
	mapzoom=4
	pointLat = 39.0510 
	pointLong = -98.0250
	polygon ='[[ [-109.05, 37.0], [-102.05, 37.0], [-102.05, 41.0], [-109.05, 41.0], [-111.05, 41.0], [-111.05, 42.0], [-114.05, 42.0], [-114.05, 37.0], [-109.05, 37.0]]]';
	state ='Washington'
	variable = 'NDVI'
	domainType = 'conus'
	dateStart ='2013-01-01' 
	dateEnd='2013-03-31'

        template_values = {
	    'pointLat': pointLat,
	    'pointLong': pointLong,
	    'ppost': ppost,
	    'mapzoom': mapzoom,
	    'formVariableGrid': formVariableGrid,
	    'formLocation': formLocation,
	    'formVariableLandsat': formVariableLandsat,
	    'formStates': formStates,
	    'variable': variable,
	    'state': state,
	    #'polygon': polygon,
	    'domainType': domainType,
	    'dateStart': dateStart,
	    'dateEnd': dateEnd,
	    #'timeSeriesGraphData': timeSeriesGraphData,
        }
        template = JINJA_ENVIRONMENT.get_template('droughttool.php')
        self.response.out.write(template.render(template_values))

    def post(self):
	ppost=1
        ee.Initialize(config.EE_CREDENTIALS, config.EE_URL)

	#Get data from form
        dateStart= cgi.escape(self.request.get('dateStart'))
        dateEnd = cgi.escape(self.request.get('dateEnd'))
        pointLatLong = cgi.escape(self.request.get('pointLatLong'))
        pointLatLongX = pointLatLong.split(",")
        pointLong = float(pointLatLongX[0])
        pointLat = float(pointLatLongX[1])
	variable =self.request.get('basicvariable')
	domainType =self.request.get('domainType')
	state=self.request.get('state')
	#polygon=self.request.get('polygon')
	#polygon ='[[ [-109.05, 37.0], [-102.05, 37.0], [-102.05, 41.0], [-109.05, 41.0], [-111.05, 41.0], [-111.05, 42.0], [-114.05, 42.0], [-114.05, 37.0], [-109.05, 37.0]]]';


	if(domainType=='points' or domainType=='conus'):
		subdomain = ee.Feature.Point(pointLong,pointLat);
		point = subdomain;
	elif(domainType=='states'):
		subdomain=state;
	elif(domainType=='polygon'):
		subdomain=ee.Feature.Polygon(polygon);

	if(variable=='NDVI' or variable=='NDSI'):
		product = 'landsat'
		productLongName = 'LANDSAT 7 L1T TOA'
		notes="NDVI calculated from Norm. Diff. of Infrared and Red bands"
		mapzoom=4 #was 4 
		minColorbar=-.1
		maxColorbar=.9
	elif(variable=='pr'): 
		product = 'gridded'
		productLongName = 'GRIDMET 4-km (Abatzoglou)'
		notes=""
		mapzoom=4
		minColorbar=0
		maxColorbar=400

	collection,collectionLongName= collectionMethods.get_collection(product, variable,dateStart, dateEnd);
	collection =collectionMethods.filter_domain1(collection,domainType,subdomain)

	template_values = {
	}
	if(variable=='NDVI' or variable=='NDSI'):
		if(domainType=='points'):
			timeSeriesData=collectionMethods.get_timeseries(collection,point,variable)

			timeSeriesGraphData = []	
			n_rows = numpy.array(timeSeriesData).shape[0];
			for i in range(2,n_rows):
			  entry = {'count':timeSeriesData[i][1],'name':timeSeriesData[i][0]};
			  timeSeriesGraphData.append(entry);

			template_values = {
			    'timeSeriesData': timeSeriesData,
	    		    'timeSeriesGraphData': timeSeriesGraphData,
			}
		title='Median '+variable;
		source=collectionLongName+' from '+dateStart+'-'+dateEnd+''
	elif(variable=='pr'): 
		title='Total Precipitation (mm)';
		source=collectionLongName+' from '+dateStart+'-'+dateEnd+''

	collection = collectionMethods.get_statistic(collection,variable);
	collection =collectionMethods.filter_domain2(collection,domainType,subdomain)
	mapid =collectionMethods.map_collection(collection,minColorbar,maxColorbar,variable)

	extra_template_values = {
	    'pointLat': pointLat,
	    'pointLong': pointLong,
	    'product': product,
	    'productLongName': productLongName,
	    'notes': notes,
	    'variable': variable,
	    'state': state,
	    #'polygon': polygon,
	    'domainType': domainType,
	    'dateStart': dateStart,
	    'dateEnd': dateEnd,
	    'ppost': ppost,
	    'title': title,
	    'source': source,
	    'mapzoom': mapzoom,
	    'mapid': mapid['mapid'],
	    'token': mapid['token'],
	    'formVariableGrid': formVariableGrid,
	    'formLocation': formLocation,
	    'formVariableLandsat': formVariableLandsat,
	    'formStates': formStates,
	}
	template_values = dict(template_values,**extra_template_values);

        template = JINJA_ENVIRONMENT.get_template('droughttool.php')
        self.response.out.write(template.render(template_values))

#############################################
##       CONTACT PAGE                      ##
#############################################
class ContactPage(webapp2.RequestHandler):
    def get(self):   
        template = JINJA_ENVIRONMENT.get_template('contact.html')
        self.response.out.write(template.render({}))

#############################################
##       ABOUT DATA PAGE                   ##
#############################################
class DataPage(webapp2.RequestHandler):
    def get(self):   
        template = JINJA_ENVIRONMENT.get_template('aboutdata.html')
        self.response.out.write(template.render({}))

#############################################
##       ABOUT METRIC PAGE                 ##
#############################################
class MetricsPage(webapp2.RequestHandler):
    def get(self):   
        template = JINJA_ENVIRONMENT.get_template('aboutmetrics.html')
        self.response.out.write(template.render({}))

#############################################
##       URL MAPPING                        ##
#############################################
app = webapp2.WSGIApplication(
    [('/', MainPage),
    ('/droughttool', DroughtTool),
    ('/contact',ContactPage),
    ('/aboutdata',DataPage),
    ('/aboutmetrics',MetricsPage)],
    #('/worker', TaskWorker),
    #('/progress', ProgressWorker)],
    debug=True)
