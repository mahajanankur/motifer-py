import sys, logging, json, uuid
from flask import g
from motifer.formatters import LogFormatter
from motifer.filters import RequestIdFilter

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
        # options = json.loads(json.dumps(props))
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
        if(server is not None):
            self.server = server
            @server.before_request
            def before_request():
                # g.request_id = request.headers.get('X-Request-Id', str(uuid.uuid4())
                randUid = str(uuid.uuid4())
                print("Random UID generated before request", randUid)
                g.request_id = randUid


    # Get logger factory.
    def get_logger(self):
        # Create logger
        # For simplicity, we use the root logger, i.e. call 'logging.getLogger()'
        # without name argument. This way we can simply use module methods for
        # for logging throughout the script. An alternative would be exporting
        # the logger, i.e. 'global logger; logger = logging.getLogger("<name>")'
        logger = logging.getLogger()

        # Set global log level to 'debug' (required for handler levels to work)
        logger.setLevel(logging.DEBUG)

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
        # If server object is not null.
        if(self.server is not None):
            # appServer = self.server
            handler = logging.StreamHandler(sys.stdout)
            logger.addHandler(handler)
        #     @apServer.before_request
        #     def before_request():
        #         print('before req')
            
        #     @apServer.after_request
        #     def after_request(response):
        #         print('after response')
        #         return response
        #     return
        # Add custom variables

        # customField = {'service': self.service}
        # logger = logging.LoggerAdapter(logger, customField)
        
        
        return logger