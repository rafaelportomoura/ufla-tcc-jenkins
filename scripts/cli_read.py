import subprocess
import re
import os
import pwd
import grp


def demote(user_name="jenkins", group_name="jenkins"):
    uid = pwd.getpwnam(user_name).pw_uid
    gid = grp.getgrnam(group_name).gr_gid
    os.setgid(gid)
    os.setuid(uid)


class CliRead:
    def cmd(self, cmd: str):
        pattern = r"""((?:[^\s"']|"[^"]*"|'[^']*')+)"""
        args = re.findall(pattern, cmd)
        args = [arg.strip() for arg in args]
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=lambda: demote(),
        )
        output, errors = process.communicate()

        if process.returncode != 0:
            raise CliReadException(errors.decode("utf-8"))

        return output.decode("utf-8")


class CliReadException(Exception):
    def __init__(self, error):
        super().__init__(f"❌ {error}")
