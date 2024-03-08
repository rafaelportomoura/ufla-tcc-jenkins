import sys
import os
from utils.cloudformation import CloudFormation
import utils.stacks as stacks


vpc = sys.argv[1] if len(sys.argv) > 1 else None
if not vpc:
    raise ValueError("VPC is required")
subnet = sys.argv[2] if len(sys.argv) > 2 else None
if not subnet:
    raise ValueError("Subnet is required")
amiid = sys.argv[3] if len(sys.argv) > 3 else "ami-022661f8a4a1b91cf"
instance_type = sys.argv[3] if len(sys.argv) > 3 else "t2.micro"
tenant = sys.argv[4] if len(sys.argv) > 4 else "tcc"
region = sys.argv[5] if len(sys.argv) > 5 else "us-east-2"
profile = sys.argv[6] if len(sys.argv) > 6 else "tcc"
log_level = int(sys.argv[7], base=10) if len(sys.argv) > 7 else 3

cloudformation = CloudFormation(profile, region, log_level)


cloudformation.deploy_stack(
    stacks.jenkins(
        tenant=tenant, vpc=vpc, subnet=subnet, amiid=amiid, instance_type=instance_type
    )
)
