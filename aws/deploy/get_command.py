import os
import sys
from typing import Any
from os.path import abspath, dirname, sep
import json

sys.path.append(sep.join([dirname(dirname(dirname(abspath(__file__)))), "scripts"]))


from document import document_stack_name
from jenkins import jenkins_stack_name
from utils.cloudformation import CloudFormation
from utils.log import Log
import utils.stacks as stacks

FILE_DIR = os.path.dirname(__file__)

command_id = (
    sys.argv[1]
    if len(sys.argv) > 1
    else json.loads(os.popen(f"/bin/cat {FILE_DIR}/command.output.json").read())[
        "Command"
    ]["CommandId"]
)
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
os.system(
    f"bash {FILE_DIR}/get-command.sh {jenkins} {command_id} {region} {profile}  > {FILE_DIR}/get_command.output.json"
)
command = json.loads(os.popen(f"/bin/cat {FILE_DIR}/get_command.output.json").read())

status = command["Status"]

print(status)
