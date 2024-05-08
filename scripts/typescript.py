import os


class Typescript:
    def __init__(
        self,
        node_version: int = 20,
        package_manager: str = "pnpm",
        package_manager_install: str = "install",
        package_manager_dev_build_flags: list[str] = [
            "--silent",
            "--no-optional",
            "--ignore-scripts",
        ],
        package_manager_prod_build_flags: list[str] = [
            "--prod",
            "--silent",
            "--no-optional",
            "--ignore-scripts",
        ],
    ):
        self.node_version = node_version
        self.package_manager = package_manager
        self.package_manager_install = package_manager_install
        self.package_manager_dev_build_flags = " ".join(package_manager_dev_build_flags)
        self.package_manager_prod_build_flags = " ".join(
            package_manager_prod_build_flags
        )

    def build(self, cmd: str = "build") -> None:
        package_install = f"{self.package_manager} {self.package_manager_install}"
        dev_install = f"{package_install} {self.package_manager_dev_build_flags}"
        os.system(
            f". ~/.nvm/nvm.sh \
                  && nvm use {self.node_version} \
                  && {dev_install} \
                  && {self.package_manager} run {cmd}"
        )
        print(
            "\n\n ============================== BUILDING PRODUCTION ==============================  \n\n",
            flush=True,
        )
        os.system(
            f". ~/.nvm/nvm.sh \
                  && nvm use {self.node_version} \
                  && rm -rf node_modules \
                  && echo '👍'\
                  && npm install -g yarn \
                  && yarn install --ignore-engines --production=true --silent"
        )
        print(
            "=================================== BUILDED ===================================== \n\n",
            flush=True,
        )

    def lint(self, cmd: str = "lint") -> None:
        os.system(f"{self.package_manager} run {cmd}")

    def test(self, cmd: str = "test") -> None:
        os.system(f"{self.package_manager} run {cmd}")

    def remove(self, package: str) -> None:
        os.system(
            f". ~/.nvm/nvm.sh \
                  && nvm use {self.node_version} \
                  && {self.package_manager} remove {package}"
        )
