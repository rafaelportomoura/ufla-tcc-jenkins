import os
from scripts.log import Log


def remove_from_bucket(bucket: str, log: Log, profile: str = None) -> None:
    cmd += "aws"
    cmd += f" --profile {profile}" if profile or profile != "default" else ""
    cmd += f" s3 rm s3://{bucket} --recursive"
    log.cmd(cmd)
    os.system(cmd)
