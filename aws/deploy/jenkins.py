import os
from scripts.utils import stacks


def jenkins_stack_name(tenant: str) -> str:
    return stacks.stack_name(tenant=tenant, name="Jenkins")


def jenkins(
    tenant: str,
    vpc: str,
    subnet: str,
    amiid: str = "",
    instance_type: str = "",
) -> stacks.Stack:
    return stacks.Stack(
        os.sep.join(["aws", "jenkins.yaml"]),
        jenkins_stack_name(tenant=tenant),
        {
            "VpcId": vpc,
            "SubnetId": subnet,
            "AmiId": amiid,
            "InstanceType": instance_type,
            "GitUserName": "jenkins-tcc",
            "Tenant": tenant,
            "GitEmail": "jenkins@jenkins.jenkins",
            "SgInitIp": os.popen("curl ifconfig.me").read(),
        },
        tenant,
    )


def document_stack_name() -> str:
    return stacks.stack_name(name="Document-Run-Container")
