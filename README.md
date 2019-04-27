# Redis Performance Testing - A OpsTree utility to test load on Redis

This main goal of creating this utility is to provide easy and fast performance testing for Redis.

## Dependencies

The list of dependencies are not quite long but yes we do have some dependencies.

#### System Dependencies
- [X] **python3**

#### Python Dependencies
- [X] **locust**
- [X] **json**
- [X] **argparse**
- [X] **redis**

Don't worry we have taken care the python dependencies in [requirments.txt](./Scripts/requirments.txt)

## Overview of Utility Structure

In this repository we have:-
- **Scripts**:- Scripts folder contains all the codebase which is required for performance testing.
    - **[redis_set.py](./Scripts/redis_set.py)**:- This script is used to set random keys in Redis.
    - **[redis_read.py](./Scripts/redis_read.py)**:- This script is used to perform *GET* action on Redis.
    - **[redis_get_set.py](./Scripts/redis_get_set.py)**: This script is used to perform *SET* and *GET* operation simultaneously on Redis.
    - **[redis.json](./Scripts/redis.json)**:- This is a json file in which we have to define our connection details of Redis. I created this file because I believe that code should not be changed.

- **Results**:- This is a directory in which I am dumping some of my test results.
    - **[redis_get_1000_users_stats.md](./Results/mardownResults/redis_get_1000_users_stats.md)**:- This is a test result of *GET* operation with 1000 users.
    - **[redis_get_set_100_users_stats.md](./Results/mardownResults/redis_get_set_100_users_stats.md)**:- This is a test result of *GET* and *SET* operation simultaneously with 100 users.

You may need to install python3 manually, for other things you can use **[requirments.txt](./Scripts/requirments.txt)**

```shell
cd Scripts
pip3 install -r requirments.txt
```

## Usage

The use of this utility is not a fancy thing, just need to update the **[redis.json](./Scripts/redis.json)** with your redis connection details. Content of file should be like this:-

```json
{
    "redis_host": "18.215.118.208",
    "redis_port": "6379",
    "redis_password": ""
}
```

#### For SET Operation in Redis

```shell
./redis_set.py --filepath redis.json
```

#### For GET Operation in Redis

```shell
locust -f redis_read.py
```

#### For GET and SET simultaneously operation in Redis

```shell
locust -f redis_get_set.py
```
