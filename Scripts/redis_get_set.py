#!/usr/bin/python3
## pylint: disable = invalid-name, too-few-public-methods
"""
This is a script to Get and Set key in Redis Server for load testing.
This script will use locust as framework.

Author:- OpsTree Solutions
Edited by: zviedris
"""

from random import randint
import json
import time
from locust import User, events, TaskSet, task, constant
import redis
import string
import random
import gevent.monkey
gevent.monkey.patch_all()


def load_config(filepath):
    """For loading the connection details of Redis"""
    with open(filepath) as property_file:
        configs = json.load(property_file)
    return configs

def randStr(chars = string.ascii_uppercase + string.digits, N=10):
    return ''.join(random.choice(chars) for _ in range(N))

filename = "redis.json"
configs = load_config(filename)


class RedisClient(object):
    def __init__(self, host=configs["redis_host"], port=configs["redis_port"], password=configs["redis_password"]):
        self.rc = redis.StrictRedis(host=host, port=port, password=password)
        self.errorTime = configs["error_timeout"]
        self.expirationTime = configs["expire_seconds"]

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
            events.request_failure.fire(
                request_type=command, name="get", response_time=total_time, response_length=1, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(result)
            if self.errorTime > 0 and total_time > self.errorTime:
                events.request_failure.fire(
                    request_type=command, name="get", response_time=total_time, response_length=length, exception="timeout exception")            
            else:
                events.request_success.fire(
                    request_type=command, name="get", response_time=total_time, response_length=length)
        return result

    def write(self, key, value, command='SET'):
        """Function to Test SET operation on Redis"""
        result = None
        start_time = time.time()
        try:
            if self.expirationTime > 0:
                result = self.rc.set(key, value, self.expirationTime)
            else:
                result = self.rc.set(key, value)
            if not result:
                result = ''
        except Exception as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(
                request_type=command, name="set", response_time=total_time, response_length=1, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            length = len(value)
            #if time is greater than normal timeout - it is registred as timeout
            if self.errorTime > 0 and total_time > self.errorTime:
                events.request_failure.fire(
                    request_type=command, name="set", response_time=total_time, response_length=length, exception="timeout exception")            
            else:
                events.request_success.fire(
                    request_type=command, name="set", response_time=total_time, response_length=length)
        return result


class RedisLocust(User):
    wait_time = constant(0.1)
    key_range = configs["key_range"]
    key_length = configs["key_length"]

    def __init__(self, *args, **kwargs):
        super(RedisLocust, self).__init__(*args, **kwargs)
        self.client = RedisClient()
        self.key = 'key1'
        self.value = 'value1'

    #get task - get one random key
    @task(configs["get_int"])
    def get_time(self):
        i = randint(1, self.key_range-1)
        self.key = 'key'+str(i)
        self.client.query(self.key)

    #set task - set one random key
    @task(configs["set_int"])
    def write(self):
        i = randint(1, self.key_range-1)
        self.key = 'key'+str(i)
        self.value = randStr(N=self.key_length)
        self.client.write(self.key, self.value)
