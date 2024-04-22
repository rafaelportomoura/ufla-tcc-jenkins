def modules = load("${env.WORKSPACE}/scripts/infra.groovy")

// ACCOUNT PARAMETERS
String profile="default"
String region="us-east-2"
// ENV PARAMETERS
String stage="prod"
String tenant="tcc"
String stack_stage="Prod"
String stack_tenant="Tcc"
String job_folder="$stage"
// PIPE PARAMETERS
Boolean env_disable_pipes=false
String scm_cron="H/5 * * * *"
String codecommit="https://git-codecommit.us-east-2.amazonaws.com/v1/repos"
String default_branch = "origin/main"
String jenkins_repo_path="/var/repositories/ufla-tcc-jenkins"
String jenkins_scripts="${jenkins_repo_path}/scripts"
String python_version="python3.10"
// AWS CMDS
String aws="aws --profile ${profile} --region ${region}"
String deploy="${aws} cloudformation deploy --no-fail-on-empty-changeset --capabilities CAPABILITY_NAMED_IAM"

folder(job_folder) {
    displayName(stack_stage)
}

modules.Infra.job(this, job_folder, "vpc", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_version, "create_vpc.py")
modules.Infra.job(this, job_folder, "network", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_version, "create_network.py")
modules.Infra.job(this, job_folder, "domain", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_version, "create_domain.py")
modules.Infra.job(this, job_folder, "certificate", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_version, "create_certificate.py")
modules.Infra.job(this, job_folder, "package-bucket", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_version, "create_bucket.py")
