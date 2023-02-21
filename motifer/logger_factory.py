import sys, logging
from motifer.formatters import LogFormatter
from motifer.filters import RequestIdFilter

class LogFactory:
    service = None
    log_level = logging.INFO
    options = None
    console_log_output = 'stdout'
    console_log_color = True
    logfile_file = None
    logfile_log_level = logging.INFO
    logfile_log_color = True
    log_line_template = '%(color_on)s%(asctime)s [%(service)s] [%(levelname)-4s] [%(filename)s:%(lineno)d] %(message)s%(color_off)s'

    def __init__(self, service, log_level, **options):
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
        logger = logging.getLogger(self.service)
  
    # Get logger factory.
    def initialize(self):
        # Create logger
        logger = logging.getLogger(self.service)
        # stop propagting to root logger
        logger.propagate = False
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
            
        # Create and set formatter, add console handler to logger
        console_formatter = LogFormatter(fmt=self.log_line_template, color=self.console_log_color)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        requestFilters = RequestIdFilter(server= None, service= self.service)
        logger.addFilter(requestFilters)
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
        # Add custom variables
        # customField = {'service': self.service}
        # logger = logging.LoggerAdapter(logger, customField)
        return logger