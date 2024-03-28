import os
from scripts import stacks


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
            "Tenant": tenant,
            "SgInitIp": os.popen("curl https://api.ipify.org").read(),
        },
        tenant,
    )


def get_jenkins_instance(tenant: str, cloudformation) -> str:
    exports = cloudformation.list_exports()
    jenkins = cloudformation.get_export_value(exports, f"{tenant}-jenkins-instance")
    return jenkins


def get_jenkins_url(tenant: str, cloudformation) -> str:
    exports = cloudformation.list_exports()
    jenkins = cloudformation.get_export_value(exports, f"{tenant}-jenkins-url")
    return jenkins


def document_stack_name() -> str:
    return stacks.stack_name(name="Document-Run-Container")
