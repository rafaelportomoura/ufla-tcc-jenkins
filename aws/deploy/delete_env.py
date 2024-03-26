import os
import sys
from typing import Any
from os.path import abspath, dirname, sep

sys.path.append(sep.join([dirname(dirname(dirname(abspath(__file__)))), "scripts"]))


from document import document_stack_name
from jenkins import jenkins_stack_name
from utils.cloudformation import CloudFormation
from utils.log import Log
import utils.stacks as stacks

ROOT = os.path.dirname(os.path.dirname(__file__))

tenant = sys.argv[1] if len(sys.argv) > 2 else "tcc"
region = sys.argv[2] if len(sys.argv) > 3 else "us-east-2"
profile = sys.argv[3] if len(sys.argv) > 4 else "tcc"
log_level = int(sys.argv[4], base=10) if len(sys.argv) > 4 else 3

cloudformation = CloudFormation(profile, region, log_level)
log = Log(log_level)

stacks = cloudformation.list_final_status_stacks()["StackSummaries"]

stacks = sorted(stacks, key=lambda x: x["CreationTime"], reverse=True)
for stack in stacks:
    stack_name = stack["StackName"]
    cloudformation.delete_stack(stack_name)
    cloudformation.wait_stack_delete(stack_name)
