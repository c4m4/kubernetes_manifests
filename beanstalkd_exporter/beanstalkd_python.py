#!/usr/bin/env python

import sys
import time
import beanstalkc
from prometheus_client import Gauge, make_wsgi_app
from wsgiref.simple_server import make_server



if len(sys.argv[1:]) != 2:
  beanstalkd_host = "127.0.0.1"
  beanstalkd_port = 11300
else:
  beanstalkd_host = sys.argv[1]
  beanstalkd_port = sys.argv[2]

print "connecting to %s -> port %s" % (beanstalkd_host, beanstalkd_port)

beanstalk = beanstalkc.Connection(host=beanstalkd_host, port=int(beanstalkd_port))

def collect():
  data = {}
  mylist = []
  for tube in beanstalk.tubes():
    mydict = beanstalk.stats_tube(tube)
    for key in mydict.keys():
      newstr = "beanstalkd_" + tube + "_" + key.replace('-', '_')
      g = Gauge(newstr, tube + "_" + key)
      if not str(mydict[key]):
        g.set(mydict[key])

collect()
app = make_wsgi_app()
httpd = make_server('', 9095, app)
httpd.serve_forever()

