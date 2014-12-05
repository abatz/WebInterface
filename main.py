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
import httplib2 

from forms import *   
import collectionMethods
from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(60)
httplib2.Http(timeout=15)

#############################################
##       SET DIRECTORY FOR PAGES          ##
#############################################
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
#############################################
##      GET                                ##
#############################################
    def get(self): 
        ppost=0	
        ee.Initialize(config.EE_CREDENTIALS, config.EE_URL)

	#mapzoom,pointLat,pointLong,state,variable,domainType,dateStart,dateEnd,anomOrValue,opacity,NELat,NELong,SWLat,SWLong\
        #    =collectionMethods.initialize_form(self,ppost);
        initial_mapzoom=4;
        initial_pointLat=42;
        initial_pointLong=-112;
        initial_state='Calfornia';
        initial_variable='pr';
        initial_domainType='full';
        initial_dateStart='2013-01-01';
        initial_dateEnd='2013-03-31';
        initial_anomOrValue='anom';
        initial_opacity=str(14*0.05);
        initial_NELat=45;
        initial_NELong=-95;
        initial_SWLat=40;
        initial_SWLong=-111;

        #initialize forms
        mapzoom=self.request.get('mapzoom',initial_mapzoom);
        pointLat=self.request.get('pointLat',initial_pointLat);
        pointLong=self.request.get('pointLong',initial_pointLong);
        state=self.request.get('state',initial_state);
        variable=self.request.get('variable',initial_variable);
        domainType=self.request.get('domainType',initial_domainType);
        dateStart=self.request.get('dateStart',initial_dateStart);
        dateEnd=self.request.get('dateEnd',initial_dateEnd);
        anomOrValue=self.request.get('anomOrValue',initial_anomOrValue);
        opacity=self.request.get('opacity',initial_opacity);
        NELat=float(self.request.get('NELat',initial_NELat));
        NELong=float(self.request.get('NELong',initial_NELong));
        SWLat=float(self.request.get('SWLat',initial_SWLat));
        SWLong=float(self.request.get('SWLong',initial_SWLong));

        #if self.request.arguments():	
        #    palette=self.request.get('palette','');
        #    minColorbar=float(self.request.get('minColorbar',''));
        #    maxColorbar=float(self.request.get('maxColorbar',''));
	#    colorbarLabel='';
        #    mapid,template_values,colorbarLabel,product,collectionLongName,notes,title,source,mapzoom= \
        #        collectionMethods.get_images(opacity,pointLat,pointLong,NELat,NELong,SWLat,SWLong,ppost,\
        #          variable,state,domainType,dateStart,dateEnd,anomOrValue,palette,minColorbar,maxColorbar);
        #else:
        palette,minColorbar,maxColorbar,colorbarLabel=collectionMethods.get_colorbar(variable,anomOrValue);

        shareLink = 'khegewisch-test.appspot.com'+'?mapzoom='+str(mapzoom)+'?pointLat='+str(pointLat)+\
            '?pointLong='+str(pointLong)+'?variable='+variable+'?opacity='+str(opacity)+'?dateStart='+dateStart+'?dateEnd='+dateEnd;
             # not working currently... should only put variables in link that are different from the initialization values..
             #if(mapzoom!=initial_mapzoom):
             #  shareLink=shareLink+'?mapzoom='+str(mapzoom)
             #if(pointLat!=initial_pointLat):
             #  shareLink=shareLink+'?pointLat='+str(pointLat)
             #if(pointLong!=initial_pointLong):
             #shareLink=shareLink+'?pointLong='+str(pointLong)

        base_template_values = {   #these are the same base as in POST
            'shareLink': shareLink,
            'opacity': opacity,
            'pointLat': pointLat,
            'pointLong': pointLong,
            'NELat': NELat,
            'NELong': NELong,
            'SWLat': SWLat,
            'SWLong': SWLong,
            'ppost': ppost,
            'mapzoom': mapzoom,
            'variable': variable,
            'state': state,
            'domainType': domainType,
            'dateStart': dateStart,
            'dateEnd': dateEnd,
            'anomOrValue': anomOrValue,
            'formOpacity': formOpacity,
            'formAnomOrValue': formAnomOrValue,
            'formVariableGrid': formVariableGrid,
            'formLocation': formLocation,
            'formVariableLandsat': formVariableLandsat,
            'formStates': formStates,
            'palette': palette,
            'minColorbar': minColorbar,
            'maxColorbar': maxColorbar,
         }
	template_values = base_template_values; 
        template = JINJA_ENVIRONMENT.get_template('droughttool.php')
        self.response.out.write(template.render(template_values))

    #############################################
    ##      POST                                ##
    #############################################
    def post(self):
        ppost=1
        ee.Initialize(config.EE_CREDENTIALS, config.EE_URL)

        #Get data from form
        opacity= self.request.get('opacity')
        dateStart= self.request.get('dateStart')
        dateEnd = self.request.get('dateEnd')
        variable =self.request.get('basicvariable')
        domainType =self.request.get('domainType')
        state=self.request.get('state')
        anomOrValue=self.request.get('anomOrValue')
        pointLatLong = self.request.get('pointLatLong')
        pointLatLongX = pointLatLong.split(",")
        pointLong = float(pointLatLongX[0])
        pointLat = float(pointLatLongX[1])
        NELat = float(self.request.get('NELat'))
        NELong = float(self.request.get('NELong'))
        SWLat = float(self.request.get('SWLat'))
        SWLong = float(self.request.get('SWLong'))

        palette=self.request.get('palette');
        minColorbar=float(self.request.get('minColorbar'));
        maxColorbar=float(self.request.get('maxColorbar'));

	if(variable=='wb'):
            mapid,template_values,colorbarLabel,product,collectionLongName,notes,title,source,mapzoom,palette,minColorbar,maxColorbar=\
	        collectionMethods.get_wb(opacity,pointLat,pointLong,NELat,NELong,SWLat,SWLong,ppost,\
    	        state,domainType,dateStart,dateEnd,anomOrValue,palette,minColorbar,maxColorbar);
	else:
            mapid,template_values,colorbarLabel,product,collectionLongName,notes,title,source,mapzoom,palette,minColorbar,maxColorbar=\
	        collectionMethods.get_images(opacity,pointLat,pointLong,NELat,NELong,SWLat,SWLong,ppost,\
    	        variable,state,domainType,dateStart,dateEnd,anomOrValue,palette,minColorbar,maxColorbar);

        shareLink = 'khegewisch-test.appspot.com'+'?mapzoom='+str(mapzoom)+'?pointLat='+str(pointLat)+\
	'?pointLong='+str(pointLong)+'?variable='+variable+'?opacity='+str(opacity)+'?dateStart='+dateStart+'?dateEnd='+dateEnd;

        extra_template_values = {
            'shareLink': shareLink,
            'colorbarLabel': colorbarLabel,
            'opacity': opacity,
            'pointLat': pointLat,
            'pointLong': pointLong,
            'NELat': NELat,
            'NELong': NELong,
            'SWLat': SWLat,
            'SWLong': SWLong,
            'product': product,
            'productLongName': collectionLongName,
            'notes': notes,
            'variable': variable,
            'state': state,
            'domainType': domainType,
            'dateStart': dateStart,
            'dateEnd': dateEnd,
            'anomOrValue': anomOrValue,
            'ppost': ppost,
            'title': title,
            'source': source,
            'mapzoom': mapzoom,
            'mapid': mapid['mapid'],
            'token': mapid['token'],
            'formOpacity': formOpacity,
            'formAnomOrValue': formAnomOrValue,
            'formVariableGrid': formVariableGrid,
            'formLocation': formLocation,
            'formVariableLandsat': formVariableLandsat,
            'formStates': formStates,
            'palette': palette,
            'minColorbar': minColorbar,
            'maxColorbar': maxColorbar,
        }
        template_values = dict(template_values,**extra_template_values);

        template = JINJA_ENVIRONMENT.get_template('droughttool.php')
        self.response.out.write(template.render(template_values))

#############################################
##       CONTACT PAGE                      ##
#############################################
#class ContactPage(webapp2.RequestHandler):
#	def get(self):   
#		template = JINJA_ENVIRONMENT.get_template('contact.html')
#		self.response.out.write(template.render({}))

#############################################
##       ABOUT DATA PAGE                   ##
#############################################
#class DataPage(webapp2.RequestHandler):
#	def get(self):   
#		template = JINJA_ENVIRONMENT.get_template('aboutdata.html')
#		self.response.out.write(template.render({}))

#############################################
##       ABOUT METRIC PAGE                 ##
#############################################
#class MetricsPage(webapp2.RequestHandler):
#	def get(self):   
#		template = JINJA_ENVIRONMENT.get_template('aboutmetrics.html')
#		self.response.out.write(template.render({}))

#############################################
##       URL MAPPING                        ##
#############################################
app = webapp2.WSGIApplication(
    [#('/', MainPage),
    ('/', DroughtTool),
    #('/droughttool', DroughtTool),
    #('/droughttool/', DroughtTool),
    #('/contact',ContactPage),
    #('/aboutdata',DataPage),
    #('/aboutmetrics',MetricsPage)
],
debug=True)
