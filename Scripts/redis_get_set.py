#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a script to Get and Set key in Redis Server for load testing.
This script will use locust as framework.

Author:- OpsTree Solutions
"""

import json
import time
from locust import Locust, events
from locust.core import TaskSet, task
import redis
import gevent.monkey
gevent.monkey.patch_all()
from random import randint

def load_config(filepath):
    """For loading the connection details of Redis"""
    with open(filepath) as property_file:
        configs = json.load(property_file)
    return configs

filename = "redis.json"

configs = load_config(filename)

class RedisClient(object):
    def __init__(self, host=configs["redis_host"], port=configs["redis_port"]):
        self.rc = redis.StrictRedis(host=host, port=port)
    
    def query(self, key, command='GET'):
        """Function to Test GET operation on Redis"""
        result = None
        start_time = time.time()
        try:
            result = self.rc.get(key)
            if not result:
                result = ''
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type=command, name=key, response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(result)
            events.request_success.fire(request_type=command, name=key, response_time=total_time, response_length=length)
        return result

    def write(self, key, value, command='SET'):
        """Function to Test SET operation on Redis"""
        result = None
        start_time = time.time()
        try:
            result=self.rc.set(key,value)
            if not result:
                result = ''
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type=command, name=key, response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = 1
            events.request_success.fire(request_type=command, name=key, response_time=total_time, response_length=length)
        return result

class RedisLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(RedisLocust, self).__init__(*args, **kwargs)
        self.client = RedisClient()
        self.key = 'key1'
        self.value = 'value1'

class RedisLua(RedisLocust):
    min_wait = 100
    max_wait = 100

    class task_set(TaskSet):
        @task(2)
        def get_time(self):
            for i in range(100):
                self.key='key'+str(i)
                self.client.query(self.key)

        @task(1)
        def write(self):
            for i in range(100):
                self.key='key'+str(i)
                self.value='value'+str(i)
                self.client.write(self.key,self.value)

        @task(1)
        def get_key(self):
            var=str(randint(1,99))
            self.key='key'+var
            self.value='value'+var
