import os
from scripts.stacks import Stack, stack_name


def document(
    path: str = None,
    url: str = None,
    branch: str = None,
    email: str = None,
    username: str = None,
) -> Stack:
    return Stack(
        os.sep.join(["aws", "document.yaml"]),
        document_stack_name(),
        {
            "GitRepositoryPath": path,
            "GitRepositoryCloneUrl": url,
            "GitRepositoryBranch": branch,
            "GitEmail": email,
            "GitUserName": username,
        },
    )


def get_document(cloudformation) -> str:
    exports = cloudformation.list_exports()
    document = cloudformation.get_export_value(exports, "clone-or-update-repository")
    return document


def document_stack_name() -> str:
    return stack_name(name="Clone-Or-Update-Repository-Document")
