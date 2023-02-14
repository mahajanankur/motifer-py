# import logging
import logging

# Main function
def innerFunction():
    logger = logging.getLogger()
    if (not logger):
        print("Failed to setup logging, aborting.")
        return 1

    # Log some messages
    logger.debug("inner debug")
    logger.info("inner Info message")
    logger.warning("inner Warning message")
    logger.error("inner Error message")
    logger.critical("inner Critical message")