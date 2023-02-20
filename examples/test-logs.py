# No need to add sys in real implementations.
import sys
sys.path.append('../')
from motifer import LogFactory
from innerlayer import innerFunction

def main():
    # Setup logging
    factory = LogFactory(service="appname", log_level="debug", server= None, console_log_output="stdout")
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
    try:
        raise Exception("This is some exception")
    except Exception as e:
        logger.exception(e)

    innerFunction()

# Call main function
if (__name__ == "__main__"):
    sys.exit(main())