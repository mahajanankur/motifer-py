import sys, logging, json, uuid, time
from flask import g, request
from motifer.formatters import LogFormatter
from motifer.filters import RequestIdFilter
# logger = None

class FlaskLogFactory:
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
        if(server is not None):
            self.server = server
            @server.before_request
            def __motifer_before_request__():
                g.start_time = time.time()
                g.request_id = str(uuid.uuid4())
                try:
                    request_body_in = request.get_json() if(request is not None and request.is_json == True) else {}
                    request_body = json.dumps(request_body_in) if request_body_in != {} else {}
                    # Bugfix - If the content type is application/json in GET json decode exception occurs.
                except Exception as e:
                    request_body = {}
                self.logger.info("[{REQUEST_METHOD}] [{REQUEST_IP}] [{API_PATH}] [{BODY}]".format(REQUEST_METHOD = request.method, REQUEST_IP=request.remote_addr, API_PATH=request.path, BODY=request_body))

            @server.after_request
            def __motifer_after_request__(response):
                response_time = int((time.time() - g.start_time) * 1000)
                self.logger.info("[{REQUEST_METHOD}] [{REQUEST_IP}] [{API_PATH}] [{RESPONSE_STATUS}] [{CONTENT_LENGTH}] [{RESPONSE_TIME}] [{USER_AGENT}]".format(REQUEST_METHOD=request.method, REQUEST_IP=request.remote_addr, API_PATH=request.path, RESPONSE_STATUS=response.status_code, CONTENT_LENGTH=response.content_length, RESPONSE_TIME=response_time, USER_AGENT=request.user_agent))
                return response

    # Get logger factory.
    def initialize(self):
        # Create logger
        logger = logging.getLogger(self.service)
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
            
        requestFilters = RequestIdFilter(server= self.server, service= self.service)
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
        requestFilters = RequestIdFilter(server= self.server, service= self.service)
        werkzeug.addFilter(requestFilters)
        # Create and set formatter, add console handler to logger
        console_formatter = LogFormatter(fmt=self.log_line_template, color=self.console_log_color)
        console_handler.setFormatter(console_formatter)
        werkzeug.addHandler(console_handler)
        # if len(werkzeug.handlers) == 1:
        #     formatter = logging.Formatter(self.log_line_template)
        #     werkzeug.handlers[0].setFormatter(formatter)