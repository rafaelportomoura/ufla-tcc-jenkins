import os
import sys
from typing import Any
from aws.deploy.document import document_stack_name
from aws.deploy.jenkins import jenkins_stack_name
from scripts.utils.cloudformation import CloudFormation
from scripts.utils.log import Log
import scripts.utils.stacks as stacks

ROOT = os.path.dirname(os.path.dirname(__file__))

tenant = sys.argv[1] if len(sys.argv) > 2 else "tcc"
region = sys.argv[2] if len(sys.argv) > 3 else "us-east-2"
profile = sys.argv[3] if len(sys.argv) > 4 else "tcc"
log_level = int(sys.argv[4], base=10) if len(sys.argv) > 4 else 3

cloudformation = CloudFormation(profile, region, log_level)
log = Log(log_level)


cloudformation.delete_stack(jenkins_stack_name(tenant=tenant))
cloudformation.delete_stack(document_stack_name())
