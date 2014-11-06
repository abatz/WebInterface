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
	    'formVariableGrid': formVariableGrid,
	    'formVariableLandsat': formVariableLandsat,
	    'formStates': formStates,
	     #'progressScriptActive':False,
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
	variable =self.request.get('basicvariable')
	#key =self.request.get('key')

	state =self.request.get('state')
	point = ee.Feature.Point(userLong,userLat);
	#taskqueue.add(url='/worker', params={'key': key})

	if(variable=='NDVI' or variable=='NDSI'):
		product = 'landsat'
		mapzoom=7
		title='Average NDVI ('+dateStart+'-'+dateEnd+')';
		source='Landsat 5,7,8, median-pixel composite'
		minColorbar=-.1
		maxColorbar=.9
    		collection= landsat.get_collection(product, variable,dateStart, dateEnd,'point',point,state)
    		#collection= landsat.get_collection(product, variable,dateStart, dateEnd,'state',point,state)
		mapid =landsat.map_collection(collection,minColorbar,maxColorbar,variable)
		timeSeriesData=landsat.get_timeseries(collection,point,variable)
		template_values = {
		    'userLat': userLat,
		    'userLong': userLong,
		    'product': product,
		    'variable': variable,
		    'ppost': ppost,
		    'title': title,
		    'source': source,
		    'mapzoom': mapzoom,
		    'mapid': mapid['mapid'],
		    'token': mapid['token'],
		    'formVariableGrid': formVariableGrid,
		    'formVariableLandsat': formVariableLandsat,
	    	    'formStates': formStates,
		    'timeSeriesData': timeSeriesData,
		}
	elif(variable=='pr'): 
		product = 'gridded'
		mapzoom=4
		title='Total Precipitation(mm) ('+dateStart+'-'+dateEnd+')';
		source='gridMET 4-km observational dataset, University of Idaho'
		variable = 'pr'
		minColorbar=0
		maxColorbar=400
    		collection= gridded.get_collection(product, variable,dateStart, dateEnd)
		mapid =gridded.map_collection(collection,minColorbar,maxColorbar)
		#climatologycollection =gridded.get_climatologycollection(product,variable,dateStart,dateEnd)
		#mapid =gridded.map_collection(climatologycollection,minColorbar,maxColorbar)
		template_values = {
		    'userLat': userLat,
		    'userLong': userLong,
		    'product': product,
		    'variable': variable,
		    'ppost': ppost,
		    'title': title,
		    'source': source,
		    'mapzoom': mapzoom,
		    'mapid': mapid['mapid'],
		    'token': mapid['token'],
		    'formVariableGrid': formVariableGrid,
		    'formVariableLandsat': formVariableLandsat,
	    	    'formStates': formStates,
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
    #('/worker', TaskWorker),
    #('/progress', ProgressWorker)],
    debug=True)
