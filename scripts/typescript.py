import os


class Typescript:
    def __init__(
        self,
        package_manager: str = "pnpm",
        package_manager_install: str = "install",
        package_manager_dev_build_flags: list[str] = [
            "--dev",
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
        self.package_manager = package_manager
        self.package_manager_install = package_manager_install
        self.package_manager_dev_build_flags = " ".join(package_manager_dev_build_flags)
        self.package_manager_prod_build_flags = " ".join(
            package_manager_prod_build_flags
        )

    def build(self, cmd: str = "build") -> None:
        package_install = f"{self.package_manager} {self.package_manager_install}"
        dev_install = f"{package_install} {self.package_manager_dev_build_flags}"
        os.system(dev_install)
        os.system("find ./node_modules -mtime +10950 -exec touch {} +")
        os.system(f"{self.package_manager} run {cmd}")
        os.system("rm -rf node_modules")
        prod_install = f"{package_install} {self.package_manager_prod_build_flags}"
        os.system(prod_install)

    def lint(self, cmd: str = "lint") -> None:
        os.system(f"{self.package_manager} run {cmd}")

    def test(self, cmd: str = "test") -> None:
        os.system(f"{self.package_manager} run {cmd}")
