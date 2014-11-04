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

        template_values = {
	    'formProduct': formProduct,
	    'formVariableGrid': formVariableGrid,
	    'formVariableLandsat': formVariableLandsat,
	    'formVariableModis': formVariableModis,
	    'formGridTimeSpan': formGridTimeSpan,
	    'formLandsatTimeSpan': formLandsatTimeSpan,
	    'formModisTimeSpan': formModisTimeSpan,
	    'formDayTimeChoice': formDayTimeChoice,
	    'formMonthTimeChoice': formMonthTimeChoice,
	    'formMonthStart': formMonthStart,
	    'formDayStart': formDayStart,
	    'formYearStart': formYearStart,
	    'formMonthEnd': formMonthEnd,
	    'formDayEnd': formDayEnd,
	    'formYearEnd': formYearEnd,
	    'formBasicVariable': formBasicVariable,
	    'formDisplay': formDisplay,
	    'formMetric': formMetric,
	    'formStatistic': formStatistic,
	    'ppost': ppost,
        }
        template = JINJA_ENVIRONMENT.get_template('droughttool.php')
        self.response.out.write(template.render(template_values))
    def post(self):
        #ee.Initialize(config.EE_CREDENTIALS, config.EE_URL)
	#Get data from form
        dateStart= cgi.escape(self.request.get('dateStart'))
        dateEnd = cgi.escape(self.request.get('dateEnd'))
        userLatLong = cgi.escape(self.request.get('userLatLong'))
        userLatLongX = userLatLong.split(",")
        userLong = float(userLatLongX[0])
        userLat = float(userLatLongX[1])
	product =self.request.get('product')
	variable =self.request.get('variable')

	point = ee.Feature.Point(userLong,userLat);

	if(product =='landsat' and variable=='NDVI'):
		minColorbar=-.1
		maxColorbar=.9
    		collection= landsat.get_collection(product, variable,point,dateStart, dateEnd)
		mapid =landsat.map_collection(collection,minColorbar,maxColorbar)
		timeSeriesData=landsat.get_timeseries(collection,point,variable)
	#elif(product=='gridded' and variable=='PPT'):
    	#	collection= gridded.get_collection(product, variable,point,dateStart, dateEnd)
	#	mapid =gridded.map_collection(collection,minColorbar,maxColorbar)
	#	timeSeriesData=gridded.get_timeseries(collection,point,variable)
	
	#minColorbar =self.request.get('minColorbar')
	#maxColorbar =self.request.get('maxColorbar')

	ppost=1

 	template_values = {
            'mapid': mapid['mapid'],
            'token': mapid['token'],
            'formProduct': formProduct,
            'formVariableGrid': formVariableGrid,
            'formVariableLandsat': formVariableLandsat,
            'formVariableModis': formVariableModis,
            'formGridTimeSpan': formGridTimeSpan,
            'formLandsatTimeSpan': formLandsatTimeSpan,
            'formModisTimeSpan': formModisTimeSpan,
            'formDayTimeChoice': formDayTimeChoice,
            'formMonthTimeChoice': formMonthTimeChoice,
            'formMonthStart': formMonthStart,
            'formDayStart': formDayStart,
            'formYearStart': formYearStart,
            'formMonthEnd': formMonthEnd,
            'formDayEnd': formDayEnd,
            'formYearEnd': formYearEnd,
            'formBasicVariable': formBasicVariable,
	    'formDisplay': formDisplay,
	    'formMetric': formMetric,
	    'formStatistic': formStatistic,
	    'timeSeriesData': timeSeriesData,
	    'userLat': userLat,
	    'userLong': userLong,
	    'product': product,
	    'variable': variable,
	    'ppost': ppost,
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
