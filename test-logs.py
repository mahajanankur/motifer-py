# import logging
import os
import sys
from motifer import LogFactory
from testlogs2 import innerFunction

# logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-4.5s]  %(message)s")
# rootLogger = logging.getLogger()

# fileHandler = logging.FileHandler("{0}/{1}.log".format(os.getcwd(), "ankur"))
# fileHandler.setFormatter(logFormatter)
# rootLogger.addHandler(fileHandler)

# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# rootLogger.addHandler(consoleHandler)

# logging.debug('This is a debug message')
# logging.info('This is an info message')
# logging.warning('This is a warning message')
# logging.error('This is an error message')
# logging.critical('This is a critical message')

# Main function
def main():
    # Setup logging
    script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
    # factory = LogFactory(app=""console_log_output="stdout", console_log_level="warning", console_log_color=True, logfile_file=script_name + ".log", logfile_log_level="debug", logfile_log_color=False)
    factory = LogFactory(service="chatbot", log_level="debug", server= None, console_log_output="stdout", logfile_file="ankur.log")
    logger = factory.get_logger()
    if (not logger):
        print("Failed to setup logging, aborting.")
        return 1

    # Log some messages
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
    logger.critical("Critical message")
    innerFunction()

# Call main function
if (__name__ == "__main__"):
    sys.exit(main())