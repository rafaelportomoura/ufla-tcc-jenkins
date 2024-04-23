import os 

class Docker:
    def __init__(self, ecr_uri: str, image: str, tag: str):
        self.ecr_uri = ecr_uri
        self.image = image
        self.tag = tag
    
    def build(self) -> None:
        os.system(f"docker build -t {self.image}:{self.tag} .")

    def push(self) -> None:
        os.system(f"docker tag {self.image}:{self.tag} {self.ecr_uri}/{self.image}:{self.tag}")
        os.system(f"aws ecr get-login-password | get docker login --username AWS --password-stdin {self.ecr_uri}")
        os.system(f"docker push {self.ecr_uri}/{self.image}:{self.tag}")
        
    @staticmethod
    def ecr_uri(account_id: str, region: str) -> str:
        return f"{account_id}.dkr.ecr.{region}.amazonaws.com"