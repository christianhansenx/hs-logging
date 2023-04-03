# Standard Python modules
from typing import Optional, Callable, Any
import platform
import time
import os
import subprocess
import sys
import traceback
import re
from pathlib import Path
import logging
import logging.config

# Third party modules
import yaml

DEFAULT_TIME_FORMAT = '%(utc)%(iso8601us)'  # Used if no time format is provided for a logger
DEFAULT_EXCEPTION_LOGGER = 'exception'
EXCEPTION_POST_LOG_MSG = 'Application terminated due to exception'


class LoggingSetupException(BaseException):
    def __init__(self, message):
        super().__init__(message)


def exception_post_log(exception_logger: Optional[logging.Logger] = None) -> None:
    """
    A call back function for logging_setup function to log an exception.

    :param exception_logger: Logger of exceptions.
        If set to None then the exception is not logged.

    :return: None
    """
    if exception_logger is not None:
        exception_logger.critical(EXCEPTION_POST_LOG_MSG)
    exit_code = 1
    os._exit(exit_code)  # pylint: disable=(protected-access)


# <link> https://towardsdatascience.com/8-advanced-python-logging-features-that-you-shouldnt-miss-a68a5ef1b62d
def logging_setup(
    configuration_file_path: str,
    exception_logger_name: Optional[str] = DEFAULT_EXCEPTION_LOGGER,
    exception_post: Optional[Callable[[Optional[logging.Logger]], None]] = exception_post_log,
    fake_journal: Optional[bool] = None,
) -> Any:
    """
    See README file for usage.
    """

    def config_file_exception(error_message, exception_error=None):
        exception_error = f', {exception_error.__class__.__name__}: {exception_error}' if exception_error is not None else ''
        raise LoggingSetupException(f'{error_message}{exception_error}')

    _additional_text_formatters()
    logging.Formatter = _LoggingFormatter  # type: ignore  # mypy

    if not Path(configuration_file_path).is_file():
        config_file_exception(f'Configuration file does not exist: "{configuration_file_path}"')
    with open(configuration_file_path, 'rt', encoding='utf-8') as configuration_file:
        try:
            logging_configuration = yaml.safe_load(configuration_file.read())
        except BaseException as error:  # pylint: disable=(broad-except)
            config_file_exception(f'Could not load configuration file: "{configuration_file_path}"', error)

    # Create fake journal log file handlers if systemd is not supported
    _fake_journal_file(logging_configuration, fake_journal)

    # Create directories of logging files
    handlers = logging_configuration['handlers'].items()
    for handler in handlers:
        file_path = handler[1].get('filename')
        if file_path:
            directory_path = Path(file_path).parent
            Path(directory_path).mkdir(parents=True, exist_ok=True)

    # Parse logging configurations
    try:
        logging.config.dictConfig(logging_configuration)
    except BaseException as error:  # pylint: disable=(broad-except)
        config_file_exception(f'Error in configuration file: "{configuration_file_path}"', error)

    _exception_logger_setup(exception_logger_name, exception_post)

    return logging_configuration


class _LoggingFormatter(logging.Formatter):

    def formatTime(self, *args, **kwargs):
        record = args[0]
        time_format = args[1]

        if not time_format:
            time_format = DEFAULT_TIME_FORMAT

        if '%(iso8601)' in time_format:
            time_format = time_format.replace('%(iso8601)', '%Y-%m-%dT%H:%M:%S%z')
        if '%(iso8601ms)' in time_format:
            time_format = time_format.replace('%(iso8601ms)', '%Y-%m-%dT%H:%M:%S.%(millis)%z')
        if '%(iso8601us)' in time_format:
            time_format = time_format.replace('%(iso8601us)', '%Y-%m-%dT%H:%M:%S.%(micros)%z')

        if '%(utc)' in time_format:
            # <link> https://stackoverflow.com/questions/32402502/how-to-change-the-time-zone-in-python-logging
            self.converter = time.gmtime  # pylint: disable=(attribute-defined-outside-init)
            time_format = time_format.replace('%(utc)', '')
        if '%(tz)' in time_format:  # Same as %z but wit colon separator (e.g. +0100 -> +01:00)
            time_stamp = self.converter(record.created)
            time_zone = time.strftime('%z', time_stamp)  # %z does not contain colon e.g. +0100
            time_zone = time_zone[:3] + ':' + time_zone[-2:]  # Insert colon e.g. +01:00
            time_format = time_format.replace('%(tz)', time_zone)

        # ms and us are not rounded but truncated to integer. This is in alignment with standard Python logging.
        if '%(millis)' in time_format:
            # <link> https://gist.github.com/vernomcrp/18069053fb3cf3807c9e8601eb8016d5
            time_format = time_format.replace('%(millis)', str(int(record.msecs)).zfill(3))
        if '%(micros)' in time_format:
            time_format = time_format.replace('%(micros)', str(int(record.msecs * 1000)).zfill(6))

        args_list = list(args)
        args_list[1] = time_format
        return super().formatTime(*args_list, **kwargs)


def _additional_text_formatters():
    old_logging_record_factory = logging.getLogRecordFactory()

    def logging_record_factory(*args, **kwargs):
        record = old_logging_record_factory(*args, **kwargs)
        record.hostname = platform.node()
        return record

    logging.setLogRecordFactory(logging_record_factory)


def _fake_journal_file(logging_configuration, fake_journal):
    if fake_journal is None:
        result, error, returncode = _subprocess_command('journalctl | tail -n 1')
        ansi_escape = re.compile(r'(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]')
        error = ansi_escape.sub('', error).splitlines()[0]
        fake_journal = bool(result == '' and 'No journal files were found.' in error and returncode == 1)
    fake_handlers = []
    handlers = logging_configuration['handlers'].items()
    for handler in handlers:
        journal_handler = logging_configuration['handlers'][handler[0]]
        if 'fakejournal' in handler[1]:
            fake_handler_name = handler[1]['fakejournal']
            fake_handlers.append(fake_handler_name)
            if fake_journal:
                journal_handler.update(logging_configuration['handlers'][fake_handler_name])
            del journal_handler['fakejournal']
    for fake_handler_name in fake_handlers:
        del logging_configuration['handlers'][fake_handler_name]


def _subprocess_command(command):
    cmd_list = command.split()
    with subprocess.Popen(cmd_list, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as sub_process:
        output, error = sub_process.communicate(timeout=15)
    returncode = sub_process.returncode
    try:
        error = error.decode().strip()
    except UnicodeDecodeError:
        str(error)
    output = output.decode().strip()
    return output, error, returncode


def _exception_logger_setup(exception_logger_name, exception_post):
    if exception_logger_name is not None:
        exception_logger = logging.getLogger(exception_logger_name)

    def uncaught_exceptions(exc_type, exc_value, exc_traceback):
        # <link> https://stackoverflow.com/questions/4564559/get-exception-description-and-stack-trace-which-caused-an-exception-all-as-a-st  # pylint: disable=(line-too-long)  # noqa: E501

        traceback_info = ''.join(traceback.format_tb(exc_traceback)).replace('\n', '\\n')
        exception_logger.critical(
            f'{exc_type.__name__}: {exc_value}\\nTraceback:\\n{traceback_info}',
            # <code> exc_info=(exc_type, exc_value, exc_traceback)  # Multi lines traceback
        )
        sys.__excepthook__(exc_type, exc_value, exc_traceback)  # Default excepthook (traceback multi lines in console)
        if exception_post is not None:
            exception_post(exception_logger)

    if exception_logger_name is not None:
        sys.excepthook = uncaught_exceptions
