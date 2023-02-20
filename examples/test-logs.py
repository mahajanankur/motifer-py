import os
import sys
sys.path.append('../')
from motifer import LogFactory
from innerlayer import innerFunction

def main():
    # Setup logging
    # factory = LogFactory(service="chatbot", log_level="debug", server= None, console_log_output="stdout", logfile_file="motifer.log")
    factory = LogFactory(service="chatbot", log_level="debug", server= None, console_log_output="stdout")
    logger = factory.initialize()
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