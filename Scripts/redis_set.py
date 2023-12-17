#!/usr/bin/python3
## pylint: disable = invalid-name
"""
This is a script to set key in Redis Server for load testing.

Author:- OpsTree Solutions
"""

import argparse
import json
from rediscluster import RedisCluster

def load_config(filepath):
    """For loading the connection details of Redis"""
    with open(filepath) as property_file:
        configs = json.load(property_file)
    return configs

def redis_populate(filepath):
    """Function to populate keys in Redis Server"""
    configs = load_config(filepath)
    startup_nodes = [{"host": configs["redis_host"], "port": configs["redis_port"]}]
    rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    for i in range(100000):
        key='key'+str(i)
        value='value'+str(i)
        rc.set(key,value)
        print(key,value)

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Redis Performance Testing")
    parser.add_argument("--filepath", help="Path of the Json File(Default is redis.json)")
    redis_populate("redis.json")
