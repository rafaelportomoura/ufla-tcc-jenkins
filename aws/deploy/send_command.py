import os
import sys
import json


def send_command(
    profile: str, region: str, jenkins: str, document: str, clone: bool = False
):
    command = os.popen(
        "aws ssm send-command"
        + f" --profile {profile}"
        + f" --region {region}"
        + f" --instance-ids {jenkins}"
        + f" --document-name {document}"
        + f' --parameters "Clone={"True" if clone else "False"}"'
    ).read()

    return json.loads(command)


if __name__ == "__main__" and __file__ == os.path.abspath(sys.argv[0]):
    from os.path import abspath, dirname, sep

    dir_of_file = dirname(abspath(__file__))
    sys.path.append(dirname(dirname(dirname(abspath(__file__)))))
    from scripts.cloudformation import CloudFormation
    from scripts.log import Log
    from document import get_document
    from jenkins import get_jenkins_instance

    clone = sys.argv[1].lower() == "true" if len(sys.argv) > 1 else False
    tenant = sys.argv[2] if len(sys.argv) > 2 else "tcc"
    region = sys.argv[3] if len(sys.argv) > 3 else "us-east-2"
    profile = sys.argv[4] if len(sys.argv) > 4 else "tcc"
    log_level = int(sys.argv[5], base=10) if len(sys.argv) > 5 else 3

    cloudformation = CloudFormation(profile, region, log_level)
    log = Log(log_level)
    exports = cloudformation.list_exports()
    document = get_document(cloudformation)
    jenkins = get_jenkins_instance(tenant=tenant, cloudformation=cloudformation)

    command = send_command(profile, region, jenkins, document, clone)
    with open(f"{dir_of_file}/command.output.json", "w") as f:
        f.write(json.dumps(command))

    command_id = command["Command"]["CommandId"]

    print(command_id)
