# Standard Python modules
import subprocess
from platform import uname


class Utilities:

    @staticmethod
    def wsl_info():  # <link> https://www.scivision.dev/python-detect-wsl
        info = uname().release
        if 'microsoft-standard' not in info:
            info = f'NOT WSL - {info}'
        else:
            info = info.replace('microsoft-standard-', '')
        return info

    @staticmethod
    def subprocess_command(command_line):
        command_list = command_line.split()
        with subprocess.Popen(command_list, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as sub_proc:
            output, output_error = sub_proc.communicate(timeout=15)
        returncode = sub_proc.returncode
        try:
            output_error = output_error.decode().strip()
        except UnicodeDecodeError:
            str(output_error)
        output = output.decode().strip()
        return output, output_error, returncode
