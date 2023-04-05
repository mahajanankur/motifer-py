# Motifer
[![PyPI](https://img.shields.io/pypi/v/motifer?logo=PyPI)](https://badge.fury.io/py/motifer)
![PyPI - Status](https://img.shields.io/pypi/status/motifer?logo=PyPI)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/motifer?logo=PyPI)
[![License](https://img.shields.io/badge/code%20license-Apache%20License%2C%202.0-lightgrey?logo=GitHub)](https://github.com/mahajanankur/motifer-py/blob/main/LICENSE)
[![Downloads](https://static.pepy.tech/badge/motifer)](https://pepy.tech/project/motifer)

Motifer is a generic logs pattern builder on top of Python logging. It covers multiple usecases as follows.

  - Log pattern validation.
  - Consistent log pattern across the application.
  - Logstash and Cloudtrail support.
  - Request and response logging with a **unique request id** for a request flow.

### Installation

Motifer requires [Python](https://www.python.org/) to run.

Install the dependencies and devDependencies and start the server.

```sh
$ pip install motifer
```
## Usage
The recommended way to use `motifer` is to create a logger. The simplest way to do this is using `LoggerFactory`. Please look in the example folder for further information.

### LoggerFactory
Initialize the `LoggerFactory` object once and use it in different Python files.
``` python
import logging
from motifer import LogFactory

factory = LogFactory(service="appname", log_level=logging.DEBUG)
logger = factory.initialize()

logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```
All log levels supported by [Python logging](https://docs.python.org/3/library/logging.html#logging-levels) are supported.

``` log
2023-02-20 23:05:25,876 [appname] [DEBUG] [test-logs.py:16] Debug message
2023-02-20 23:05:25,876 [appname] [INFO] [test-logs.py:17] Info message
2023-02-20 23:05:25,876 [appname] [WARN] [test-logs.py:18] Warning message
2023-02-20 23:05:25,876 [appname] [ERROR] [test-logs.py:19] Error message
2023-02-20 23:05:25,876 [appname] [CRITICAL] [test-logs.py:20] Critical message
2023-02-20 23:05:25,876 [appname] [ERROR] [test-logs.py:24] This is some exception
Traceback (most recent call last):
  File "test-logs.py", line 22, in main
    raise Exception("This is some exception")
Exception: This is some exception
2023-02-20 23:05:25,877 [appname] [DEBUG] [innerlayer.py:11] inner debug
2023-02-20 23:05:25,877 [appname] [INFO] [innerlayer.py:12] inner Info message
2023-02-20 23:05:25,877 [appname] [WARN] [innerlayer.py:13] inner Warning message
2023-02-20 23:05:25,877 [appname] [ERROR] [innerlayer.py:14] inner Error message
2023-02-20 23:05:25,877 [appname] [CRITICAL] [innerlayer.py:15] inner Critical message
```
---
### FlaskLogFactory
Initialize the `FlaskLogFactory` object once with flask server object and use it in different routes. Motifer supports `Flask version >= 2.0.1`.Please look in the example folder for further information.

##### index.py / app.py
``` python
import logging
from flask import Flask
from motifer import FlaskLogFactory

app = Flask(__name__)
factory = FlaskLogFactory(service="webappname", log_level=logging.DEBUG, server=app)
logger = factory.initialize()

def calculate():
    logger.error("Some error occured")
    return 10

@app.route('/')
def health():
    logger.debug("In the root route of sample app.")
    calculate()
    return {"status": "okay"}

if __name__ == '__main__':
    app.run()
```
> Request id is of `UUID V4` type.
``` log
2023-02-21 18:46:14,648 [request] [af7050bd-8f6a-4507-a8e3-1a327ef92d82] [webappname] [INFO] [flask_factory.py:40] [GET] [127.0.0.1] [/] [{'name': 'ankur', 'project': 'motifer'}]
2023-02-21 18:46:14,648 [service] [af7050bd-8f6a-4507-a8e3-1a327ef92d82] [webappname] [DEBUG] [index.py:15] In the root route of sample app.
2023-02-21 18:46:14,648 [service] [af7050bd-8f6a-4507-a8e3-1a327ef92d82] [webappname] [ERROR] [index.py:10] Some error occured
2023-02-21 18:46:14,649 [response] [af7050bd-8f6a-4507-a8e3-1a327ef92d82] [webappname] [INFO] [flask_factory.py:46] [GET] [127.0.0.1] [/] [200] [18] [1] [PostmanRuntime/7.29.2]
2023-02-21 18:46:16,339 [request] [e6a80807-6352-44bd-9765-c60e8b3b596a] [webappname] [INFO] [flask_factory.py:40] [GET] [127.0.0.1] [/] [{'name': 'xyz', 'project': 'motifer'}]
2023-02-21 18:46:16,339 [service] [e6a80807-6352-44bd-9765-c60e8b3b596a] [webappname] [DEBUG] [index.py:15] In the root route of sample app.
2023-02-21 18:46:16,339 [service] [e6a80807-6352-44bd-9765-c60e8b3b596a] [webappname] [ERROR] [index.py:10] Some error occured
2023-02-21 18:46:16,340 [response] [e6a80807-6352-44bd-9765-c60e8b3b596a] [webappname] [INFO] [flask_factory.py:46] [GET] [127.0.0.1] [/] [200] [18] [1] [PostmanRuntime/7.29.2]
```
---
### FastApiLogFactory
Initialize the `FastApiLogFactory` object once with fastapi app object and use it in different routes. Motifer supports `fastapi version >= 0.73.0`.Please look in the example folder for further information.

##### index.py / app.py
``` python
import logging, uvicorn
from fastapi import FastAPI
from motifer import FastApiLogFactory

app = FastAPI()
factory = FastApiLogFactory(service="webappname", log_level=logging.DEBUG, server=app)
logger = factory.initialize()

def calculate():
    logger.error("Some error occured")
    return 10

@app.get("/")
def health():
    logger.debug("In the root route of sample app.")
    calculate()
    return {"status": "okay"}

if __name__ == '__main__':
    uvicorn.run(app=app, host="0.0.0.0", port=8000, workers=1)
```
> Request id is of `UUID V4` type.
``` log
2023-02-21 18:46:14,648 [request] [af7050bd-8f6a-4507-a8e3-1a327ef92d82] [webappname] [INFO] [fast_api_factory.py:45] [GET] [127.0.0.1] [/] [{'name': 'ankur', 'project': 'motifer'}]
2023-02-21 18:46:14,648 [service] [af7050bd-8f6a-4507-a8e3-1a327ef92d82] [webappname] [DEBUG] [index.py:15] In the root route of sample app.
2023-02-21 18:46:14,648 [service] [af7050bd-8f6a-4507-a8e3-1a327ef92d82] [webappname] [ERROR] [index.py:10] Some error occured
2023-02-21 18:46:14,649 [response] [af7050bd-8f6a-4507-a8e3-1a327ef92d82] [webappname] [INFO] [fast_api_factory.py:48] [GET] [127.0.0.1] [/] [200] [18] [1] [PostmanRuntime/7.29.2]
2023-02-21 18:46:16,339 [request] [e6a80807-6352-44bd-9765-c60e8b3b596a] [webappname] [INFO] [fast_api_factory.py:45] [GET] [127.0.0.1] [/] [{'name': 'xyz', 'project': 'motifer'}]
2023-02-21 18:46:16,339 [service] [e6a80807-6352-44bd-9765-c60e8b3b596a] [webappname] [DEBUG] [index.py:15] In the root route of sample app.
2023-02-21 18:46:16,339 [service] [e6a80807-6352-44bd-9765-c60e8b3b596a] [webappname] [ERROR] [index.py:10] Some error occured
2023-02-21 18:46:16,340 [response] [e6a80807-6352-44bd-9765-c60e8b3b596a] [webappname] [INFO] [fast_api_factory.py:48] [GET] [127.0.0.1] [/] [200] [18] [1] [PostmanRuntime/7.29.2]
```
#### Log Patterns
##### Request Logs
``` log
TIMESTAMP_ISO [request] [REQUEST_ID] [APP_NAME] [LOG_LEVEL] [FILENAME] [REQUEST_METHOD] [REQUEST_IP] [API_PATH] [BODY]
```
##### Service Logs
``` log
TIMESTAMP_ISO [service] [REQUEST_ID] [APP_NAME] [LOG_LEVEL] [FILENAME] MULTI_OR_SINGLE_LINE_MESSAGE
```
##### Response Logs
``` log
TIMESTAMP_ISO [response] [REQUEST_ID] [APP_NAME] [LOG_LEVEL] [FILENAME] [REQUEST_METHOD] [REQUEST_IP] [API_PATH] [RESPONSE_STATUS] [CONTENT_LENGTH] [RESPONSE_TIME] [USER_AGENT] 
```
---
### LoggerFactory

The **object** has three parameter.

| Param | Description |Mandatory |Default |Comments|
| ------ | ------ | ------ | ------ | ------ |
| service | Application or service name. | Yes | NA| This is a mandatory param.|
| log_level | Log level for the application. | No | info| Info is default log level.|
| options | Array of objects for file appender and rotation. | No | null| If not supplied file appender will not be attached.|

### FlaskLogFactory

The **object** has four parameter.

| Param | Description |Mandatory |Default |Comments|
| ------ | ------ | ------ | ------ | ------ |
| service | Application or service name. | Yes | NA| This is a mandatory param.|
| log_level | Log level for the application. | Yes | NA| This is a mandatory param.|
| server | Flask object | Yes | NA| This is a mandatory param.|
| options | Array of objects for file appender and rotation. | No | null| If not supplied file appender will not be attached.|

### FastApiLogFactory

The **object** has four parameter.

| Param | Description |Mandatory |Default |Comments|
| ------ | ------ | ------ | ------ | ------ |
| service | Application or service name. | Yes | NA| This is a mandatory param.|
| log_level | Log level for the application. | Yes | NA| This is a mandatory param.|
| server | FastApi object | Yes | NA| This is a mandatory param.|
| options | Array of objects for file appender and rotation. | No | null| If not supplied file appender will not be attached.|
---
## Production Usecase
While WSGI can be useful during development and testing, it is generally not recommended for production use due to concerns related to scalability, security, performance, and configuration complexity. Instead, dedicated web servers such as Nginx or Apache should be used along with application servers like Gunicorn or Uvicorn for serving Python-based web applications in production environments.

To integrate `Motifer` with the internal logs of `gunicorn` and `uvicorn`, you can add `--log-config` to the command. To do so, you should first download the appropriate configuration files (for either [gunicorn_log.conf](https://github.com/mahajanankur/motifer-py/blob/main/gunicorn_log.conf) or [uvicorn_log.conf](https://github.com/mahajanankur/motifer-py/blob/main/uvicorn_log.conf)) and add them to either the config or root directory.

Gunicorn is a popular application server that is compatible with WSGI applications. To start a Gunicorn server, you can use the following command:
```sh
gunicorn flask-app:app --log-config gunicorn_log.conf
```
Uvicorn is an ASGI (Asynchronous Server Gateway Interface) server that is designed for high-performance web applications.
```sh
uvicorn fast-api-app:app --log-config uvicorn_log.conf
```
---
License
----
**Apache 2.0**