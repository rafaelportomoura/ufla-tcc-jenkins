import os
from scripts.log import Log
from scripts.cloudformation import Cloudformation
from scripts.exception import NotFoundException


class ECS:
    def __init__(self, profile: str, region: str, log_level=1) -> None:
        self.log = Log(log_level=log_level)
        self.profile = profile
        self.region = region

    def force_new_deployment(self, cluster: str, service: str):
        cmd = self.__force_new_deployment(cluster, service)
        self.log.cmd(cmd)
        os.system(f"{cmd} > /dev/null")

    def force_stack_new_deployment(
        self, cloudformation: Cloudformation, stack_name: str
    ):
        if not cloudformation.stack_is_succesfully_deployed(stack_name=stack_name):
            return None

        stack_resources = cloudformation.describe_stack_resources(stack_name=stack_name)
        service = [
            x["PhysicalResourceId"] if x["LogicalResourceId"] == "Service" else None
            for x in stack_resources["StackResources"]
        ][0]
        cluster = [
            x["PhysicalResourceId"] if x["LogicalResourceId"] == "Cluster" else None
            for x in stack_resources["StackResources"]
        ][0]
        if not service:
            raise NotFoundException("Service not found")
        if not cluster:
            raise NotFoundException("Cluster not found")

        self.force_new_deployment(cluster=cluster, service=service)

    def __force_new_deployment(self, cluster: str, service: str):
        cmd = self.__prefix(
            f"update-service --cluster {cluster} --service {service} --force-new-deployment"
        )
        self.log.cmd(cmd)
        return cmd

    def __prefix(self, cmd: str) -> str:
        profile = (
            f"--profile {self.profile}"
            if self.profile and self.profile != "default"
            else ""
        )
        return f"aws {profile} --region {self.region} ecs {cmd}"
