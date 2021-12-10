import logging
import os

loggers_dict = {}
# Logging
LOGLEVEL = 20  # logging.INFO
LOG_FORMAT = u"%(name)-20s %(levelname)-8s %(message)s"
FILE_LOGLEVEL = 10  # logging.DEBUG
FILE_LOG_FORMAT = u"%(asctime)s %(name)-20s %(levelname)-8s %(message)s"


# --- Logging utilities --------------------------------------------------------
def add_file_handler(logger, log_filepath, loglevel=FILE_LOGLEVEL, log_format=FILE_LOG_FORMAT):
    """Add a file handler to the logger."""
    file_handler = logging.FileHandler(log_filepath, encoding='utf-8')
    file_handler.setLevel(loglevel)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)


def setup_loggers(log_dir, save_log, loglevel=FILE_LOGLEVEL, log_format=FILE_LOG_FORMAT):
    """Setup the loggers with file handlers."""
    for name in logging.Logger.manager.loggerDict.keys():
        if name.startswith(save_log):
            add_file_handler(
                logging.getLogger(name), os.path.join(log_dir, name + '.log'),
                loglevel, log_format)
