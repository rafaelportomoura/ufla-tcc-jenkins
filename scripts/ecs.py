import os
from scripts.log import Log


class ECS:
    def __init__(self, profile: str, region: str, log_level=1) -> None:
        self.log = Log(log_level=log_level)
        self.profile = profile
        self.region = region

    def force_new_deployment(self, cluster: str, service: str):
        cmd = self.__force_new_deployment(cluster, service)
        self.log.cmd(cmd)
        os.system(cmd)

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
        return f"aws  --profile {profile} --region {self.region} ecs {cmd}"
