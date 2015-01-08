# Google Drought

Code repository for the Google Drought web interface and tool under development by the Desert Research Institute, Google, and the University of Idaho.

You can find the most up-to-date deployments [here] (http://drought-monitor.appspot.com/) and [here] (http://gd-britta.appspot.com/).

### Links & Resources
- [DRI landing page] (http://www.dri.edu/google-drought)
- [Britta's page] (http://wrcc.dri.edu/csc/documentation/ee/set_up/)
- [Earth Engine Documentation] (https://sites.google.com/site/earthengineapidocs/)
- [Earth Engine Access Library] (https://code.google.com/p/earthengine-api/wiki/Installation)
- [Earth Engine Playground] (https://ee-api.appspot.com/)
- [Google Cloud Platform] (https://cloud.google.com/appengine/docs/python/gettingstartedpython27/helloworld)
- [Google Python Style Guide] (https://google-styleguide.googlecode.com/svn/trunk/pyguide.html)
- [Google Maps Javascript API v3] (https://developers.google.com/maps/documentation/javascript/)

### General Git Instructions:
- Working with the centralized repo:
	- `git clone https://github.com/Google-Drought/WebInterface directory_name`
	- `git remote rename original-name new-name`
	- Make symbolic links to Anaconda environment packages:
		- `ln -s $HOME/anaconda/envs/ee-python/lib/python2.7/site-packages/ee ee`
		- `ln -s $HOME/anaconda/envs/ee-python/lib/python2.7/site-packages/oauth2client/ oauth2client`
		- `ln -s $HOME/anaconda/envs/ee-python/lib/python2.7/site-packages/six.py six.py`
		- `ln -s $HOME/anaconda/envs/ee-python/lib/python2.7/site-packages/httplib2 httplib2`
	- Make symbolic link to private key:
		- `ln -s ~/.keys/privatekey.pem`
	- Set Developer information:
		- `app-id` in app.yaml
		- `x@developer.gserviceaccount.com` in config.py
	- `git branch` to look at branches.
	- `git branch -b branch-name` to create and switch to new local branch for working on feature.
	- `git add` to stage files and `git commit` to commit to feature branch.
	- `git checkout development` to switch back to development branch.
	- `git merge branch-name` to merge `branch-name` into the current branch.
	- `git push remote-name development`

### Installing & Running Google Earth Engine Python API
- Links:
	- https://docs.google.com/document/d/1tvkSGb-49YlSqW3AGknr7T_xoRB1KngCD3f2uiwOS3Q/edit
- Installation:
	- Download Anaconda with Python 2.7 and install.
	- To remove environment: `conda remove -n myenv --all` where `myenv` is environment name.
	- To create environment: `conda create -n ee-python python=2.7`
	- Activate environment: `source activate ee-python`
	- Install packages:
		- `conda install pycrypto`
		- `conda install pip`
		- `conda install numpy`
		- `pip install oauth2client`
		- `pip install --no-deps earthengine-api`
	- To test installation and authentication:
		- `python -c "import ee; print ee.__version__"`
		- `python -c "import os; import ee; MY_SERVICE_ACCOUNT = os.environ.get('MY_SERVICE_ACCOUNT'); MY_PRIVATE_KEY_FILE = os.environ.get('MY_PRIVATE_KEY_FILE'); ee.Initialize(ee.ServiceAccountCredentials(MY_SERVICE_ACCOUNT, MY_PRIVATE_KEY_FILE)); print(ee.Image('srtm90_v4').getThumbUrl())"`
- Configuring App Engine to use conda Environment:
	- Install Google App Engine for Python and clone Earth Engine API repository.
	- `~/Development/google_appengine/dev_appserver.py .`



### Repository Organization:
- app.yaml (configuration file for webapp2 templating)
- main.py (python script that sets up the framework environment and defines classes for handling URL requests)
- main.py (python script that sets up the framework environment and defines classes for handling URL requests)
- forms.py (python script which defines the dictionaries for the forms on the DroughtTool interface)
- collectionMethods.py (python script of methods for extracting and filtering) 
- media
	- css (css webpage styling formats (uses Twitter-Bootstrap web framework))
	- js (bootstrap and jQuery javascript functions)
	- myjs (javascript functions written specifically for this project)
	- showLoadingImage.js (javascript function responsive for the progress bar display)
	- formListener.js (javascript functions for listening for events on the forms of the DrougthTool Interface)
	- get_colorbar.js (functions for inserting the colorbar below the google maps)
	- get_colorbar_url.php
	- graph_utils.js (javascript functions for making graphs/charts (not currently working))
- templates
	- base.php (php file for base web template for the look of the webpage)
	- home.html (html file of structure of the home page)
	- aboutdata.html (html file of structure of the aboutData page)
	- aboutmetrics.html (html file of structure of the aboutMetrics page)
	- contact.html (html file of structure of the Contact page)
	- droughttool.php (php file for structure of the Drought Tool page)
	- descriptions (directory of page descriptions for aboutData and aboutMetrics and home page)
	- images (directory of images)
	- includes (directory of html/php files that have been included from the other page templates)
		- head.html (html file for html head inclusions (i.e. css))
		- footer.html (html file of footer bling)
		- basicscripts.php (php file of scripts included in template page (i.e. jQuery, Bootstrap))
		- scripts.php (php file of scripts included just for the Drought Tool page (i.e. javascript functions,etc))
		- navigation.html (html file for the main navigation tab on page)
		- dataform.html (html file for the data options forms on the webpage (includes basic/advanced forms))
		- mapfiguredata.html (html file for the portion of the page that has map/figure/data)
		- basicdataform.html (html file for the basic dataform)
		- advanceddataform.html (html file for the basic dataform(not currently being used))
		- map.html (html file for the MAP portion of the webpage)
		- datatab.html (html file for the DATA tab on webpage)
		- figuretab.html (html file for the FIGURE tab on webpage)

