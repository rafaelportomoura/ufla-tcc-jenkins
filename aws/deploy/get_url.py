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

FILE_DIR = os.path.dirname(__file__)

browser = sys.argv[1] if len(sys.argv) > 1 else "xdg-open"
tenant = sys.argv[2] if len(sys.argv) > 2 else "tcc"
region = sys.argv[3] if len(sys.argv) > 3 else "us-east-2"
profile = sys.argv[4] if len(sys.argv) > 4 else "tcc"
log_level = int(sys.argv[4], base=10) if len(sys.argv) > 4 else 3

cloudformation = CloudFormation(profile, region, log_level)
log = Log(log_level)


exports = cloudformation.list_exports()
jenkins = cloudformation.get_export_value(exports, f"{tenant}-jenkins-url")

os.system(f"{browser} {jenkins} & > /dev/null 2>&1")
