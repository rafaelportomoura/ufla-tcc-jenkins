import os
from utils.log import Log


def remove_from_bucket(profile: str, bucket: str, log: Log) -> None:
    cmd = f"aws --profile {profile} s3 rm s3://{bucket} --recursive"
    log.cmd(cmd)
    os.system(cmd)
