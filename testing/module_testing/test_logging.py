# Standard Python modules
import logging
from pathlib import Path
import os
import time

# Third party modules
import pytest

# First party external modules
from hs_logging.hs_logging import logging_setup, _LoggingFormatter


@pytest.mark.parametrize('test_step, timestamp', [  # <link> https://www.unixtimestamp.com/
    ({'tz': 'CST-1', 'handler': 'file-iso-micros', 'expected': '2022-12-09T11:13:09.000000+0100'}, 1670580789.000000),
    ({'tz': 'CST+8', 'handler': 'file-iso-micros', 'expected': '2022-12-09T02:13:09.999999-0800'}, 1670580789.999999),
    ({'tz': 'CST-1', 'handler': 'file-iso-micros-utc', 'expected': '2022-12-09T10:13:09.000001+0000'}, 1670580789.000001),
    ({'tz': 'CST+8', 'handler': 'file-iso-micros-utc', 'expected': '2022-12-09T10:13:09.999989+0000'}, 1670580789.999989),
])
def test_logging_iso(test_step, timestamp, _mock_format_time):
    """Logging time format ISO."""

    # Set time zone
    # <link> https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
    # <link> https://stackoverflow.com/questions/5873857/how-to-set-timezone-in-python-using-os-environ
    os.environ['TZ'] = test_step['tz']
    time.tzset()

    # Execute a logging record
    logging_configuration = logging_setup(_LOGGING_CONFIGURATION_FILE)
    logger_test = logging.getLogger('logger-test-main')
    logger_test.info(f'logger module test time format, time_stamp={timestamp}')

    # Test logging record time stamp
    logging_file = Path(logging_configuration['handlers'][test_step['handler']]['filename'])
    with open(logging_file, 'r', encoding='utf-8') as file:
        file_lines = file.readlines()
    file_line = file_lines[0].strip()
    expected = test_step['expected']
    assert file_line.startswith(expected), f'Expected "{expected}" in "{file_line}"'


_LOGGING_CONFIGURATION_FILE = f'{Path(__file__).resolve().parent}/test_logging_configuration.yaml'


# <link> https://stackoverflow.com/questions/66349953/how-to-pass-data-to-a-monkeypatch-in-pytest
@pytest.fixture
def _mock_format_time(monkeypatch, timestamp):

    original_format_time = _LoggingFormatter.formatTime

    def patch_format_time(self, *args, **kwargs):
        args_list = list(args)
        time_record = args[0]

        # Using string converting due to mathematics calculation is inaccurate
        timestamp_string = str(timestamp)
        timestamp_list = timestamp_string.split('.')
        time_record.msecs = int(timestamp_list[1]) * 0.001 if len(timestamp_list) > 1 else 0
        time_record.created = int(timestamp_list[0]) + time_record.msecs * 0.001

        args_list[0] = time_record
        return original_format_time(self, *args_list, **kwargs)

    monkeypatch.setattr(_LoggingFormatter, 'formatTime', patch_format_time)
