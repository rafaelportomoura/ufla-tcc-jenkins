import os


class Docker:
    @staticmethod
    def build_and_push(
        ecr_uri: str, image: str, tag: str, region: str, profile: str = None
    ) -> None:
        profile = f"--profile {profile}" if profile and profile != "default" else ""
        os.system(
            f"docker build -t {ecr_uri}/{image}:{tag} . \
                  && aws {profile} --region {region} ecr get-login-password | get docker login --username AWS --password-stdin {ecr_uri} \
                  && docker push {ecr_uri}/{image}:{tag}"
        )

    @staticmethod
    def ecr_uri(account_id: str, region: str) -> str:
        return f"{account_id}.dkr.ecr.{region}.amazonaws.com"
