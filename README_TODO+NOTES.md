## **This file is for my own records as owner/developer of this repository.**</br></br>


# **TODO**

- https://ubuntu.com//blog/ubuntu-wsl-enable-systemd

- Journalctl settings on Pi</br>
https://raspberrypi.stackexchange.com/questions/79525/accessing-the-system-log-on-raspbian
https://raspberrypi.stackexchange.com/questions/108411/raspbian-journalctl-only-lists-current-boot-although-syslogs-exist</br>

- Concurrent logging with compressing</br>
https://queirozf.com/entries/log-rotation-in-python-reference-and-examples
https://github.com/Preston-Landers/concurrent-log-handler

</br>

# **NOTES**

https://pypi.org/project/piview/#description

logging sudo apt-get update && sudo apt-get upgrade && sudo apt-get install python3-systemd https://github.com/systemd/python-systemd from systemd import journal https://www.loggly.com/ultimate-guide/python-logging-basics/

Example for full disable:

    import logging
    if __name__ == '__main__':
        logging.disable(logging.NOTSET)

        logging.basicConfig(
            format="%(levelname) -10s %(asctime)s %(filename)s:%(lineno)s  %(message)s",
            level=logging.NOTSET
        )
        logging.getLogger().disabled = True

        # Testing
        logging.critical("Critical")
        logging.error("Error")
        logging.warning("Warning")
        logging.info("Info")
        logging.debug("Debug")

- (https://pypi.org/project/systemd-logging/)</br>
 sudo apt-get update && sudo apt-get upgrade && sudo apt-get install libsystemd-dev
