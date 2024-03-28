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

clean_environment = False


clone = sys.argv[1] == "True" if len(sys.argv) > 1 else clean_environment
vpc = sys.argv[2] if len(sys.argv) > 2 else "vpc-0826717742c251f0f"
subnet = sys.argv[3] if len(sys.argv) > 3 else "subnet-0bc9e41ccc407a504"
amiid = sys.argv[4] if len(sys.argv) > 4 else "ami-022661f8a4a1b91cf"
instance_type = sys.argv[5] if len(sys.argv) > 5 else "t2.micro"
tenant = sys.argv[6] if len(sys.argv) > 6 else "tcc"
region = sys.argv[7] if len(sys.argv) > 7 else "us-east-2"
profile = sys.argv[8] if len(sys.argv) > 8 else "tcc"
log_level = int(sys.argv[9], base=10) if len(sys.argv) > 9 else 3

log = Log(log_level=log_level)
sleep = Sleep(log)
cloudformation = CloudFormation(profile, region, log_level)

if clone == False:
    stacks = cloudformation.list_final_status_stacks()["StackSummaries"]
    has_jenkins_stack = jenkins_stack_name(tenant) in [
        stack["StackName"] for stack in stacks
    ]
    clone = not has_jenkins_stack

# DEPLOY
cloudformation.deploy_stack(
    stack=jenkins(
        tenant=tenant, vpc=vpc, subnet=subnet, amiid=amiid, instance_type=instance_type
    )
)
cloudformation.deploy_stack(stack=document())

log.checkpoint("Send Document to Jenkins instance")
document_name = get_document(cloudformation)
jenkins_instance = get_jenkins_instance(tenant, cloudformation)
command = send_command(profile, region, jenkins_instance, document_name, clone=clone)
log.cmd("CommandId:", command["Command"]["CommandId"], "\n")
status = get_and_wait(
    profile, region, jenkins_instance, command["Command"]["CommandId"], sleep
)
if status != "Success":
    log.error("Failed to send document, final status: ", status)
    exit(1)

sleep.sleep(10, "{{symbol}} Get jenkins url in {{time_desc}} seconds")
print(f"\r{' '* 31}")
url = get_jenkins_url(tenant, cloudformation)
log.checkpoint(f"Opening in browser with {url}")
os.system(f"xdg-open {url} &> /dev/null")
