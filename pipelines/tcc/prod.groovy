folder(job_folder) {
    displayName(stack_stage + "-" + stack_tenant)
}

Infra.job(this, job_folder, "vpc", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_version, "create_vpc.py")
Infra.job(this, job_folder, "network", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_version, "create_network.py")
Infra.job(this, job_folder, "domain", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_version, "create_domain.py")
Infra.job(this, job_folder, "certificate", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_version, "create_certificate.py")
Infra.job(this, job_folder, "package-bucket", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_version, "create_package_bucket.py")

OAuth.job(this, job_folder, "oauth", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_version, account_id)