import os
import json
from typing import Any
from scripts.sleep import Sleep
from scripts.log import Log
from scripts.stacks import Stack


class CloudFormation:
    __FINAL_STATUS_STACKS = [
        "CREATE_FAILED",
        "UPDATE_ROLLBACK_FAILED",
        "UPDATE_COMPLETE",
        "DELETE_FAILED",
        "IMPORT_COMPLETE",
        "UPDATE_FAILED",
        "ROLLBACK_COMPLETE",
        "ROLLBACK_FAILED",
        "IMPORT_ROLLBACK_COMPLETE",
        "CREATE_COMPLETE",
        "IMPORT_ROLLBACK_FAILED",
        "UPDATE_ROLLBACK_COMPLETE",
    ]

    def __init__(self, profile: str, region: str, log_level=1) -> None:
        self.log = Log(log_level=log_level)
        self.profile = profile
        self.region = region
        self.sleep = Sleep(self.log)

    def package_and_deploy_stack(
        self, stack: Stack, output: str = "output.yaml"
    ) -> None:
        stack.set_output_template(output)
        self.log.checkpoint(f"Packaging {stack.stack_name}")
        self.package(stack["template"], stack["output_template"])
        self.log.info("\n")
        self.deploy_stack(stack)

    def deploy_stack(self, stack: Stack) -> None:
        template = stack["output_template"]
        stack_name = stack.stack_name
        parameters = stack["parameters"]
        self.log.checkpoint(f"Deploy of {stack_name}")
        self.deploy(template, stack_name, parameters)

    def delete_stack(self, stack_name: str) -> None:
        self.log.checkpoint(f"Deleting {stack_name}")
        cmd = self.__delete_stack(stack_name)
        self.log.cmd(cmd)
        os.system(f"{cmd} &> /dev/null")

    def get_stack_status(self, stack_name: str) -> str:
        stack = self.describe(stack_name)
        if "Stacks" not in stack or len(stack["Stacks"]) == 0:
            return "DELETE_COMPLETE"
        return stack["Stacks"][0]["StackStatus"]

    def stack_is_succesfully_deployed(self, stack_name: str) -> bool:
        status = self.get_stack_status(stack_name)
        return status in [
            "CREATE_COMPLETE",
            "UPDATE_COMPLETE",
            "UPDATE_ROLLBACK_COMPLETE",
        ]

    def check_if_stack_is_deleted(self, stack_name: str) -> tuple[bool, str]:
        DELETE_FINAL_STATUS = ["DELETE_COMPLETE"]
        try:
            stack = self.describe(stack_name)
            has_stacks = "Stacks" in stack
            if not has_stacks or len(stack["Stacks"]) == 0:
                return True, None
            stack = stack["Stacks"][0]
            has_status = "StackStatus" in stack
            if not has_status:
                return True, None
            return (
                stack["StackStatus"] in DELETE_FINAL_STATUS,
                stack["StackStatus"],
            )
        except Exception:
            return True, None

    def check_if_is_deleted(self, stack_name: str) -> str:
        is_deleted, status = self.check_if_stack_is_deleted(stack_name=stack_name)

        if is_deleted:
            self.log.info(f"\nStack {stack_name} has been deleted")
            return "DELETE_COMPLETE"

        if status == "UPDATE_ROLLBACK_COMPLETE":
            cmd = self.delete_stack(stack_name)
            os.system(f"{cmd} &> /dev/null")

        return status

    def wait_stacks_delete(self, stacks: list[str], max_retries_seg=1800) -> str:
        if max_retries_seg <= 0:
            return f"EXCEEDED_MAX_RETRIES: {' '.join(stacks)}"

        queue = stacks.copy()
        for stack in queue:
            status = self.check_if_is_deleted(stack)
            if status == "DELETE_COMPLETE":
                msg_status = f"{stack}: {status}"
                print(f"✅ {msg_status}")
                stacks.remove(stack)
            else:
                self.delete_stack(stack_name=stack)
        if len(stacks) == 0:
            return "ALL_STACKS_DELETED"
        message = f"Has {len(stacks)} in delete process"
        self.sleep.sleep(seconds=10, message=message, erase_len=len(message) + 30)
        return self.wait_stacks_delete(stacks, max_retries_seg - 10)

    def package(self, template: str, output: str) -> str:
        bucket = f"package-bucket-{self.region}"
        cmd = self.__package(bucket, template, output)
        os.system(f"{cmd} > /dev/null")
        return output

    def deploy(self, template: str, stack_name: str, parameters={}) -> None:
        cmd = self.__deploy(template, stack_name, parameters)
        self.log.cmd(cmd)
        os.system(cmd)

    def describe(self, stack_name: str) -> dict[str, Any]:
        cmd = self.__describe(stack_name)
        self.log.cmd(cmd)
        res = os.popen(cmd).read()
        return json.loads(res)

    def describe_stack_resources(self, stack_name: str):
        cmd = self.__describe_stack_resources(stack_name)
        self.log.cmd(cmd)
        cmd += " 2> /dev/null"
        res = os.popen(cmd).read()
        return json.loads(res)

    def list_final_status_stacks(self) -> dict[str, list[dict[str, Any]]]:
        try:
            cmd = self.__list_stacks(self.__FINAL_STATUS_STACKS)
            cmd += " 2> /dev/null"
            self.log.cmd(cmd)
            res = os.popen(cmd).read()
            return json.loads(res)
        except Exception:
            return {"StackSummaries": []}

    def list_exports(self):
        cmd = self.__prefix("list-exports")
        cmd += " 2> /dev/null"
        self.log.cmd(cmd)
        res = os.popen(cmd).read()
        return json.loads(res)

    def get_export_value(self, exports, name):
        exports = exports["Exports"]
        for exported in exports:
            if name == exported["Name"]:
                return exported["Value"]
        self.log.error(f"Não foi possível obter o valor exportado: {name}")
        return None

    def get_output_value(self, stack: dict, key: str) -> str:
        outputs = stack["Stacks"][0]["Outputs"]
        return [x["OutputValue"] for x in outputs if x["OutputKey"] == key][0]

    def get_physical_resource_id(self, resources: dict, resource: str) -> str:
        return [
            x["PhysicalResourceId"]
            for x in resources
            if x["LogicalResourceId"] == resource
        ][0]

    def lint(self, template: str) -> None:
        os.system(f"cfn-lint {template}")

    def __prefix(self, cmd) -> str:
        profile = (
            f"--profile {self.profile}"
            if self.profile and self.profile != "default"
            else ""
        )
        return f"aws {profile} --region {self.region} cloudformation {cmd}"

    def __list_stacks(self, filter: list[str] = None):
        status_filter = ""
        if filter:
            filter = '" "'.join(filter)
            status_filter = f'--stack-status-filter "{filter}"'

        cmd = self.__prefix(f"list-stacks {status_filter}")
        return cmd

    def __deploy(self, template, stack_name, parameters={}) -> str:
        cmd = "deploy --no-fail-on-empty-changeset --capabilities CAPABILITY_NAMED_IAM"
        cmd += f" --template-file {template}"
        cmd += f" --stack-name {stack_name}"
        if isinstance(parameters, dict) and len(parameters.keys()) > 0:
            params = "--parameter-overrides"
            for key in parameters:
                if parameters[key] == None or parameters[key] == "":
                    continue

                params += f" {key}='{parameters[key]}'"
            if params != "--parameter-overrides":
                cmd += f" {params}"
        return self.__prefix(cmd)

    def __describe(self, stack_name) -> str:
        cmd = f"describe-stacks --stack-name {stack_name}"
        return self.__prefix(cmd)

    def __describe_stack_resources(self, stack_name) -> str:
        cmd = f"describe-stack-resources --stack-name {stack_name}"
        return self.__prefix(cmd)

    def __delete_stack(self, stack_name) -> str:
        return self.__prefix(f"delete-stack --stack-name {stack_name}")

    def __package(self, bucket, template, output) -> str:
        cmd = "package"
        cmd += f" --template-file {template}"
        cmd += f" --output-template-file {output}"
        cmd += f" --s3-bucket {bucket}"
        return self.__prefix(cmd)
