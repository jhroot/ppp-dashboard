import logging
import os


def logger(log_file=None, set_level="INFO", identity=""):
    """
    Create a logger, by specifying a unique (or same) logFile,
    set the level of logging, and optional identity for what is
    sending logging message, to identify multiple workers
    """
    logger = logging.getLogger('myapp')
    if log_file:
        hdlr = logging.FileHandler(os.getcwd() + os.sep + log_file)
    else:
        # No log file provided, use the stream handler
        hdlr = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(levelname)s ' + identity + ' %(message)s', '%Y-%m-%dT%H:%M:%SZ')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(eval("logging." + set_level))
    return logger
