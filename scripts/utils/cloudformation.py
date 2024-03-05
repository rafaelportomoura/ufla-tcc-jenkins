import os
import json
import time
from typing import Any
from utils.log import Log

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

class CloudFormation:
    def __init__(self, profile: str, region: str, log_level=1) -> None: 
        self.log = Log(log_level=log_level)
        self.profile = profile
        self.region = region

    def deploy_stack(self, stack: dict[str, Any]) -> None:
        template = os.path.join(ROOT,stack['template'])
        stack_name = stack['stack_name']
        parameters = stack['parameters']
        self.log.checkpoint(f'Deploy of {stack_name}')
        self.deploy(template,stack_name,parameters)

    def delete_stack(self, stack_name: str) -> None: 
        self.log.checkpoint(f'Deleting {stack_name}')   
        cmd = self.__delete_stack(stack_name)
        self.log.cmd(cmd)
        os.system(f"{cmd} &> /dev/null")
    
    def check_if_stack_is_deleted(self,stack_name:str) -> bool:
        DELETE_FINAL_STATUS = ["DELETE_FAILED", "CREATE_COMPLETE", "UPDATE_COMPLETE"]
        
        try:
            stack = self.describe(stack_name)
            return False
        except Exception:
            return True
        


        # self.log.error(f"Deleting stack {stack_name}. The stack status is: {status}")
        # stacks = "Stacks" in stack 
        #     if (
                
        #         and len(stack["Stacks"]) > 0
        #         and "StackStatus" in stack["Stacks"][0]
        #     ):
        #         status = stack["Stacks"][0]["StackStatus"]
        #         if status == "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS":
        #             rollback_in_progress = True
        #         if rollback_in_progress and status == "UPDATE_ROLLBACK_COMPLETE":
        #             rollback_in_progress = False
        #             cmd = self.delete_stack(stack_name)
        #             os.system(f"{cmd} &> /dev/null")
            
        
    
    def package(self, template: str) -> str:
        output = "output.yaml"
        bucket = f"package-bucket-{self.region}"
        cmd = self.__package(bucket, template, output)
        os.system(f"{cmd} > /dev/null")
        return output

    def deploy(self, template: str, stack_name: str, parameters = {}) -> None:    
        cmd = self.__deploy(template,stack_name,parameters)
        self.log.cmd(cmd)
        os.system(cmd)
    
    def describe(self, stack_name: str) -> None:    
        cmd = self.__describe(stack_name)
        self.log.cmd(cmd)
        res = os.popen(cmd).read()
        return json.loads(res)
    
    def describe_stack_resources(self, stack_name: str):
        cmd = self.__describe_stack_resources(stack_name)
        self.log.cmd(cmd)
        cmd += " 2> /dev/null"
        res = os.popen(cmd).read()
        return json.loads(res)
    
    def list_exports(self):
        cmd = self.__prefix('list-exports')
        cmd += " 2> /dev/null"
        self.log.cmd(cmd)
        res = os.popen(cmd).read()
        return json.loads(res)
    
    def get_export_value(self, exports, name):
        exports = exports['Exports']
        for exported in exports:
            if name == exported['Name']:
                return exported['Value']
        self.log.error(f'Não foi possível obter o valor exportado: {name}')
        return None
    
    def get_output_value(self, stack: dict, key: str) -> str:
        outputs = stack["Stacks"][0]["Outputs"]
        return [x["OutputValue"] for x in outputs if x["OutputKey"] == key][0]

    def get_physical_resource_id(self, resources: dict, resource: str) -> str:
        return [
            x["PhysicalResourceId"] for x in resources if x["LogicalResourceId"] == resource
        ][0]
    
    def lint(self, template: str) -> None:
        os.system(f"cfn-lint {template}")

    def __prefix(self, cmd) -> str: 
        return f"aws --profile {self.profile} --region {self.region} cloudformation {cmd}"
    
    def __deploy(self, template, stack_name, parameters = {}) -> str:
        cmd = "deploy --no-fail-on-empty-changeset --capabilities CAPABILITY_NAMED_IAM"
        cmd += f" --template-file {template}"
        cmd += f" --stack-name {stack_name}"
        if isinstance(parameters, dict) and len(parameters.keys()) > 0:
            cmd += " --parameter-overrides"
            for key in parameters:
                cmd += f" '{key}={parameters[key]}'"
        return self.__prefix(cmd)

    def __describe(self, stack_name) -> str:
        cmd = f"describe-stacks --stack-name {stack_name}"
        return self.__prefix(cmd)

    def __describe_stack_resources(self, stack_name) -> str:
        cmd = f"describe-stack-resources --stack-name {stack_name}"
        return self.__prefix(cmd)
    
    def __delete_stack(self, stack_name) -> str:
        return self.__prefix(f"delete-stack --stack-name {stack_name}")
    
    def __package(self, bucket, template, output) -> str:
        cmd = "package"
        cmd += f" --template-file {template}"
        cmd += f" --output-template-file {output}"
        cmd += f" --s3-bucket {bucket}"
        return self.__prefix(cmd)

