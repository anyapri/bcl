import logging
import logging.handlers
import os
import sys
import time

package_name = "content-processing-model"
logger = logging.getLogger(package_name)
logger.setLevel(logging.DEBUG)

def set_logging(config):
    # set up logging
    global logger
    logger.handlers = []
    log_dir = config.log_dir
    os.makedirs(log_dir, exist_ok=True)

    # stream logging
    stream_handler = logging.StreamHandler(sys.stdout)
    if config.debug:
        stream_handler.setLevel(logging.DEBUG)
        stream_formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    else:
        stream_handler.setLevel(logging.INFO)
        stream_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    # file logging
    max_size = int(config.log_max_size) * 1024 * 1024
    log_path = os.path.join(config.log_dir, "{}.log".format(package_name))
    file_handler = logging.handlers.RotatingFileHandler(
        log_path, maxBytes=max_size, backupCount=config.log_counts
    )
    file_format_string = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_formatter = logging.Formatter(file_format_string, datefmt="%Y-%m-%d %H:%M:%S")
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

