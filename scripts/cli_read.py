import subprocess
import re


class CliRead:
    def cmd(self, cmd: str):
        pattern = r"""((?:[^\s"']|"[^"]*"|'[^']*')+)"""
        args = re.findall(pattern, cmd)
        args = [arg.strip() for arg in args]
        process = subprocess.Popen(
            args,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            executable="/bin/bash",
        )
        output, errors = process.communicate()

        if process.returncode != 0:
            raise CliReadException(errors.decode("utf-8"))

        return output.decode("utf-8")

    def pre_defined_cmd(self, cmds: str):
        process = subprocess.Popen(
            cmds,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            executable="/bin/bash",
            text=True,
        )
        output, errors = process.communicate()

        if process.returncode != 0:
            raise CliReadException(errors.decode("utf-8"))

        return output


class CliReadException(Exception):
    def __init__(self, error):
        super().__init__(f"❌ {error}")
