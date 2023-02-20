# Motifer

Motifer is a generic logs pattern builder on top of Python logging. It covers multiple usecases as follows.

  - Log pattern validation.
  - Consistent log pattern across the application.
  - Logstash and Cloudtrail support.
  - Request and response logging with a **unique request id** for a request flow.

### Installation

Motifer requires [Python](https://www.python.org/) to run.

Install the dependencies and devDependencies and start the server.

```sh
$ pip3 install motifer
```
## Usage
The recommended way to use `motifer` is to create a logger. The simplest way to do this is using `LoggerFactory`.
### LoggerFactory
Initialize the `LoggerFactory` object once and use it in different Python files.
``` python
from motifer import LogFactory

factory = LogFactory(service="appname", log_level="debug")
logger = factory.initialize()
logger.debug("Debug message")
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
Initialize the `FlaskLogFactory` object once with flask server object and use it in different routes.
##### index.py / app.py
``` python
from flask import Flask
from motifer import FlaskLogFactory

app = Flask(__name__)
factory = FlaskLogFactory(service="webappname", log_level="debug", server=app)
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
2023-02-20 23:16:48,563 [webappname] [a6df150a-1fcd-4fb0-a915-a13d1dac24bd] [INFO] [flask_factory.py:40] [request] [GET] [127.0.0.1] [/] [ImmutableMultiDict([])]
2023-02-20 23:16:48,563 [webappname] [a6df150a-1fcd-4fb0-a915-a13d1dac24bd] [DEBUG] [flask-runner-copy.py:17] In the root route of sample app.
2023-02-20 23:16:48,564 [webappname] [a6df150a-1fcd-4fb0-a915-a13d1dac24bd] [ERROR] [flask-runner-copy.py:12] Some error occured
2023-02-20 23:16:48,565 [webappname] [a6df150a-1fcd-4fb0-a915-a13d1dac24bd] [INFO] [flask_factory.py:46] [response] [GET] [127.0.0.1] [/] [200] [18] [2] [Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36]
2023-02-20 23:17:16,299 [webappname] [f0bb5f15-40a2-4c66-93e0-6b7710021ae4] [INFO] [flask_factory.py:40] [request] [GET] [127.0.0.1] [/] [ImmutableMultiDict([])]
2023-02-20 23:17:16,300 [webappname] [f0bb5f15-40a2-4c66-93e0-6b7710021ae4] [DEBUG] [flask-runner-copy.py:17] In the root route of sample app.
2023-02-20 23:17:16,301 [webappname] [f0bb5f15-40a2-4c66-93e0-6b7710021ae4] [ERROR] [flask-runner-copy.py:12] Some error occured
2023-02-20 23:17:16,301 [webappname] [f0bb5f15-40a2-4c66-93e0-6b7710021ae4] [INFO] [flask_factory.py:46] [response] [GET] [127.0.0.1] [/] [200] [18] [3] [Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36]
```

#### Log Patterns
##### Request Logs
``` log
TIMESTAMP_ISO [request] [REQUEST_ID] [APP_NAME] [LOG_LEVEL] [REQUEST_METHOD] [REQUEST_IP] [API_PATH] [BODY]
```
##### Service Logs
``` log
TIMESTAMP_ISO [service] [REQUEST_ID] [APP_NAME] [LOG_LEVEL] [FILENAME] MULTI_OR_SINGLE_LINE_MESSAGE
```
##### Response Logs
``` log
TIMESTAMP_ISO [response] [REQUEST_ID] [APP_NAME] [LOG_LEVEL] [REQUEST_METHOD] [REQUEST_IP] [API_PATH] [RESPONSE_STATUS] [CONTENT_LENGTH] [RESPONSE_TIME] [USER_AGENT] 
```
---
### LoggerFactory

The **object** has three parameter.

| Param | Description |Mandatory |Default |Comments|
| ------ | ------ | ------ | ------ | ------ |
| service | Application or service name. | Yes | NA| This is a mandatory param.|
| level | Log level for the application. | No | info| Info is default log level.|
| options | Array of objects for file appender and rotation. | No | null| If not supplied file appender will not be attached.|

### FlaskLogFactory

The **object** has four parameter.

| Param | Description |Mandatory |Default |Comments|
| ------ | ------ | ------ | ------ | ------ |
| service | Application or service name. | Yes | NA| This is a mandatory param.|
| level | Log level for the application. | Yes | NA| This is a mandatory param.|
| server | Flask object | Yes | NA| This is a mandatory param.|
| options | Array of objects for file appender and rotation. | No | null| If not supplied file appender will not be attached.|

---
License
----
**Apache 2.0**

**Free Software, Hell Yeah!**