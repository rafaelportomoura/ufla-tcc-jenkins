import os
from scripts.log import Log


def remove_from_bucket(bucket: str, log: Log, profile: str = None) -> None:
    cmd += "aws"
    cmd += f" --profile {profile}" if profile or profile != "default" else ""
    cmd += f" s3 rm s3://{bucket} --recursive"
    log.cmd(cmd)
    os.system(cmd)


def list_buckets(log: Log, profile: str = None) -> list:
    cmd = "aws"
    cmd += f" --profile {profile}" if profile or profile != "default" else ""
    cmd += " s3 ls"
    log.cmd(cmd)
    return os.popen(cmd).read().split("\n")
