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
        stack_name: str,
        parameters: dict[str, str | int | bool] = None,
        tenant: str = None,
        stage: str = None,
    ) -> None:
        self.template = template
        self.stack_name = stack_name
        self.tenant = tenant
        self.parameters = parameters or {}
        self.stage = stage
        self.output_template = template

    def __str__(self) -> str:
        return self.stack_name

    def __getitem__(self, key: str) -> str | dict[str, str | int | bool]:
        if key == "template":
            return self.template
        elif key == "stack_name":
            return self.stack_name
        elif key == "parameters":
            return self.parameters
        elif key == "output_template":
            return self.output_template
        else:
            raise KeyError(f"Key {key} not found")

    def set_output_template(self, output_template: str) -> None:
        self.output_template = output_template
