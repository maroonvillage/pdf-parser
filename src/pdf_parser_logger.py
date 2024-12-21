import logging


# Create a custom logger
logger = logging.getLogger("pdf-extraction-logger")

# Set the logging level for the logger
logger.setLevel(logging.DEBUG)

# Create handlers
console_handler = logging.StreamHandler()
file_handler = logging.FileHandler("app.log")

# Set logging levels for handlers
#console_handler.setLevel(logging.WARNING)
# console_handler.setLevel(logging.ERROR)
# console_handler.setLevel(logging.INFO)
# console_handler.setLevel(logging.DEBUG)
#file_handler.setLevel(logging.CRITICAL)
#file_handler.setLevel(logging.INFO)
#file_handler.setLevel(logging.ERROR)



# Create formatters and add them to handlers
console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(console_format)
file_handler.setFormatter(file_format)

# Add handlers to the logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# Example log messages
# logger.debug("This is a debug message")
# logger.info("This is an info message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")
