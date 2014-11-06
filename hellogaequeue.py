import os
import time
import webapp2
import jinja2
import json
from google.appengine.api import taskqueue

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
JINJA_ENV = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


myresults = []
myProgressValue = 0 #range[ 0, 100 ]


class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {'myresults': myresults, 'progressScriptActive':False}
        counter_template = JINJA_ENV.get_template('counter.html')
        self.response.out.write(counter_template.render(template_values))

    def post(self):
        key = self.request.get('key')
        # Add the task to the default queue.
        taskqueue.add(url='/worker', params={'key': key})

        template_values = {'myresults': myresults, 'progressScriptActive':True}
        counter_template = JINJA_ENV.get_template('counter.html')
        self.response.out.write(counter_template.render(template_values))


class TaskWorker(webapp2.RequestHandler):
    def post(self): 
        global myresults
        global myProgressValue

        key = self.request.get('key')
        for x in xrange(1, 11):
            time.sleep(1)
            res = x*int(key)
            myresults.append(str(res))
            myProgressValue = myProgressValue + 10


class ProgressWorker(webapp2.RequestHandler):
    def get(self):
        global myProgressValue

        json_result = json.dumps( myProgressValue )
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.response.out.write(json_result)


application = webapp2.WSGIApplication(
    [
        ('/', MainHandler),
        ('/worker', TaskWorker),
        ('/progress', ProgressWorker)
    ], debug=True)
