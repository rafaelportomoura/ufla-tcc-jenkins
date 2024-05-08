folder(job_folder) {
    displayName(stack_stage + "-" + stack_tenant)
}

Infra.job(this, job_folder, "vpc", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_vpc.py")
Infra.job(this, job_folder, "network", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_network.py")
Infra.job(this, job_folder, "domain", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_domain.py")
Infra.job(this, job_folder, "certificate", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_certificate.py")
if (region != 'us-east-1') {
    Infra.job(this, job_folder, "us-east-1-certificate", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_us_east_1_certificate.py")
}
Infra.job(this, job_folder, "package-bucket", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_package_bucket.py")
Infra.job(this, job_folder, "kms", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_kms.py")
Infra.job(this, job_folder, "document-db", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_document_db.py")
OAuth.job(this, job_folder, "oauth", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id)
Products.job(this, job_folder, "products", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id)