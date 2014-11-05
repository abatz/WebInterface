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

from forms import *
from functions import *
import gridded
import landsat

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
	userLat = 39.5272
	userLong = -119.8219

        template_values = {
	    'userLat': userLat,
	    'userLong': userLong,
	    'ppost': ppost,
	    'mapzoom': mapzoom,
	    'formProduct': formProduct,
	    'formVariableGrid': formVariableGrid,
	    'formVariableLandsat': formVariableLandsat,
        }
        template = JINJA_ENVIRONMENT.get_template('droughttool.php')
        self.response.out.write(template.render(template_values))
    def post(self):
	ppost=1
        ee.Initialize(config.EE_CREDENTIALS, config.EE_URL)
	#Get data from form
        dateStart= cgi.escape(self.request.get('dateStart'))
        dateEnd = cgi.escape(self.request.get('dateEnd'))
        userLatLong = cgi.escape(self.request.get('userLatLong'))
        userLatLongX = userLatLong.split(",")
        userLong = float(userLatLongX[0])
        userLat = float(userLatLongX[1])
	product =self.request.get('product')
	variable =self.request.get('basicvariable')

	point = ee.Feature.Point(userLong,userLat);

	if(product =='landsat' and variable=='NDVI'):
		mapzoom=7
		title='Average NDVI ('+dateStart+'-'+dateEnd+')';
		minColorbar=-.1
		maxColorbar=.9
    		collection= landsat.get_collection(product, variable,point,dateStart, dateEnd)
		mapid =landsat.map_collection(collection,minColorbar,maxColorbar)
		timeSeriesData=landsat.get_timeseries(collection,point,variable)
		template_values = {
		    'userLat': userLat,
		    'userLong': userLong,
		    'product': product,
		    'variable': variable,
		    'ppost': ppost,
		    'title': title,
		    'mapzoom': mapzoom,
		    'mapid': mapid['mapid'],
		    'token': mapid['token'],
		    'formProduct': formProduct,
		    'formVariableGrid': formVariableGrid,
		    'formVariableLandsat': formVariableLandsat,
		    'timeSeriesData': timeSeriesData,
		}
	#elif(product=='gridded' and variable=='pr'): #this doesn't work because variable='' not 'pr' ??
	else:
		mapzoom=4
		title='Total Precipitation(mm) ('+dateStart+'-'+dateEnd+')';
		variable = 'pr'
		minColorbar=0
		maxColorbar=400
    		collection= gridded.get_collection(product, variable,dateStart, dateEnd)
		mapid =gridded.map_collection(collection,minColorbar,maxColorbar)
		#climatologycollection =gridded.get_climatologycollection(product,variable,dateStart,dateEnd)
		#mapid =gridded.map_collection(climatologycollection,minColorbar,maxColorbar)
		#timeSeriesData=gridded.get_timeseries(collection,point,variable)
		template_values = {
		    'userLat': userLat,
		    'userLong': userLong,
		    'product': product,
		    'variable': variable,
		    'ppost': ppost,
		    'title': title,
		    'mapzoom': mapzoom,
		    'mapid': mapid['mapid'],
		    'token': mapid['token'],
		    'formProduct': formProduct,
		    'formVariableGrid': formVariableGrid,
		    'formVariableLandsat': formVariableLandsat,
		}

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
    debug=True)
