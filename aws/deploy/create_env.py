import os
import sys
from os.path import abspath, dirname, sep
from time import sleep

sys.path.append(sep.join([dirname(dirname(dirname(abspath(__file__)))), "scripts"]))

from send_command import send_command
from get_command import get_and_wait
from document import document, get_document
from jenkins import jenkins, get_jenkins_instance, get_jenkins_url
from utils.cloudformation import CloudFormation
from utils.log import Log

clone = sys.argv[1] == "True" if len(sys.argv) > 1 else False
vpc = sys.argv[2] if len(sys.argv) > 2 else "vpc-0826717742c251f0f"
subnet = sys.argv[3] if len(sys.argv) > 3 else "subnet-0bc9e41ccc407a504"
amiid = sys.argv[4] if len(sys.argv) > 4 else "ami-022661f8a4a1b91cf"
instance_type = sys.argv[5] if len(sys.argv) > 5 else "t2.micro"
tenant = sys.argv[6] if len(sys.argv) > 6 else "tcc"
region = sys.argv[7] if len(sys.argv) > 7 else "us-east-2"
profile = sys.argv[8] if len(sys.argv) > 8 else "tcc"
log_level = int(sys.argv[9], base=10) if len(sys.argv) > 9 else 3

log = Log(log_level=log_level)
cloudformation = CloudFormation(profile, region, log_level)

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
log.cmd("Command_id", command["Command"]["CommandId"])
status = get_and_wait(
    profile, region, jenkins_instance, command["Command"]["CommandId"]
)

if status == "Success":
    for simbol in ["⣾", "⣷", "⣯", "⣟", "⡿", "⢿", "⣻", "⣽"]:
        print(f"\r{simbol} Waiting for Jenkins to start", end="", flush=True)
        sleep(1.5)
    print(f"\r{' '* 31}")
    log.checkpoint("Opened in browser")
    url = get_jenkins_url(tenant, cloudformation)
    os.system(f"xdg-open {url} &> /dev/null")
    exit(0)
