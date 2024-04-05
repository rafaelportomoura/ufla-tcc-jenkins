from types import Any, LiteralString


class Job:
    name: str
    folder: str
    repository: str
    branch: str
    scm: str
    branch: str
    params: list
    steps: list
    clean_ws: list
    pre_build_clean: list

    def __init__(
        self, folder: str, name: str, branch: str, repository: str, scm_cron: str
    ):
        self.name = name
        self.folder = folder
        self.params = []
        self.clean_ws = []
        self.steps = []
        self.pre_build_clean = []
        self.repository = repository
        self.scm = scm_cron
        self.branch = branch

    def add_params(self, param_type: str, param: str, default: Any = '""'):
        self.params.append(f'{param_type}("{param}",{default})')

    def add_clean_ws(self, clean_ws: str, value: Any):
        self.clean_ws.append(f"{clean_ws}({value})")

    def add_pre_build_clean(self, pre_build_clean: str, value: Any = ""):
        self.pre_build_clean.append(f"{pre_build_clean}({value})")

    def add_steps(self, step: str, value: str = ""):
        self.steps.append(f"{step}({value})")

    def generate_steps(self) -> LiteralString:
        steps = "\n".join(self.steps)
        return f"steps {{\n{steps}\n}}"

    def generate_params(self) -> LiteralString:
        params = "\n".join(self.params)
        return f"parameters {{\n{params}\n}}"

    def create(
        self,
    ):
        return f"""
job('{self.folder}/{self.name}') {{
    {self.generate_steps()}
    publishers {{
        {self.publishers}
    }}
}}
"""

    def __str__(self):
        return f"Job {self.name}"
