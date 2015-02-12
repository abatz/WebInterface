#############################################
##       MAIN HANDLER FILE FOR VIEWS       ##
#############################################
import datetime
import json
import logging
import os

import cgi
import config
import ee
import httplib2
import jinja2
import numpy
import webapp2

import forms
import processingMethods
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
    def set_share_link(self, initial_template_values):
        shareLink = 'drought-monitor3.appspot.com?'
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
        tempstart = datetime.date.today()-datetime.timedelta(days=60)
        tempend = datetime.date.today()-datetime.timedelta(days=2)
        template_values = {
            'mapid':self.request.get('mapid',''),
            'token':self.request.get('token',''),
            'form_error': {},
            #Variable Options
            'variable': self.request.get('variable','Gpr'),
            'statistic': self.request.get('statistic','Total'),
            'anomOrValue': self.request.get('anomOrValue','value'),
            'units': self.request.get('units','metric'),
            'varUnits': self.request.get('varUnits','mm'),
            #Time Options
            'minYear':self.request.get('minYear','1979'),
            'minDate':self.request.get('minDate','1979-01-01'),
            'maxDate':self.request.get('maxDate',tempend.strftime('%Y-%m-%d')),
            'maxYear':self.request.get('maxYear',tempend.strftime('%Y')),
            'dateStart': self.request.get('dateStart',tempstart.strftime('%Y-%m-%d')),
            'dateEnd': self.request.get('dateEnd',tempend.strftime('%Y-%m-%d')),
            'yearStart': self.request.get('yearStart','1979'),
            'yearEnd': self.request.get('yearEnd',tempend.strftime('%Y')),
            #Map Options
            'opacity': self.request.get('opacity',str(14*0.05)),
            'mapCenterLongLat':self.request.get('mapCenterLongLat','-112,42'),
            'NELat': self.request.get('NELat',45),
            'NELong': self.request.get('NELong',-95),
            'SWLat': self.request.get('SWLat',40),
            'SWLong': self.request.get('SWLong',-111),
            'ppost': 0,
            'state': self.request.get('state','California'),
            'domainType': self.request.get('domainType','full'),
            'background': self.request.get('background','nowhitebackground'),
            'layer': self.request.get('layer','none'),
            'kmlurl': self.request.get('kmlurl', ''),
            'kmloption': self.request.get('kmloption', ''),
            #Colorbar Options
            'palette': self.request.get('palette', None),
            'minColorbar': self.request.get('minColorbar', 0),
            'maxColorbar': self.request.get('maxColorbar', 400),
            'colorbarmap': self.request.get('colorbarmap', 'GnBu'),
            'colorbarsize': self.request.get('colorbarsize', '8'),
            'colorbarLabel': self.request.get('colorbarLabel', 'Total Precipitation (mm)'),
            #TimeSeries Options
            'timeSeriesCalc': self.request.get('timeSeriesCalc','days'),
            'chartType': self.request.get('chartType', 'column'),
            #PointMarker Options
            'marker_colors':['blue', 'green', 'orange', 'purple','yellow', 'pink','red'],
            'p1check': self.request.get('p1check','checked'),
            'p2check': self.request.get('p2check','checked'),
            'p3check': self.request.get('p3check','checked'),
            'p4check': self.request.get('p4check','checked'),
            'p5check': self.request.get('p5check','checked'),
            'p6check': self.request.get('p6check','checked'),
            'p7check': self.request.get('p7check','checked'),
            'p1display': self.request.get('p1display','block'),
            'p2display': self.request.get('p2display','none'),
            'p3display': self.request.get('p3display','none'),
            'p4display': self.request.get('p4display','none'),
            'p5display': self.request.get('p5display','none'),
            'p6display': self.request.get('p6display','none'),
            'p7display': self.request.get('p7display','none'),
            #Forms
            'formChartType': forms.formChartType,
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
        #Conditional template values
        #Climatology start year depends in minYear of variable
        template_values['yearStartClim'] = self.request.get('yearStartClim',template_values['minYear'])
        template_values['yearEndClim'] = self.request.get('yearEndClim','2010')
        #Map zoom depends on domain type
        if template_values['domainType'] == 'full':
            mz= '5'
        elif template_values['domainType'] == 'states':
            mz= '6'
            stLong = str(forms.stateLong[template_values['state']])
            stLat = str(forms.stateLat[template_values['state']])
            template_values['mapCenterLongLat'] = stLong + ',' + stLat
        else:
            mz='4'
        template_values['mapzoom'] = self.request.get('mapzoom',mz)
        #Markers are initialized to center of map
        template_values['pointsLongLat'] = self.request.get('pointsLongLat',template_values['mapCenterLongLat'])
        template_values['p1'] = self.request.get('p1',template_values['mapCenterLongLat'])
        template_values['p2'] = self.request.get('p2',template_values['mapCenterLongLat'])
        template_values['p3'] = self.request.get('p3',template_values['mapCenterLongLat'])
        template_values['p4'] = self.request.get('p4',template_values['mapCenterLongLat'])
        template_values['p5'] = self.request.get('p5',template_values['mapCenterLongLat'])
        template_values['p6'] = self.request.get('p6',template_values['mapCenterLongLat'])
        template_values['p7'] = self.request.get('p7',template_values['mapCenterLongLat'])

        #Sharelink depends on most template variables
        template_values['shareLink'] = self.set_share_link(template_values)

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
        #self.set_form_params()
        template_values = self.set_initial_template_values()

        #Check user input for errors:
        fieldID,input_err = self.check_user_input(template_values)
        if not input_err:
            if self.request.arguments():
                #Update template values with mapid or time series data
                if template_values['domainType'] == 'full':
                    template_values = processingMethods.get_images(template_values)
                else:  #want ability in future to look at time series for states,etc
                    template_values = processingMethods.get_time_series(template_values)
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

        #self.set_form_params()
        template_values = self.set_initial_template_values()
        #Check user input for errors:
        fieldID,input_err = self.check_user_input(template_values)
        if not input_err:
            #Override ppost default
            template_values['ppost'] = 1
            #Update template values with mapid or time series data
            if template_values['domainType'] == 'full':
                template_values = processingMethods.get_images(template_values)
            else: #want ability in future to do time series of states,etc
                template_values = processingMethods.get_time_series(template_values)
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
