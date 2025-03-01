// ACCOUNT PARAMETERS
String profile="default"
String region="us-east-2"
String account_id="076005165667"
// ENV PARAMETERS
String stage="prod"
String tenant="tcc"
String stack_stage="Prod"
String stack_tenant="Tcc"
String job_folder="${stage}-${tenant}"
// PIPE PARAMETERS
Boolean env_disable_pipes=false
String scm_cron="H/5 * * * *"
String codecommit="https://git-codecommit.us-east-2.amazonaws.com/v1/repos"
String default_branch = "origin/main"
String jenkins_repo_path="/var/repositories/ufla-tcc-jenkins"
String jenkins_scripts="${jenkins_repo_path}/scripts"
String python_exe="python3.10"
def log_levels = ['debug', 'verbose', 'info', 'log', 'warn', 'error'] as List