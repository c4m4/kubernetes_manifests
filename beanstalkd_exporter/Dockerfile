FROM python:2.7.15-alpine3.6

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY beanstalkd_python.py /usr/bin
RUN chmod +x /usr/bin/beanstalkd_python.py
CMD 'beanstalkd_python.py'
