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
	mapzoom=7
	pointLat = 39.5272
	pointLong = -119.8219

        template_values = {
	    'pointLat': pointLat,
	    'pointLong': pointLong,
	    'ppost': ppost,
	    'mapzoom': mapzoom,
	    'formVariableGrid': formVariableGrid,
	    'formLocation': formLocation,
	    'formVariableLandsat': formVariableLandsat,
	    'formStates': formStates,
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
	point = ee.Feature.Point(pointLong,pointLat);
	state=self.request.get('state')
	if(domainType=='points' or domainType=='conus'):
		subdomain = point;
	elif(domainType=='states'):
		subdomain=state;

	template_values = {
	}
	if(variable=='NDVI' or variable=='NDSI'):
		product = 'landsat'
		mapzoom=4 #was 7
		minColorbar=-.1
		maxColorbar=.9

    		collection,collectionLongName= collectionMethods.get_collection(product, variable,dateStart, dateEnd);
		collection = collectionMethods.get_statistic(collection,variable);
		collection =collectionMethods.filter_domain(collection,domainType,subdomain)
		mapid =collectionMethods.map_collection(collection,minColorbar,maxColorbar,variable)
		#timeSeriesData=collectionMethods.get_timeseries(collection,point,variable)

		title='Median '+variable;
		source=collectionLongName+' from '+dateStart+'-'+dateEnd+''

		template_values = {
		    #'timeSeriesData': timeSeriesData,
                }

	elif(variable=='pr'): 
		product = 'gridded'
		mapzoom=4
		minColorbar=0
		maxColorbar=400

    		collection,collectionLongName= collectionMethods.get_collection(product, variable,dateStart, dateEnd);
		collection = collectionMethods.get_statistic(collection,variable);
		collection =collectionMethods.filter_domain(collection,domainType,subdomain)
		mapid =collectionMethods.map_collection(collection,minColorbar,maxColorbar,variable)

  		#collection= gridded.get_collection(product, variable,dateStart, dateEnd)
		#mapid =gridded.map_collection(collection,minColorbar,maxColorbar)
		#climatologycollection =gridded.get_climatologycollection(product,variable,dateStart,dateEnd)
		#mapid =gridded.map_collection(climatologycollection,minColorbar,maxColorbar)

		title='Total Precipitation (mm) ('+dateStart+'-'+dateEnd+')';
		source=collectionLongName+' from '+dateStart+'-'+dateEnd+''

	extra_template_values = {
	    'pointLat': pointLat,
	    'pointLong': pointLong,
	    'state': state,
	    'variable': variable,
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
