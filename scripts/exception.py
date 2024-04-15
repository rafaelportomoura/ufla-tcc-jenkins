from scripts.stacks import Stack


class DeployException(Exception):
    def __init__(self, stack: Stack):
        self.message = "Failed to deploy stack: " + stack.stack_name
        super().__init__(self.message)
