from scripts.log import Log
from scripts.cli_read import CliRead
import os


class Typescript:
    def __init__(
        self, node_version: int = 20, cli_read: CliRead = CliRead(), log_level=1
    ):
        self.log = Log(log_level=log_level)
        nvm_path = os.path.join(os.environ["HOME"], ".nvm", "nvm.sh")
        self.source_nvm = (
            f"source {nvm_path} > /dev/null && nvm use {node_version} > /dev/null"
        )
        self.cli_read = cli_read

    def build(
        self,
        dev_install="pnpm install --silent --no-optional --ignore-scripts",
        cmd: str = "pnpm run build",
        pre_build="echo ''",
        post_build: str = "rm -rf node_modules",
    ) -> None:
        self.log.info("🏗 Building")
        full_cmd = f"{self.source_nvm} && {dev_install} && {pre_build} && {cmd} && {post_build}"
        self.log.cmd(full_cmd)
        self.cli_read.cmd(full_cmd)
        self.log.info("🏗 Builded")

    def remove(self, package: str, cmd: str = "pnpm remove") -> None:
        output = self.cli_read.cmd(f"{self.source_nvm} && {cmd} && {package}")
        self.log.info(output)

    def lambda_packages(
        self, cmd="yarn install --ignore-engines --production=true --silent"
    ):
        self.log.info("📦 Install lambda packages")
        full_cmd = f"{self.source_nvm} && {cmd}"
        self.log.cmd(full_cmd)
        self.cli_read.cmd(full_cmd)
        self.log.info("📦 Installed lambda packages")
