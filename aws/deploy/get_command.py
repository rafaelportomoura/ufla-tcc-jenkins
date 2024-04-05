import os
import sys
from os.path import abspath, dirname, sep
import json

if abspath(__file__) != abspath(sys.argv[0]):
    from scripts.sleep import Sleep
else:
    sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
    from scripts.sleep import Sleep
    from scripts.cloudformation import CloudFormation
    from scripts.log import Log


def get_command(profile: str, region: str, jenkins: str, command_id: str):
    command = os.popen(
        "aws ssm get-command-invocation"
        + f" --profile {profile}"
        + f" --region {region}"
        + f" --instance-id {jenkins}"
        + f" --command-id {command_id}"
    ).read()

    return json.loads(command)


status_replace = lambda status, erase_len, simbol="": print(
    f'\r{" " * (erase_len + len(simbol))}\r{simbol}{status}', end="", flush=True
)


def get_and_wait(
    profile: str, region: str, jenkins: str, command_id: str, sleep: Sleep
):
    get_status = lambda: get_command(profile, region, jenkins, command_id)["Status"]
    status = get_status()
    print(status, end="")
    while status == "InProgress":
        erase_len = len(status) + 3
        sleep.sleep(seconds=10, message="{{symbol}} " + status, erase_len=erase_len)
        status = get_status()
    return status


if __name__ == "__main__" and abspath(__file__) == abspath(sys.argv[0]):
    FILE_DIR = os.path.dirname(__file__)

    command_id = sys.argv[1] if len(sys.argv) > 1 else None
    if not command_id:
        with open(f"{FILE_DIR}/command.output.json", "r") as f:
            command_id = json.load(f)["Command"]["CommandId"]
    if not command_id:
        raise ValueError("Command ID is required")
    tenant = sys.argv[2] if len(sys.argv) > 2 else "tcc"
    region = sys.argv[3] if len(sys.argv) > 3 else "us-east-2"
    profile = sys.argv[4] if len(sys.argv) > 4 else "tcc"
    log_level = int(sys.argv[4], base=10) if len(sys.argv) > 4 else 3

    cloudformation = CloudFormation(profile, region, log_level)
    log = Log(log_level)

    exports = cloudformation.list_exports()
    jenkins = cloudformation.get_export_value(exports, f"{tenant}-jenkins-instance")

    command = get_command(profile, region, jenkins, command_id)

    with open(f"{FILE_DIR}/get-command.output.json", "w") as f:
        f.write(json.dumps(command))

    status = command["Status"]

    final_status = get_and_wait(profile, region, jenkins, command_id, Sleep(log))

    print("✅" if final_status == "Success" else "❌", final_status)
