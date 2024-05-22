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
        self,
        cloudformation: Cloudformation,
        stack_name: str,
        service_logical_id: str = "Service",
        cluster_logical_id: str = "Cluster",
    ):
        if not cloudformation.stack_is_succesfully_deployed(stack_name=stack_name):
            return None

        stack_resources = cloudformation.describe_stack_resources(stack_name=stack_name)
        service = None
        cluster = None
        count = 0
        resources = stack_resources["StackResources"]
        while (not service or not cluster) and count < len(resources):
            resource = resources[count]
            logical_id = resource["LogicalResourceId"]
            physical_id = resource["PhysicalResourceId"]
            if logical_id == service_logical_id:
                service = physical_id
            elif logical_id == cluster_logical_id:
                cluster = physical_id
            count += 1

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
