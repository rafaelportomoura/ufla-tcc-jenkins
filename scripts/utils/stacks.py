import os
from typing import Any

def stack_name(tenant: str, name: str) -> str:
    return f'{tenant[0].upper() + tenant[1:]}-{name}-Deploy'

def jenkins_stack_name(tenant: str) -> str:
    return stack_name(tenant,'Jenkins')
def jenkins(tenant: str, vpc: str, subnet: str, amiid: str, instance_type: type) -> dict[str, Any]:
    return {
        'template': os.path.join('stacks','jenkins.yaml'),
        'stack_name': jenkins_stack_name(tenant),
        'parameters': {
            'Tenant': tenant,
            'VpcId': vpc,
            'SubnetId': subnet,
            'AmiId': amiid,
            'InstanceType': instance_type,
            'SgInitIp': os.popen('curl ifconfig.me').read(),
        }
    }
