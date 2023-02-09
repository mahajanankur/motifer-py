import os
import sys
import logging

# Logging formatter supporting colorized output
class LogFormatter(logging.Formatter):

    COLOR_CODES = {
        logging.CRITICAL: "\033[1;35m", # bright/bold magenta
        logging.ERROR:    "\033[1;31m", # bright/bold red
        logging.WARNING:  "\033[1;33m", # bright/bold yellow
        logging.INFO:     "\033[0;37m", # white / light gray
        logging.DEBUG:    "\033[1;30m"  # bright/bold black / dark gray
    }

    RESET_CODE = "\033[0m"

    def __init__(self, color, *args, **kwargs):
        super(LogFormatter, self).__init__(*args, **kwargs)
        self.color = color

    def format(self, record, *args, **kwargs):
        if (self.color == True and record.levelno in self.COLOR_CODES):
            record.color_on  = self.COLOR_CODES[record.levelno]
            record.color_off = self.RESET_CODE
        else:
            record.color_on  = ""
            record.color_off = ""
        return super(LogFormatter, self).format(record, *args, **kwargs)

class LogFactory:
    console_log_output = None
    console_log_level = None
    console_log_color = None
    logfile_file = None
    logfile_log_level = None
    logfile_log_color = None
    log_line_template = None

    def __init__(self, console_log_output, console_log_level, console_log_color, logfile_file, logfile_log_level, logfile_log_color, log_line_template):
        self.console_log_output = console_log_output.lower()
        self.console_log_level = console_log_level.upper()
        self.console_log_color = console_log_color
        self.logfile_file = logfile_file
        self.logfile_log_level = logfile_log_level.upper()
        self.logfile_log_color = logfile_log_color
        self.log_line_template = log_line_template

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
            console_handler.setLevel(self.console_log_level) # only accepts uppercase level names
        except:
            print("Failed to set console log level: invalid level: '%s'" % self.console_log_level)
            return False

        # Create and set formatter, add console handler to logger
        console_formatter = LogFormatter(fmt=self.log_line_template, color=self.console_log_color)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

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