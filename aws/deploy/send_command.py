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

FILE_DIR = dirname(__file__)

clone = "True" if len(sys.argv) > 1 else "False"
tenant = sys.argv[2] if len(sys.argv) > 2 else "tcc"
region = sys.argv[3] if len(sys.argv) > 3 else "us-east-2"
profile = sys.argv[4] if len(sys.argv) > 4 else "tcc"
log_level = int(sys.argv[5], base=10) if len(sys.argv) > 5 else 3

cloudformation = CloudFormation(profile, region, log_level)
log = Log(log_level)


exports = cloudformation.list_exports()
document = cloudformation.get_export_value(exports, "jenkins-document")
jenkins = cloudformation.get_export_value(exports, f"{tenant}-jenkins-instance")

os.system(
    f"bash {FILE_DIR}/send-command.sh {jenkins} {document} {clone} {region} {profile} > {FILE_DIR}/command.output.json"
)
command = os.popen(f"/bin/cat {FILE_DIR}/command.output.json").read()

command_id = json.loads(command)["Command"]["CommandId"]

print(command_id)
