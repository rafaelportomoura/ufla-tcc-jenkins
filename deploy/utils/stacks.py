import os


def first_upper(s: str) -> str:
    return f"{s[0].upper()}{s[1:]}"


def stack_name(name: str, tenant: str = None, stage: str = None) -> str:
    stage = (
        f"{first_upper(stage)}-" if isinstance(stage, str) and len(stage) > 1 else ""
    )
    tenant = (
        f"{first_upper(tenant)}-" if isinstance(tenant, str) and len(tenant) > 1 else ""
    )
    return stage + tenant + f"{first_upper(name)}-Deploy"


class Stack:
    def __init__(
        self,
        template: str,
        name: str,
        parameters: dict[str, str | int | bool],
        tenant: str = None,
        stage: str = None,
    ) -> None:
        self.template = template
        self.name = name
        self.tenant = tenant
        self.parameters = parameters
        self.stage = stage

    def stack_name(self) -> str:
        return stack_name(tenant=self.tenant, name=self.name, stage=self.stage)

    def __str__(self) -> str:
        return self.stack_name

    def __getitem__(self, key: str) -> str | dict[str, str | int | bool]:
        if key == "template":
            return self.template
        elif key == "stack_name":
            return self.stack_name
        elif key == "parameters":
            return self.parameters
        else:
            raise KeyError(f"Key {key} not found")


def jenkins(
    tenant: str,
    vpc: str,
    subnet: str,
    amiid: str = "",
    instance_type: str = "",
) -> Stack:
    return Stack(
        os.sep.join(["stacks", "jenkins.yaml"]),
        "Jenkins",
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


def jenkins_stack_name(tenant: str = None, stage: str = None) -> str:
    return stack_name(tenant=tenant, name="Jenkins", stage=stage)


def document(
    path: str = None,
    url: str = None,
    branch: str = None,
    container: str = None,
    email: str = None,
    username: str = None,
) -> Stack:
    return Stack(
        os.sep.join(["stacks", "document.yaml"]),
        "Document-Run-Container",
        {
            "GitRepositoryPath": path,
            "GitRepositoryCloneUrl": url,
            "GitRepositoryBranch": branch,
            "ContainerName": container,
            "GitEmail": email,
            "GitUserName": username,
        },
    )


def document_stack_name() -> str:
    return stack_name(name="Document-Run-Container")
