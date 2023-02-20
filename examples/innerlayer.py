import logging
logger = logging.getLogger("chatbot")
# from motifer import FlaskLogFactory
# logger = FlaskLogFactory.get_initialized_logger()

# Main function
def innerFunction():
    if (not logger):
        print("Failed to setup logging, aborting.")
        return 1

    # Log some messages
    logger.debug("inner debug")
    logger.info("inner Info message")
    logger.warning("inner Warning message")
    logger.error("inner Error message")
    logger.critical("inner Critical message")