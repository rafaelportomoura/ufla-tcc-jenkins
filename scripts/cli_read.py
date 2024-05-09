import subprocess
import re


class CliRead:
    def cmd(self, cmd: str):
        pattern = r"""((?:[^\s"']|"[^"]*"|'[^']*')+)"""
        args = re.findall(pattern, cmd)
        args = [
            "".join(re.findall(r"""((?:[^"']|"[^"]*"|'[^']*')+)""", arg))
            for arg in args
        ]
        print(args)
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, errors = process.communicate()

        if process.returncode != 0:
            raise CliReadException(errors.decode("utf-8"))

        return output.decode("utf-8")


class CliReadException(Exception):
    def __init__(self, error):
        super().__init__(f"❌ {error}")
