import logging

def setup_logging():
    #The logging configuration sets the logging level to INFO and specifies the format for log messages.
    #The format includes the timestamp, log level, and the actual log message.
    #Currently the pipeline doesn't using the logging module, but it is set up for future use.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s"
    )
