class Stack:
    def __init__(
        self,
        template: str,
        stack_name: str,
        parameters: dict[str, str | int | bool],
    ) -> None:
        self.template = template
        self.stack_name = stack_name
        self.parameters = parameters

    @staticmethod
    def stack_name(tenant: str, name: str, stage: str = None) -> str:
        stage = (
            f"{stage[0].upper()}{stage[1:]}-"
            if isinstance(stage, str) and len(stage) > 1
            else ""
        )
        return stage + f"{tenant[0].upper()}{tenant[1:]}-{name}-Deploy"

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
        "jenkins.yml",
        Stack.stack_name(tenant, "jenkins"),
        {
            "VPC": vpc,
            "Subnet": subnet,
            "AmiId": amiid,
            "InstanceType": instance_type,
        },
    )


def jenkins_stack_name(tenant: str, stage: str = None) -> str:
    return Stack.stack_name(tenant, "jenkins", stage)
