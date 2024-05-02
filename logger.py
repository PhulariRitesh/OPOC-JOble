# logger.py

import logging

# Create a logger object
logger = logging.getLogger("scrapper")

# Set the log level to INFO
logger.setLevel(logging.INFO)

# Create a file handler
# file_handler = logging.FileHandler('app.log')

# Create a stream handler
stream_handler = logging.StreamHandler()

# Create a formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the handlers
# file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
# logger.addHandler(file_handler)
logger.addHandler(stream_handler)
