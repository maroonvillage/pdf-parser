import logging


def configure_logger(__name__):
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Set the logging level for the logger
    # logger.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    # logger.setLevel(logging.ERROR)
    # logger.setLevel(logging.WARNING)
    
    # Create handlers
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("app.log")

    # Create formatters and add them to handlers
    console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

