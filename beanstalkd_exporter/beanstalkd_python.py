#!/usr/bin/env python

import time
import random
import sys
import time
import beanstalkc
from prometheus_client import Metric, REGISTRY, CollectorRegistry, start_http_server

if len(sys.argv[1:]) != 2:
  beanstalkd_host = "127.0.0.1"
  beanstalkd_port = 11300
else:
  beanstalkd_host = sys.argv[1]
  beanstalkd_port = sys.argv[2]

print "connecting to %s -> port %s" % (beanstalkd_host, beanstalkd_port)

registry = CollectorRegistry()

class MetricCollector(object):
  def __init__(self):
    pass

  def collect(self):
    beanstalk = beanstalkc.Connection(host=beanstalkd_host, port=int(beanstalkd_port))
    data = {}
    mylist = []
    for tube in beanstalk.tubes():
      mydict = beanstalk.stats_tube(tube)
      for key in mydict.keys():
        newstr = "beanstalkd_" + key.replace('-', '_')
        metric = Metric(newstr, newstr, 'gauge')
        if not type(mydict[key]) == str:
          metric.add_sample(newstr, value=mydict[key], labels={'queue': tube})
          yield metric


if __name__ == '__main__':
  start_http_server(9095)
  REGISTRY.register(MetricCollector())
  while True:
    time.sleep(3)

