# **hs-logging - user guide**

</br>

# **Module File: [hs_logging.py](hs_logging/hs_logging.py)**

## **Logging Setup Function**
A function to read and parse logging setup yaml file.</br>
Using this function is  adding logging formatters to the standard logging formatters (see *Additional formatter's* section).

```python
def logging_setup(
    configuration_file_path: str,
    exception_logger_name: Optional[str] = DEFAULT_EXCEPTION_LOGGER,
    exception_post: Optional[Callable[[Optional[logging.Logger]], None]] = exception_post_log,
    fake_journal: Optional[bool] = None,
) -> Any:
```
</br>

### ***=== arguments ===***

#### **configuration_file_path**
Full path to yaml file with logging setup configurations.</br>
Example: 'project/logging_setup.yaml'

#### **exception_logger_name**
Name of logger for uncaught exceptions.</br>
If set to None then uncaught exceptions are not logged.

#### **exception_post**
Post function call back after the exception is logged.</br>
If an exception logger is defined (defined by argument *exception_logger_name*) a post function can be called after the exception is logged. If set to None then no post function is called.</br>
The default callback function *exception_post_log* is defined internal in this module and it is logging critical level message *EXCEPTION_POST_LOG_MSG*.

#### **fake_journal**
Flag for using fake systemd journal log file.</br>
If the system does not support systemd/journalctl then a fake journal logging handler can be used.</br>
Depending of set to True or False then fake journal logging is forced to be used or not. If set to None then fake journal logging is only used if journalctl is not available on the system.</br>
If fake journal is used then in the yaml configuration file the journal handler must contain *fakejournal:* pointing to the fake handler:</br>
```yaml
formatters:
  journal-fake-fmt:
    format: "%(asctime)s %(pathname)s[%(process)d]: %(levelname)-10s[%(name)s] %(message)s"
    datefmt: "%(utc)%(iso8601us)"

handlers:
  journal-handler:
    class: systemd.journal.JournalHandler
    fakejournal: journal-fake-handler  # Fake journalctl
  journal-fake-handler:
    filename: /var/log/journal/logging_fake_journal.log
    formatter: journal-fake-fmt
```
Journal handler will be overwritten with fake handler properties and the fake handler will be deleted.</br>
The fake logging format could e.g. match output of:</br>
```bash
journalctl --utc --output=short-iso-precise --no-hostname | grep INFO

2022-11-12T14:27:17.633063+0000 main/logging_setup.py[22132]: INFO logging message
```
</br>

### ***=== return ===***
Dictionary representation of the yaml configuration file (file defined in argument *configuration_file_path*).
</br></br>

### ***=== Additional formatter's ===***
Python standard logging formats: https://docs.python.org/3/library/logging.html#formatter-objects</br></br>
<ins>**Additional text formatters**</ins></br>
**%(hostname)s** : Computer hostname
</br></br>
<ins>**Additional time formatters**</ins></br>
**%(iso8601)** : ISO-8601 standard. Example: 2022-11-09T21:34:34+0200</br>
**%(iso8601ms)** : ISO-8601 standard including milliseconds. Example: 2022-11-09T21:34:34.452+0200</br>
**%(iso8601us)** : ISO-8601 standard including microseconds. Example: 2022-11-09T21:34:34.452890+0200</br>
**%(utc)** : The logging record time is being converted to UTC time</br>
**%(tz)** : Time zone is represented with colon. Example: 2022-11-09T21:34:34.452890+02:00 (instead of +0200)</br>
**%(millis)** : Milliseconds</br>
**%(micros)** : Microseconds</br>
</br>

## **Usage Example**
### **Yaml Setup File Example**

```yaml
# File name: logging_configuration.yaml
version: 1
disable_existing_loggers: true

formatters:
  console-fmt:
    format: "%(asctime)s [%(module)s, %(name)s] %(message)s\n"
  file-data-fmt:  # Includes computer/device host name
    format: "%(asctime)s\t%(hostname)s\t%(message)s"
    datefmt: "%(utc)%(iso8601ms)"
  journal-fmt:
    format: "%(levelname)-10s[%(name)s] %(message)s"
  journal-fake-fmt:
    format: "%(asctime)s %(pathname)s[%(process)d]: %(levelname)-10s[%(name)s] %(message)s"
    datefmt: "%(utc)%(iso8601us)"

handlers:
  console-out:
    class: logging.StreamHandler
    formatter: console-fmt
    stream: ext://sys.stdout
  file-data:
    class: logging.handlers.RotatingFileHandler
    formatter: file-data-fmt
    maxBytes: 1_000_000
    backupCount: 6
    filename: /tmp/test/data.log
  journal-handler:  # Requires systemctl
    class: systemd.journal.JournalHandler
    level: DEBUG
    formatter: journal-fmt
    fakejournal: journal-fake-handler
  journal-fake-handler:
    class: logging.handlers.RotatingFileHandler
    maxBytes: 1_000_000
    backupCount: 6
    filename: /var/log/journal/logging_fake_journal.log
    formatter: journal-fake-fmt

loggers:
  main:
    level: INFO
    handlers: [console-out, journal-handler]
  data:
    handlers: [console-out, file-data]
  exception:
    handlers: [journal-handler]

root:
  level: NOTSET
  # handlers: [console-out]  # This would pipe all handlers output to console
```
### **Code Example using above Yaml Setup File**
```python
from pathlib import Path
import logging

if __name__ == '__main__':

    # Parse logging configurations and create loggers
    logging_setup('logging_configuration.yaml')
    _logger_main = logging.getLogger('main')
    _logger_data = logging.getLogger('data').info

    _logger_main.info(f'=== Script: {Path(__file__).name} ===')
```
