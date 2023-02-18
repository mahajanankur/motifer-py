import sys, logging, json, uuid, time
from flask import g, request
from motifer.formatters import LogFormatter
from motifer.filters import RequestIdFilter
# logger = None

class LogFactory:
    service = None
    log_level = logging.INFO
    options = None
    server = None
    console_log_output = 'stdout'
    console_log_color = True
    logfile_file = None
    logfile_log_level = logging.INFO
    logfile_log_color = True
    log_line_template = '%(color_on)s[%(asctime)s] [%(service)s] [%(request_id)s] [%(levelname)-4s] [%(filename)s:%(lineno)d] %(message)s%(color_off)s'

    def __init__(self, service, log_level, server, **options):
        self.service = service or "service-name"
        self.log_level = log_level.upper()
        self.options = options
        self.console_log_output = options.get('console_log_output').lower() if (options is not None and options.get('console_log_output') is not None) else 'stdout'
        # self.console_log_color = True if (options is not None and options.get('console_log_color') is not None) else False
        self.logfile_file = options.get('logfile_file') if (options is not None and options.get('logfile_file') is not None) else None
        self.logfile_log_level = options.get('logfile_log_level').upper() if (options is not None and options.get('logfile_log_level') is not None) else logging.INFO
        self.logfile_log_color = True if (options is not None and options.get('logfile_log_color') is not None) else False
        # Change log level labels in all the formatters
        logging.addLevelName(logging.WARNING, "WARN")
        # logging.addLevelName(logging.CRITICAL, "CRIT")
        logger = logging.getLogger(self.service)
        if(server is not None):
            self.server = server
            @server.before_request
            def before_request():
                g.start = time.time()
                randomUid = str(uuid.uuid4())
                logger.info("Random UID generated before request {0}".format(randomUid))
                g.request_id = randomUid

            @server.after_request
            def after_request(response):
                responseTime = int((time.time() - g.start) * 1000)
                # TIMESTAMP_ISO [response] [REQUEST_ID] [APP_NAME] [LOG_LEVEL] [REQUEST_METHOD] [REQUEST_IP] [API_PATH] [RESPONSE_STATUS] [CONTENT_LENGTH] [RESPONSE_TIME] [USER_AGENT]
                logger.info("[response] [{REQUEST_METHOD}] [{REQUEST_IP}] [{API_PATH}] [{RESPONSE_STATUS}] [{CONTENT_LENGTH}] [{RESPONSE_TIME}] [{USER_AGENT}]".format(REQUEST_METHOD=request.method, REQUEST_IP=request.remote_addr, API_PATH=request.path, RESPONSE_STATUS=response.status_code, CONTENT_LENGTH=response.content_length, RESPONSE_TIME=responseTime, USER_AGENT=request.user_agent))
                return response

    # Get logger factory.
    def get_logger(self):
        # Create logger
        logger = logging.getLogger(self.service)
        # stop propagting to root logger
        logger.propagate = False
        # Set global log level to 'debug' (required for handler levels to work)
        logger.setLevel(logging.DEBUG)
        # https://stackoverflow.com/questions/30945460/formatting-flask-app-logs-in-json 
        logging.getLogger('gunicorn').propagate = False
        logging.getLogger('werkzeug').disabled = True
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