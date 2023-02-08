# **hs-logging**

**USER GUIDE**

</br>

def logging_setup(
    configuration_file_path: str,
    exception_logger_name: Optional[str] = DEFAULT_EXCEPTION_LOGGER,
    exception_post: Optional[Callable[[Optional[logging.Logger]], None]] = exception_post_logging,
    fake_journal: Optional[bool] = None,
) -> Any:
    """
    A function to read and parse logging setup yaml file.
    Standard Python logging formatters are extended using this function.

    :param configuration_file_path: Full path to yaml file with logging setup configurations.
        Example: 'project/logging_setup.yaml'
    :param exception_logger_name: Name of logger for uncaught exceptions.
        If set to None then uncaught exceptions are not logged.
    :param exception_post: Post function call back after the exception is logged.
        If an exception logger is defined (defined by :param exception_logger_name)
        a post function can be called after the exception is logged.
        If set to None then no post function is called.
    :param fake_journal: Flag for using fake systemd journal log file.
        If the system does not support systemd then a fake journal logging handler can be used.
        Depending of set to True or False then fake journal logging is forced to be used or not.
        If set to None then fake journal logging is only used if journalctl is not available on the system.
        In the yaml configuration file the journal handler must contain fakejournal: pointing to the fake handler:
          journal-handler:
            class: systemd.journal.JournalHandler
            fakejournal: journal-fake-handler
        Journal handler will be overwritten with fake handler properties and the fake handler will be deleted.
        The fake logging format could e.g. match output of: journalctl --utc --output=short-iso-precise --no-hostname | grep INFO
        Example: 2022-11-12T14:27:17.633063+0000 main/logging_setup.py[22132]: INFO logging message
    :return: Dictionary representation of the yaml configuration file (:param configuration_file_path)

    Additional formatter's (additional to standard):
        Standard formatting's: https://docs.python.org/3/library/logging.html#formatter-objects

        Additional text formatters:
            %(hostname)s = Computer hostname

        Additional time formatters:
            %(iso8601) = ISO-8601 standard. Example: 2022-11-09T21:34:34+0200
            %(iso8601us) = ISO-8601 standard including microseconds. Example: 2022-11-09T21:34:34.452890+0200
            %(utc) = The logging record time is being converted to UTC time
            %(tz) = Time zone is represented with colon. Example: 2022-11-09T21:34:34.452890+02:00 (instead of +0200)
            %(micros) = Microseconds
    """


