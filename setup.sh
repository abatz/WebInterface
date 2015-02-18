#!/bin/sh

#these env variables must be set up to execute the statements below the line:
$HOME=
$MY_APP_ID='drought-monitor3'
$MY_SERVICE_ACCOUNT='your-service-account-id@developer.gserviceaccount.com'

#========MODIFY ONLY ABOVE THIS LINE===========

export APPENGINE_APP_ID=$MY_APP_ID
mv app.yaml app.yaml.bak
sed "s/<your-appid-here>/$APPENGINE_APP_ID/g" app.yaml.bak > app.yaml
ln -s $HOME/.keys/privatekey.pem privatekey.pem
mv config.py config.py.bak
sed "s/EE_ACCOUNT = 'your-service-account-id@developer.gserviceaccount.com'/EE_ACCOUNT = '$MY_SERVICE_ACCOUNT'/g" config.py.bak > config.py
#ln -s $HOME/anaconda/envs/ee-python/lib/python2.7/site-packages/ee ee
pip install earthengine-api --upgrade 
ln -s $HOME/anaconda/lib/python2.7/site-packages/ee
ln -s $HOME/anaconda/envs/ee-python/lib/python2.7/site-packages/oauth2client/ oauth2client
ln -s $HOME/anaconda/envs/ee-python/lib/python2.7/site-packages/six.py six.py
ln -s $HOME/anaconda/envs/ee-python/lib/python2.7/site-packages/httplib2 httplib2


