import datetime
import logging
import tempfile
from pathlib import Path

from util.application_directories import ApplicationDirectories


def make_console_handler_from_config(console_config=None):
    if console_config is None:
        console_config = dict()
    console_enabled = bool(console_config.get("enabled", "True"))
    if console_enabled:
        console_level = console_config.get("level", "DEBUG")
        default_console_log_format = \
            "[%(levelname)-8s][%(asctime)s][%(filename)s:%(lineno)d]: %(message)s"
        console_log_format = console_config.get("log_format", default_console_log_format)
        console_date_format = console_config.get("date_format", "%Y-%m-%d %H:%M:%S")
        console_handler = logging.StreamHandler()
        console_handler.setLevel(console_level)
        formatter = logging.Formatter(console_log_format, datefmt=console_date_format)
        console_handler.setFormatter(formatter)
        return console_handler
    return None


def make_file_handler_from_config(file_config=None, **kargs):
    if file_config is None:
        file_config = dict()
    file_enabled = bool(file_config.get("enabled", "True"))
    if file_enabled:
        app_dirs: ApplicationDirectories = kargs.get("app_dirs")
        if app_dirs:
            log_name = app_dirs.app_name()
            default_file_log_dir = app_dirs.log_dirpath()
        else:
            log_name = kargs.get("log_name", "logfile")
            default_file_log_dir = f"{tempfile.gettempdir()}/{log_name}/log"
        file_level = file_config.get("level", "DEBUG")
        default_file_log_format = \
            "[%(levelname)-8s][%(asctime)s][%(pathname)s:%(lineno)d %(funcName)s]: %(message)s"
        file_log_format = file_config.get("log_format", default_file_log_format)
        file_date_format = file_config.get("date_format", "%Y-%m-%d %H:%M:%S")
        filename_format = file_config.get("filename_format", f"{log_name}_%Y%m%d_%H%M%S_%f.log")
        filename_format = datetime.datetime.now().strftime(filename_format)
        if filename_format.find("logfile") == -1:
            pass
        file_dir = Path(file_config.get("dir", default_file_log_dir))
        file_dir.mkdir(parents=True, exist_ok=True)
        log_filepath = file_dir / filename_format
        file_handler = logging.FileHandler(filename=log_filepath, mode="w")
        file_handler.setLevel(file_level)
        formatter = logging.Formatter(file_log_format, datefmt=file_date_format)
        file_handler.setFormatter(formatter)
        return file_handler, log_filepath
    return None, None


def make_logger_from_config(config=None, write_filepath: bool = False, **kargs):
    if config is None:
        config = dict()
    app_dirs: ApplicationDirectories = kargs.get("app_dirs")
    if app_dirs:
        log_name = app_dirs.app_name()
    else:
        log_name = kargs.get("log_name", "logfile")
    logger = logging.Logger(f"{log_name}")
    console_config = config.get("console", dict())
    console_handler = make_console_handler_from_config(console_config)
    if console_handler is not None:
        logger.addHandler(console_handler)
    file_config = config.get("file", dict())
    file_handler, log_filepath = make_file_handler_from_config(file_config, **kargs)
    if file_handler is not None:
        logger.addHandler(file_handler)
        if write_filepath:
            logger.info(f"Log to {log_filepath}")
    return logger, log_filepath


class ScopeLog:
    STACKLEVEL = 2

    def __init__(self, message: str, logger=None, **kwargs):
        if logger is None:
            logger = logging.getLogger()
        self.__logger = logger
        self.__level = kwargs.get("level", logging.DEBUG)
        self.__begin_format = kwargs.get("begin_format", " {}")
        self.__end_format = kwargs.get("end_format", "/{}")
        self.__message = message
        self.__stacklevel = kwargs.get("stacklevel", ScopeLog.STACKLEVEL)
        self.__logger.log(self.__level, self.__begin_format.format(message), stacklevel=self.__stacklevel)

    def __del__(self):
        if self.__logger is not None:
            message = self.__message
            self.__logger.log(self.__level, self.__end_format.format(message), stacklevel=self.__stacklevel - 1)
            self.__logger = None

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.__logger is not None:
            message = self.__message
            self.__logger.log(self.__level, self.__end_format.format(message), stacklevel=self.__stacklevel - 1)
            self.__logger = None


class MethodScopeLog(ScopeLog):
    STACKLEVEL = ScopeLog.STACKLEVEL + 1

    def __init__(self, hs, logger=None, **kwargs):
        if logger is None:
            logger = logging.getLogger()
        try:
            fn, lno, func, sinfo = logger.findCaller(False, 2)
        except ValueError:
            fn, lno, func = "(unknown file)", 0, "(unknown function)"
        kwargs["stacklevel"] = MethodScopeLog.STACKLEVEL
        super().__init__(f"{hs.__class__.__name__}.{func}", logger, **kwargs)
