import os
from scripts import stacks
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


def jenkins_stack_name(tenant: str) -> str:
    return stacks.stack_name(tenant=tenant, name="Jenkins")


def generate_key() -> dict[str, str]:
    directory = os.path.dirname(__file__)
    keys_path = f"{directory}/keys"
    pub_path = f"{keys_path}/jenkins.pub"
    private_path = f"{keys_path}/jenkins"
    os.path.exists(keys_path) or os.makedirs(keys_path)
    if os.path.exists(pub_path) and os.path.exists(private_path):
        with open(pub_path, "r") as f:
            public_key = f.read()
        with open(private_path, "r") as f:
            private_key = f.read()
        public_key = public_key.replace("\n", "")
        private_key = private_key.replace("\n", "")
        return {"public_key": public_key, "private_key": private_key}
    key = rsa.generate_private_key(
        backend=crypto_default_backend(), public_exponent=65537, key_size=1200
    )
    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.OpenSSH,
        crypto_serialization.NoEncryption(),
    )
    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH, crypto_serialization.PublicFormat.OpenSSH
    )
    public_key = public_key.decode("utf-8")
    with open(pub_path, "w") as f:
        f.write(public_key)
    public_key = public_key.replace("\n", "")
    private_key = private_key.decode("utf-8")
    with open(private_path, "w") as f:
        f.write(private_key)
    private_key = private_key.replace("\n", "")
    return {"public_key": public_key, "private_key": private_key}


def jenkins(
    tenant: str,
    vpc: str,
    subnet: str,
    amiid: str = "",
    instance_type: str = "",
) -> stacks.Stack:
    key = generate_key()
    return stacks.Stack(
        os.sep.join(["aws", "jenkins.yaml"]),
        jenkins_stack_name(tenant=tenant),
        {
            "VpcId": vpc,
            "SubnetId": subnet,
            "AmiId": amiid,
            "InstanceType": instance_type,
            "Tenant": tenant,
            "SgInitIp": os.popen("curl --silent https://api.ipify.org").read(),
            "PublicKey": key["public_key"],
        },
        tenant,
    )


def get_jenkins_instance(tenant: str, cloudformation) -> str:
    exports = cloudformation.list_exports()
    jenkins = cloudformation.get_export_value(exports, f"{tenant}-jenkins-instance")
    return jenkins


def get_jenkins_url(tenant: str, cloudformation) -> str:
    exports = cloudformation.list_exports()
    jenkins = cloudformation.get_export_value(exports, f"{tenant}-jenkins-url")
    return jenkins


def get_jenkins_dns(tenant: str, cloudformation) -> str:
    exports = cloudformation.list_exports()
    dns = cloudformation.get_export_value(exports, f"${tenant}-jenkins-instance-dns")
    return dns


def document_stack_name() -> str:
    return stacks.stack_name(name="Document-Run-Container")
