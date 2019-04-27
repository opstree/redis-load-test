#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a script to Get key in Redis Server for load testing.
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
        print(host, port)

    def query(self, key, command='GET'):
        """Function to put GET request on Redis"""
        result = None
        start_time = time.time()
        result = self.rc.get(key)
        total_time = int((time.time() - start_time) *1000000)
        if not result:
            result = ''
            events.request_failure.fire(request_type=command, name=key, response_time=total_time, exception="Error")
        else:
            length = len(result)
            events.request_success.fire(request_type=command, name=key, response_time=total_time, response_length=length)
        return result

class RedisLocust(Locust):
    def __init__(self, *args, **kwargs):
        super(RedisLocust, self).__init__(*args, **kwargs)
        self.client = RedisClient()
        self.key = 'key2'
        self.value = 'value2'

class RedisLua(RedisLocust):
    min_wait = 100
    max_wait = 100

    class task_set(TaskSet):
        @task(1)
        def get_time(self):
            self.client.query('key1')
