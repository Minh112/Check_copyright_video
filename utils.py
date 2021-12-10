import requests
import logging
import os


def post_to_server(video_title, accuracy, warning):
    # http://183.81.35.24:5010/api/msg_warning/Update?title=Em giờ nơi ấy có ổn không ? Em ừ đi anh thấy yên lòng ~ huy Vạc cover hay nhất 2019&accuracy=10&timer=12
    headers = {'content-type': 'application/json'}
    url = 'http://183.81.35.24:5010/api/msg_warning/Update'
    params = {'title': video_title, 'accuracy': accuracy, 'timer': '0', 'warning': warning}
    print(params)
    # req = requests.post(url, params=params, headers=headers)


loggers_dict = {}
# Logging
LOGLEVEL = 20  # logging.INFO
LOG_FORMAT = "%(name)-20s %(levelname)-8s %(message)s"
FILE_LOGLEVEL = 10  # logging.DEBUG
FILE_LOG_FORMAT = "%(asctime)s %(name)-20s %(levelname)-8s %(message)s"


# --- Logging utilities --------------------------------------------------------
def add_file_handler(logger, log_filepath, loglevel=FILE_LOGLEVEL,
                     log_format=FILE_LOG_FORMAT):
    """Add a file handler to the logger."""
    file_handler = logging.FileHandler(log_filepath)
    file_handler.setLevel(loglevel)
    file_handler.setFormatter(logging.Formatter(log_format))
    logger.addHandler(file_handler)


def setup_loggers(log_dir, loglevel=FILE_LOGLEVEL, log_format=FILE_LOG_FORMAT):
    """Setup the loggers with file handlers."""
    for name in logging.Logger.manager.loggerDict.keys():
        if name.startswith('music'):
            add_file_handler(
                logging.getLogger(name), os.path.join(log_dir, name + '.log'),
                loglevel, log_format)
