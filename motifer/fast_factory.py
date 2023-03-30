import sys, logging, json, uuid, time, contextvars 
# from flask import g, request
from fastapi import Request
from motifer.formatters import LogFormatter
from motifer.fast_filters import FastRequestIdFilter
# logger = None

class FastApiLogFactory:
    service = None
    log_level = logging.INFO
    options = None
    server = None
    console_log_output = 'stdout'
    console_log_color = True
    logfile_file = None
    logfile_log_level = logging.INFO
    logfile_log_color = True
    log_line_template = '%(color_on)s%(asctime)s [%(log_type)s] [%(request_id)s] [%(service)s] [%(levelname)-4s] [%(filename)s:%(lineno)d] %(message)s%(color_off)s'
    # logger = None

    def __init__(self, service, log_level, server, **options):
        self.service = service or "service-name"
        # self.log_level = log_level.upper()
        self.log_level = log_level if(log_level is not None and type(log_level) is int) else logging.INFO
        self.options = options
        self.console_log_output = options.get('console_log_output').lower() if (options is not None and options.get('console_log_output') is not None) else 'stdout'
        # self.console_log_color = True if (options is not None and options.get('console_log_color') is not None) else False
        self.logfile_file = options.get('logfile_file') if (options is not None and options.get('logfile_file') is not None) else None
        self.logfile_log_level = options.get('logfile_log_level').upper() if (options is not None and options.get('logfile_log_level') is not None) else logging.INFO
        self.logfile_log_color = True if (options is not None and options.get('logfile_log_color') is not None) else False
        # Change log level labels in all the formatters
        logging.addLevelName(logging.WARNING, "WARN")
        # logging.addLevelName(logging.CRITICAL, "CRIT")
        self.logger = logging.getLogger(self.service)
        if server:
            self.server = server
            request_id_contextvar = contextvars.ContextVar("request_id", default=None)

            # @server.middleware("http")
            # async def before_request(request: Request, call_next):
            #     server.state.start_time = time.time()
            #     server.state.request_id = str(uuid.uuid4())
            #     try: 
            #         request_body_in = request.get_json() if(request is not None and request.is_json == True) else {}
            #         request_body = json.dumps(request_body_in) if request_body_in != {} else {}
            #         # Bugfix - If the content type is application/json in GET json decode exception occurs.
            #     except Exception as e:
            #         request_body = {}
            #     self.logger.info("[{REQUEST_METHOD}] [{REQUEST_IP}] [{API_PATH}] [{BODY}]".format(REQUEST_METHOD = request.method, REQUEST_IP=request.remote_addr, API_PATH=request.path, BODY=request_body))
            #     return call_next(request)

            @server.middleware("http")
            async def after_request(request: Request, call_next):
                request_id_contextvar.set(str(uuid.uuid4()))
                start_time = time.time()
                # request.state.request_id = str(uuid.uuid4())
                self.logger.info("[{REQUEST_METHOD}] [{REQUEST_IP}] [{API_PATH}] [{BODY}]".format(REQUEST_METHOD = request.method, REQUEST_IP=request.client.host, API_PATH=request.url.path, BODY={}))
                response_time = int((time.time() - start_time) * 1000)
                response = await call_next(request)
                self.logger.info("[{REQUEST_METHOD}] [{REQUEST_IP}] [{API_PATH}] [{RESPONSE_STATUS}] [{CONTENT_LENGTH}] [{RESPONSE_TIME}] [{USER_AGENT}]".format(REQUEST_METHOD=request.method, REQUEST_IP=request.client.host, API_PATH=request.url.path, RESPONSE_STATUS=response.status_code, CONTENT_LENGTH=response.headers["content-length"], RESPONSE_TIME=response_time, USER_AGENT=request.headers["user-agent"]))
                return response

    # Get logger factory.
    def initialize(self):
        # Create logger
        logger = logging.getLogger(self.service)
        # Bugfix - Multiple filters registered with multiple objects.
        if(logger.filters.__len__() == 1):
            return logger
        # stop propagting to root logger
        logger.propagate = False
        # Set global log level to 'debug' (required for handler levels to work)
        logger.setLevel(logging.DEBUG)
        # https://stackoverflow.com/questions/30945460/formatting-flask-app-logs-in-json 
        logging.getLogger('gunicorn').propagate = False
        # logging.getLogger('werkzeug').disabled = True
        self.__alter_werkzeug_logger()
        # Create console handler
        if (self.console_log_output == "stdout"):
            self.console_log_output = sys.stdout
        elif (self.console_log_output == "stderr"):
            self.console_log_output = sys.stderr
        else:
            print("Failed to set console output: invalid output: '%s'" % self.console_log_output)
            return False
        console_handler = logging.StreamHandler(self.console_log_output)
        # Set console log level
        try:
            console_handler.setLevel(self.log_level) # only accepts uppercase level names
        except:
            print("Failed to set console log level: invalid level: '%s'" % self.log_level)
            return False
            
        requestFilters = FastRequestIdFilter(server= self.server, service= self.service)
        logger.addFilter(requestFilters)
        # Create and set formatter, add console handler to logger
        console_formatter = LogFormatter(fmt=self.log_line_template, color=self.console_log_color)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        if(self.logfile_file is not None):
            # Create log file handler
            try:
                logfile_handler = logging.FileHandler(self.logfile_file)
            except Exception as exception:
                print("Failed to set up log file: %s" % str(exception))
                return False
            # Set log file log level
            try:
                logfile_handler.setLevel(self.logfile_log_level) # only accepts uppercase level names
            except:
                print("Failed to set log file log level: invalid level: '%s'" % self.logfile_log_level)
                return False
            # Create and set formatter, add log file handler to logger
            logfile_formatter = LogFormatter(fmt=self.log_line_template, color=self.logfile_log_color)
            logfile_handler.setFormatter(logfile_formatter)
            logger.addHandler(logfile_handler)
        return logger
    
    # @staticmethod
    # def get_initialized_logger():
    #     logger = logging.getLogger(FlaskLogFactory.service)
    #     if(logger is not None):
    #         return logger
    #     else:
    #         raise Exception("Logger factory is not initialized.")

    def __alter_werkzeug_logger(self):
        werkzeug = logging.getLogger('werkzeug')
        werkzeug.setLevel(logging.ERROR)
        # logging.getLogger('werkzeug').disabled = True
        console_handler = logging.StreamHandler(self.console_log_output)
        requestFilters = FastRequestIdFilter(server= self.server, service= self.service)
        werkzeug.addFilter(requestFilters)
        # Create and set formatter, add console handler to logger
        console_formatter = LogFormatter(fmt=self.log_line_template, color=self.console_log_color)
        console_handler.setFormatter(console_formatter)
        werkzeug.addHandler(console_handler)
        # if len(werkzeug.handlers) == 1:
        #     formatter = logging.Formatter(self.log_line_template)
        #     werkzeug.handlers[0].setFormatter(formatter)