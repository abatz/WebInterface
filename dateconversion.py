import datetime

def dateString2pythondate(dateString):
	#andy_date = yyyy--mm--dd , you would convert it like this:

	yr = int(andy_date[0:4])
	mon = int(andy_date[5:7])
	day = int(andy_date[8:10])
	dt = datatime.datetime(yr,mon,day)
	return (dt);

