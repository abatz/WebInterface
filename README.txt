This code is for a webpage for visualizing drought metrics utilizing the Google App Engine. 
Currently this webpage: 
	*has information about the project, data sources, data variables and contact info
	*has a draft of a Drought Tool which does: 
		*loads in gridded or remote sensing data from the google cloud
		*visualizes values, climatology or anomalies of this data
		*point selection further funnels the data to the DATA tab
*--------------------------------------------
*  CODE ORGANIZATION
*--------------------------------------------
This code is organized as follows: 

	ee 				-directory of libraries for interfacing with Google Earth Engine
	oauth2client 			-directory of libraries for authentication of Google Earth Engine
	httplib2 			- directory of libraries for ?
	pycrypto			-?? should this directory be here?

	-app.yaml 			- configuration file for webapp2 templating
	-main.py 			- python script that sets up the framework environment and defines classes for handling URL requests 
	-config.py 			- configuration file for setting up Google App Engine
	-main.py 			- python script that sets up the framework environment and defines classes for handling URL requests 
	-forms.py 			- python script which defines the dictionaries for the forms on the DroughtTool interface
	-collectionMethods.py 		- python script of methods for extracting,filtering collectionImages(gridded,remote senesing data on google cloud)

	media
		css			-css webpage styling formats (uses Twitter-Bootstrap web framework)
		js			-bootstrap and jQuery javascript functions
		myjs			-javascript functions written specifically for this project
		      -showLoadingImage.js-javascript function responsive for the progress bar display
		      -formListener.js	-javascript functions for listening for events on the forms of the DrougthTool Interface		
		      -get_colorbar.js  -functions for inserting the colorbar below the google maps
		      -get_colorbar_url.php
		      -graph_utils.js   -javascript functions for making graphs/charts (not currently working)

	templates
		-base.php		-php file for base web template for the look of the webpage
		-home.html		-html file of structure of the home page
		-aboutdata.html		-html file of structure of the aboutData page
		-aboutmetrics.html	-html file of structure of the aboutMetrics page
		-contact.html		-html file of structure of the Contact page
		-droughttool.php	-php file for structure of the Drought Tool page

		descriptions		-directory of page descriptions for aboutData and aboutMetrics and home page
		images			-directory of images
		includes		-directory of html/php files that have been included from the other page templates
			-header.html	-html file for html header inclusions (i.e. css)
			-footer.html	-html file of footer bling
			-basicscripts.php-php file of scripts included in template page (i.e. jQuery, Bootstrap)
			-scripts.php	-php file of scripts included just for the Drought Tool page (i.e. javascript functions,etc)
			-navigation.html-html file for the main navigation tab on page

			-dataform.html	-html file for the data options forms on the webpage (includes basic/advanced forms)
			-mapfiguredata.html-html file for the portion of the page that has map/figure/data

			-basicdataform.html-html file for the basic dataform
			-advanceddataform.html-html file for the basic dataform(not currently being used)

			-map.html	-html file for the MAP portion of the webpage
		        -datatab.html   -html file for the DATA tab on webpage	
		        -figuretab.html -html file for the FIGURE tab on webpage	

*==================
* CONFIGURING YOUR ENVIRONMENT TO RUN THIS CODE
*==================
In order to configure your environment to run this code, you will need to access
the oauth2client, httplib2, pycrypto, and ee libraries.  When running locally,
make sure your Python environment contains these libraries (yolk is a useful
tool for this).  When running in App Engine, you will need to include the
oauth2client, httplib2, and ee libraries in the directory containing the
app.yaml file. Instructions for downloading the libraries are at the end of
this file.

For local development using a personal service account:
* Set up a service account as described here:
  https://sites.google.com/site/earthengineapidocs/creating-oauth2-service-account
* Email the service account email address to your google contact.
* Convert the private key of that service account to a pem file:
  openssl pkcs12 -in downloaded-privatekey.p12 -nodes -nocerts > privatekey.pem
* Old versions of oauth2client will require you to delete the first few
  lines of the of the .pem file so it begins with
  ---BEGIN
  We recommend you update to the most recent version of the libraries.
* Copy the pem file into the directory that has your app.yaml file.
* Update the included config.py file with your service account email
  address.
* Use appcfg.py or the App Engine Launcher to run in your local App Engine
  development environment.

To give your App Engine account access using a personal service account:
* Follow the instructions for local development.
* Create an App Engine instance.
* Update the end of the config.py file to use your private credentials.
* Update the included app.yaml file with the id of your App Engine instance.
  If your instance is at my-app.appspot.com, the id of the instance is my-app.
* Use appcfg.py or the App Engine Launcher to deploy your application to
  App Engine.

To give your App Engine account access using an App Engine service account:
* Go to your App Engine console (http://appengine.google.com) and choose the
  instance you want to authenticate.
* Look under application settings - you'll find a link under 'Administration'
  on the left hand side of the screen.
* Email the Service Account Name to your Google contact, who will whitelist
  your application.
* Update the included app.yaml file with the id of your App Engine instance.
* Use appcfg.py or the App Engine Launcher to deploy your application to
  App Engine.

Dependencies

oauth2client:
* hg clone https://code.google.com/p/google-api-python-client/
* mv google-api-python-client/oauth2client/ into the directory
  containing app.yaml

Earth Engine
* follow the instructions at:
  https://code.google.com/p/earthengine-api/source/checkout
* move ee into the directory containing app.yaml

httplib2
* hg clone https://code.google.com/p/httplib2/
* move httplib2/python2/httplib2 into the directory containing app.yaml

pycrypto:
* download from https://www.dlitz.net/software/pycrypto/
* python setup.py build
* python setup.py install
