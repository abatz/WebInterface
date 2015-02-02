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

import forms
import collectionMethods
import figureFormatting

from google.appengine.api import urlfetch
urlfetch.set_default_fetch_deadline(60000)
httplib2.Http(timeout=30000)

#############################################
##       SET DIRECTORY FOR PAGES          ##
#############################################
template_dir = os.path.join(os.path.dirname(__file__),'templates')
JINJA_ENVIRONMENT= jinja2.Environment(autoescape=True,
    loader=jinja2.FileSystemLoader(template_dir))

#############################################
##       DROUGHT TOOL PAGE                 ##
#############################################
class DroughtTool(webapp2.RequestHandler):
    def set_form_params(self):
        #sets form  parameters
        self.ppost = 0
        self.form_error = {}

        #Variable Options
        self.variable = self.request.get('variable','Gpr')
        self.statistic = self.request.get('statistic','Total')
        self.anomOrValue = self.request.get('anomOrValue','value')
        self.units = self.request.get('units','metric')
        self.varUnits = self.request.get('varUnits','mm')

        #Time Options
        self.minYear = self.request.get('minYear','1979')
	tempstart = datetime.date.today()-datetime.timedelta(days=60)
	tempend = datetime.date.today()-datetime.timedelta(days=2)
        self.dateStart = self.request.get('dateStart',tempstart.strftime('%Y-%m-%d'))
        self.dateEnd = self.request.get('dateEnd',tempend.strftime('%Y-%m-%d'))
        self.dayStart = self.request.get('dayStart','1')
        self.dayEnd = self.request.get('dayEnd','31')
        self.monthStart = self.request.get('monthStart',tempstart.strftime('%mm'));
        self.monthEnd = self.request.get('monthEnd',tempend.strftime('%mm'));
        self.yearStart = self.request.get('yearStart','1979');
        self.yearEnd = self.request.get('yearEnd',tempend.strftime('%Y'));
        self.yearStartClim = self.request.get('yearStartClim',self.minYear);
        self.yearEndClim= self.request.get('yearEndClim','2010');
        #self.yearEndClim= self.request.get('yearEndClim',tempend.strftime('%Y'));

        #Map Options
        self.mapid = self.request.get('mapid','')
        self.token = self.request.get('token','')
        self.mapCenterLongLat = self.request.get('mapCenterLongLat','-112,42')
        self.opacity = self.request.get('opacity',str(14*0.05))
        self.domainType = self.request.get('domainType','full')
        self.state = self.request.get('state','California')
        self.background = self.request.get('background','nowhitebackground')
        self.layer = self.request.get('layer','none')
        self.NELat = self.request.get('NELat',45)
        self.NELong= self.request.get('NELong',-95)
        self.SWLat= self.request.get('SWLat',40)
        self.SWLong= self.request.get('SWLong',-111)
        self.kmloption = self.request.get('kmloption', '')
        self.kmlurl = self.request.get('kmlurl', '')
	if(self.domainType=='full'):
            mz= '5';
        elif(self.domainType=='states'):
            mz= '6';
	    self.mapCenterLongLat = str(forms.stateLong[self.state])+','+str(forms.stateLat[self.state]);
	else:
	    mz='4';
        self.mapzoom = self.request.get('mapzoom',mz)
   
        #Colorbar Options
        self.minColorbar = self.request.get('minColorbar', None)
        self.maxColorbar = self.request.get('maxColorbar', None)
        self.palette = self.request.get('palette', None)
        self.colorbarmap = self.request.get('colorbarmap', 'GnBu')
        self.colorbarsize = self.request.get('colorbarsize', '8')
        if self.minColorbar is None and self.maxColorbar is None:
            self.colorbarmap,self.colorbarsize,self.minColorbar,self.maxColorbar,self.colorbarLabel,self.varUnits,\
                 =collectionMethods.get_colorbar(self.variable,self.anomOrValue,self.units)

        #TimeSeries Options
        self.pointsLongLat = self.request.get('pointsLongLat',self.mapCenterLongLat)
        self.timeSeriesCalc = self.request.get('timeSeriesCalc','days')

        #Points/marker Options
        #Long,Lat inputs
        self.p1 = self.request.get('p1',self.mapCenterLongLat);
        self.p2 = self.request.get('p2',self.mapCenterLongLat);
        self.p3 = self.request.get('p3',self.mapCenterLongLat);
        self.p4 = self.request.get('p4',self.mapCenterLongLat);
        self.p5 = self.request.get('p5',self.mapCenterLongLat);
        self.p6 = self.request.get('p6',self.mapCenterLongLat);
        self.p7 = self.request.get('p7',self.mapCenterLongLat);

        #checkboxes and displays
        self.p1check =self.request.get('p1check','checked');self.p2check=self.request.get('p2check','checked')
        self.p3check =self.request.get('p3check','checked');self.p4check=self.request.get('p4check','checked')
        self.p5check =self.request.get('p5check','checked');self.p6check=self.request.get('p6check','checked')
        self.p7check =self.request.get('p7check','checked')
        self.p1display =self.request.get('p1display','block');self.p2display=self.request.get('p2display','none')
        self.p3display =self.request.get('p3display','none');self.p4display=self.request.get('p4display','none')
        self.p5display =self.request.get('p5display','none');self.p6display=self.request.get('p6display','none')
        self.p7display =self.request.get('p7display','none');
        self.marker_colors = ['blue', 'green', 'orange', 'purple',\
        'yellow', 'pink','red']

    def set_share_link(self, initial_template_values):
        shareLink = 'drought-monitor2.appspot.com?'
        for key, val in initial_template_values.iteritems():
            if str(key[0:4]) == 'form':
                continue
            if key == 'ppost':continue
            param_str = str(key) + '=' + str(val)
            if shareLink[-1] =='?':
                shareLink+=param_str
            else:
                shareLink+='&' + param_str
        return shareLink

    def set_initial_template_values(self):
        template_values = {
            'mapid':self.mapid,
            'token':self.token,
            'form_error': self.form_error,
            #Variable Options
            'variable': self.variable,
            'statistic': self.statistic,
            'anomOrValue': self.anomOrValue,
            'units': self.units,
            'varUnits': self.varUnits,
            #Time Options
            'minYear':self.minYear,
            'dateStart': self.dateStart,
            'dateEnd': self.dateEnd,
            'yearStart': self.yearStart,
            'yearEnd': self.yearEnd,
            'yearStartClim': self.yearStartClim,
            'yearEndClim': self.yearEndClim,
            #Map Options
            'opacity': self.opacity,
            'pointsLongLat':self.pointsLongLat,
            'mapCenterLongLat':self.mapCenterLongLat,
            'NELat': self.NELat,
            'NELong': self.NELong,
            'SWLat': self.SWLat,
            'SWLong': self.SWLong,
            'ppost': self.ppost,
            'mapzoom': self.mapzoom,
            'state': self.state,
            'domainType': self.domainType,
            'background': self.background,
            'layer': self.layer,
            'kmlurl': self.kmlurl,
            'kmloption': self.kmloption,
            #Colorbar Options
            'palette': self.palette,
            'minColorbar': self.minColorbar,
            'maxColorbar': self.maxColorbar,
            'colorbarmap': self.colorbarmap,
            'colorbarsize': self.colorbarsize,
            #TimeSeries Options
            'timeSeriesCalc': self.timeSeriesCalc,
            #PointMarker Options
            'marker_colors':self.marker_colors,
            'p1':self.p1,
            'p2':self.p2,
            'p3':self.p3,
            'p4':self.p4,
            'p5':self.p5,
            'p6':self.p6,
            'p7':self.p7,
            'p1check':self.p1check,
            'p2check':self.p2check,
            'p3check':self.p3check,
            'p4check':self.p4check,
            'p5check':self.p5check,
            'p6check':self.p6check,
            'p7check':self.p7check,
            'p1display':self.p1display,
            'p2display':self.p2display,
            'p3display':self.p3display,
            'p4display':self.p4display,
            'p5display':self.p5display,
            'p6display':self.p6display,
            'p7display':self.p7display,
             #Forms
            'formMonth': forms.formMonth,
            'formDay': forms.formDay,
            'formYear': forms.formYear,
            'formMapZoom': forms.formMapZoom,
            'formPaletteDivMap': forms.formPaletteDivMap,
            'formPaletteSeqMap': forms.formPaletteSeqMap,
            'formPaletteSize': forms.formPaletteSize,
            'formOpacity': forms.formOpacity,
            'formUnits': forms.formUnits,
            'formAnomOrValue': forms.formAnomOrValue,
            'formBackground': forms.formBackground,
            'formTimeSeriesCalc': forms.formTimeSeriesCalc,
            'formVariableGrid': forms.formVariableGrid,
            'formStatistic': forms.formStatistic,
            'formLocation': forms.formLocation,
            'formVariableLandsat': forms.formVariableLandsat,
            'formVariableModis': forms.formVariableModis,
            'formStates': forms.formStates,
            'formLayers': forms.formLayers
        }

        #why is this section necessary? -kch
        if self.colorbarmap:
            template_values['colorbarmap']= self.colorbarmap
        if self.colorbarsize:
            template_values['colorbarsize']= self.colorbarsize
        if self.palette:
            template_values['palette']= self.palette
        if self.minColorbar:
            template_values['minColorbar']= self.minColorbar
        if self.maxColorbar:
            template_values['maxColorbar']= self.maxColorbar
        template_values['shareLink'] = self.set_share_link(template_values)
        if self.minColorbar:
            template_values['minColorbar'] = self.minColorbar
        if self.maxColorbar:
            template_values['maxColorbar'] = self.maxColorbar
        if self.kmlurl:
            template_values['kmlurl'] = self.kmlurl
        if self.kmloption:
            template_values['kmloption'] = self.kmloption

        #format template values to allow for different date formats etc...
        #See format_ functions in forms.py
        formatted_template_values = {}
        for key, val in template_values.iteritems():
            format_function_name = 'format_' + key
            try:
                format_function = getattr(forms,format_function_name)
            except:
                format_function = None

            if format_function:
                formatted_template_values[key] = format_function(val)
            else:
                formatted_template_values[key] = val
        return formatted_template_values

    def check_user_input(self, template_values):
        #Checks for errors in user input
        #See check_ functions in forms.py
        #At first error encountered, spits out error message and exits
        err = None; fieldID = None
        for key, val in template_values.iteritems():
            #do not check form items
            if key[0:4] == 'form':
                continue
            check_function_name = 'check_' + key
            try:
                #See if a check function exists in forms.py
                #If so, executed to check for form errors
                check_function = getattr(forms,check_function_name)
            except:
                continue
            err = check_function(val)
            if err:
                fieldID = key
                return fieldID,err
        return fieldID,err
    #############################################
    ##      GET                                ##
    #############################################
    def get(self):
        ppost=0
        ee.Initialize(config.EE_CREDENTIALS, config.EE_URL)
	ee.data.setDeadline(60000);

        #initialize forms
        self.set_form_params()
        template_values = self.set_initial_template_values()

        #Check user input for errors:
        fieldID,input_err = self.check_user_input(template_values)
        if not input_err:
            if self.request.arguments():
                #Update template values with mapid or time series data
                if self.domainType == 'full':
                    template_values = collectionMethods.get_images(template_values)
                else:  #want ability in future to look at time series for states,etc
                    template_values = collectionMethods.get_time_series(template_values)
        else:
            template_values['form_error'] = {fieldID:input_err}

        template = JINJA_ENVIRONMENT.get_template('droughttool.php')
        self.response.out.write(template.render(template_values))
    #############################################
    ##      POST                                ##
    #############################################
    def post(self):
        ee.Initialize(config.EE_CREDENTIALS, config.EE_URL)
	ee.data.setDeadline(60000);

        self.set_form_params()
        template_values = self.set_initial_template_values()
        #Check user input for errors:
        fieldID,input_err = self.check_user_input(template_values)
        if not input_err:
            #Override ppost default
            template_values['ppost'] = 1
            #Update template values with mapid or time series data
            if self.domainType == 'full':
                template_values = collectionMethods.get_images(template_values)
            else: #want ability in future to do time series of states,etc
                template_values = collectionMethods.get_time_series(template_values)
        else:
            #write error message to html
            template_values['form_error'] = {fieldID:input_err}
        template = JINJA_ENVIRONMENT.get_template('droughttool.php')
        self.response.out.write(template.render(template_values))

#############################################
##       URL MAPPING                        ##
#############################################
app = webapp2.WSGIApplication(
    [
    ('/', DroughtTool),
],
debug=True)
