import os
import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))


from scripts.cloudformation import CloudFormation
from scripts.log import Log
import scripts.stacks as stacks
from scripts.sleep import Sleep
from scripts.s3 import list_buckets, remove_from_bucket

ROOT = os.path.dirname(os.path.dirname(__file__))

tenant = sys.argv[1] if len(sys.argv) > 2 else "tcc"
region = sys.argv[2] if len(sys.argv) > 3 else "us-east-2"
profile = sys.argv[3] if len(sys.argv) > 4 else "tcc"
log_level = int(sys.argv[4], base=10) if len(sys.argv) > 4 else 3

cloudformation = CloudFormation(profile, region, log_level)
log = Log(log_level)


def remove_from_buckets():
    buckets = list_buckets(log, profile)

    for bucket in buckets:
        remove_from_bucket(bucket=bucket, log=log, profile=profile)


def delete_stacks(stk: list, cf: CloudFormation) -> None:
    stk = sorted(stk, key=lambda x: x["CreationTime"], reverse=True)
    waiting_stacks = []
    for stack in stk:
        stack_name = stack["StackName"]
        cf.delete_stack(stack_name)
        waiting_stacks.append(stack_name)

    cf.wait_stacks_delete(waiting_stacks)


remove_from_buckets()
stacks = cloudformation.list_final_status_stacks()["StackSummaries"]
delete_stacks(stacks, cloudformation)
log.info("All stacks and buckets were deleted")
