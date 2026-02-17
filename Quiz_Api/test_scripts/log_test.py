from loggers.logger import logger

def example_function():
    logger.debug("This is a debug message")
    logger.info("This is info")
    logger.warning("A warning!")
    logger.error("An error occurred")
    logger.critical("Critical issue!")

example_function()
