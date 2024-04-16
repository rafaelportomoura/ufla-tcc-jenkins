import os
import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))


from scripts.cloudformation import CloudFormation
from scripts.log import Log
import scripts.stacks as stacks
from scripts.sleep import Sleep

ROOT = os.path.dirname(os.path.dirname(__file__))

tenant = sys.argv[1] if len(sys.argv) > 2 else "tcc"
region = sys.argv[2] if len(sys.argv) > 3 else "us-east-2"
profile = sys.argv[3] if len(sys.argv) > 4 else "tcc"
log_level = int(sys.argv[4], base=10) if len(sys.argv) > 4 else 3

cloudformation = CloudFormation(profile, region, log_level)
log = Log(log_level)

stacks = cloudformation.list_final_status_stacks()["StackSummaries"]

stacks = sorted(stacks, key=lambda x: x["CreationTime"], reverse=True)
waiting_stacks = []
for stack in filter(
    lambda x: x["StackName"]
    not in [
        "Tcc-Jenkins-Deploy",
        "Clone-Or-Update-Repository-Document-Deploy",
        "Prod-Tcc-Domain-Deploy",
    ],
    stacks,
):
    stack_name = stack["StackName"]
    cloudformation.delete_stack(stack_name)
    waiting_stacks.append(stack_name)

cloudformation.wait_stacks_delete(waiting_stacks)
