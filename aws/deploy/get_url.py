import os
import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
from scripts.cloudformation import CloudFormation

from jenkins import get_jenkins_url

tenant = sys.argv[1] if len(sys.argv) > 1 else "tcc"
region = sys.argv[2] if len(sys.argv) > 2 else "us-east-2"
profile = sys.argv[3] if len(sys.argv) > 3 else "tcc"
log_level = int(sys.argv[4], base=10) if len(sys.argv) > 4 else 3

cloudformation = CloudFormation(profile, region, log_level)

url = get_jenkins_url(tenant, cloudformation)
print(url)
os.system(f"xdg-open {url} &> /dev/null")
