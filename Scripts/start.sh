#! /bin/sh
envsubst < redis_orig.json > redis.json
ls -la
cat redis.json
locust -f redis_get_set.py
