import os
import sys
from os.path import abspath, dirname
from time import sleep

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))

from send_command import send_command
from get_command import get_and_wait
from document import document, get_document
from jenkins import jenkins, get_jenkins_instance, get_jenkins_url, jenkins_stack_name
from scripts.cloudformation import CloudFormation
from scripts.log import Log
from scripts.sleep import Sleep

new_environment = False
send_document = True

clone = sys.argv[1].lower() == "true" if len(sys.argv) > 1 else new_environment
log_level = int(sys.argv[9], base=10) if len(sys.argv) > 2 else 3
vpc = "vpc-0826717742c251f0f"
subnet = "subnet-0bc9e41ccc407a504"
amiid = "ami-0900fe555666598a2"
volume_size = 40
instance_type = "t2.medium"
tenant = "tcc"
region = "us-east-2"
profile = "tcc"

log = Log(log_level=log_level)
sleep = Sleep(log)
cloudformation = CloudFormation(profile, region, log_level)
if (
    clone == False
    and len(sys.argv) > 1
    and sys.argv[1].lower()
    in [
        "notsend",
        "nosend",
        "not_send",
        "no_send",
        "not send",
        "no send",
    ]
):
    clone = False
    send_document = False
elif clone == False:
    stacks = cloudformation.list_final_status_stacks()["StackSummaries"]
    has_jenkins_stack = jenkins_stack_name(tenant) in [
        stack["StackName"] for stack in stacks
    ]
    clone = not has_jenkins_stack

# DEPLOY
cloudformation.deploy_stack(
    stack=jenkins(
        tenant=tenant,
        vpc=vpc,
        subnet=subnet,
        volume_size=volume_size,
        amiid=amiid,
        instance_type=instance_type,
    )
)
cloudformation.deploy_stack(stack=document())


def send_document_procedure():
    log.checkpoint("Send Document to instance")
    document_name = get_document(cloudformation)
    jenkins_instance = get_jenkins_instance(tenant, cloudformation)
    command = send_command(
        profile, region, jenkins_instance, document_name, clone=clone
    )
    log.cmd("CommandId:", command["Command"]["CommandId"], "\n")
    status = get_and_wait(
        profile, region, jenkins_instance, command["Command"]["CommandId"], sleep
    )
    if status != "Success":
        log.error("\rFailed to send document, final status: ", status)
        exit(1)
    log.info("✅ Document sent successfully")


if send_document:
    send_document_procedure()
