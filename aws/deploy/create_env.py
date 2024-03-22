import sys
from os.path import abspath, dirname, sep

sys.path.append(sep.join([dirname(dirname(dirname(abspath(__file__)))), "scripts"]))


from document import document
from jenkins import jenkins
from utils.cloudformation import CloudFormation


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
    stack=jenkins(
        tenant=tenant, vpc=vpc, subnet=subnet, amiid=amiid, instance_type=instance_type
    )
)
cloudformation.deploy_stack(stack=document())
