"""
Used to create loggers for modules within the namespace.
These loggers are the standard python.logging loggers which can be adapted/changed via the standard methods.
"""

import logging
import logging.handlers
import os

from directories import LOG_DIR

# Default logging format
FUNSPACE_LOG_FORMAT = '%(asctime)s %(name)s %(levelname)s: %(message)s'
DEFAULT_LOG_FORMATTER = logging.Formatter(FUNSPACE_LOG_FORMAT)
DEFAULT_MAX_BYTES = 1000000
DEFAULT_MAX_BACKUPS = 5

# Create the log directory if it does not exist yet -raise error if unable
try:
    os.makedirs(LOG_DIR, exist_ok=True)
except OSError:
    raise


def get_stream_handler(log_format: str = FUNSPACE_LOG_FORMAT):
    handler = logging.StreamHandler()
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    return handler


def _get_file_handler(file_path: str, log_format: str = FUNSPACE_LOG_FORMAT):
    handler = logging.FileHandler(filename=file_path)
    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    return handler


def _get_rotating_file_handler(
        file_path: str,
        log_format: str = FUNSPACE_LOG_FORMAT,
        max_bytes: int = DEFAULT_MAX_BYTES,
        backup_count: int = DEFAULT_MAX_BACKUPS):
    handler = logging.handlers.RotatingFileHandler(filename=file_path,
                                                   maxBytes=max_bytes,
                                                   backupCount=backup_count)

    formatter = logging.Formatter(log_format)
    handler.setFormatter(formatter)
    return handler


def get_file_logger(name: str,
                    file_path: str = None,
                    log_level=logging.DEBUG,
                    log_format: str = FUNSPACE_LOG_FORMAT):
    """
    Return a logger for the specific file name and path.

    :param name: Name of the logger, depending on where the method was called from
    :param file_path: filepath to log into
    :param log_level: log level (INFO, DEBUG, etc.), defaults at DEBUG
    :param log_format: format to log - defaults at time, name, level, message
    :return: Logger setup
    """

    if file_path is None:
        file_path = os.path.join(LOG_DIR, f'{name}.log')

    # Get the logger from the logging module
    logger = logging.getLogger(name=name)
    handler = _get_file_handler(file_path=file_path, log_format=log_format)

    # Clear existing handler and create a new one
    logger.handlers.clear()

    # Add the handler and set its default level
    logger.addHandler(handler)
    logger.setLevel(log_level)

    return logger


def get_stream_and_file_logger(
        name: str,
        log_dir: str = LOG_DIR,
        log_format: str = FUNSPACE_LOG_FORMAT,
        overall_log_level: int = logging.DEBUG,
        stream_log_level: int = logging.DEBUG,
        file_log_level: int = logging.DEBUG,
        file_max_bytes: int = DEFAULT_MAX_BYTES,
        file_backup_count: int = DEFAULT_MAX_BACKUPS) -> logging.Logger:
    """
    Wrapper to use for Loggers creation.
    The Loggers will handle logs to both stream and Rotating File handlers. By default, only the name is required,
    multiple options are available in order to allow better usage of the logs.
    :param name: Log Name (usually the module using it)
    :param log_dir: the directory to log to (defaults to C:\\\\Python_logs)
    :param log_format: The Log Format
    :param overall_log_level: The overall log level
    :param stream_log_level: The stream log level
    :param file_log_level: The file log level
    :param file_max_bytes: the maximum bytes that the file can run to before rotating (default 100 KB)
    :param file_backup_count: the maximum number of backups allowed before clearing down the files, defaults to 5
    :return: logging.Logger configured to output to both a StreamHandler and a RotatingFileHandler with the
        chosen config
    """

    # Setup Logging
    _logger = logging.getLogger(name)
    _logger.handlers.clear()  # clear all handlers

    formatter = logging.Formatter(log_format)

    # Stream handling (print to console)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(stream_log_level)

    # File handling (log to log file)
    file_handler = logging.handlers.RotatingFileHandler(
        filename=os.path.join(log_dir, f'{name}.log'),
        maxBytes=file_max_bytes,
        backupCount=file_backup_count
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(file_log_level)

    # Add both handlers to the logger
    _logger.setLevel(overall_log_level)
    _logger.addHandler(file_handler)
    _logger.addHandler(stream_handler)

    return _logger


def set_level_to_all_stream_handlers(lvl: int = logging.ERROR) -> None:
    """
    This function is used to set all StreamHandlers to specific level.

    :param lvl: target stream logging level
    :return: None
    """

    # Find all existing loggers
    all_loggers = (logging.getLogger(name) for name in
                   logging.root.manager.loggerDict)

    for logger in all_loggers:
        if len(logger.handlers) != 0:
            try:
                stream_handlers = [x for x in logger.handlers if
                                   isinstance(x, logging.StreamHandler)]
                for stream_handler in stream_handlers:
                    stream_handler.setLevel(lvl)
            except IndexError:
                pass
