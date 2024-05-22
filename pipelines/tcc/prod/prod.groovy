folder(job_folder) {
    displayName(stack_stage + "-" + stack_tenant)
}

Infra.no_dependencies(this, job_folder, "vpc", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_vpc.py")
Infra.after_vpc(this, job_folder, "network", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_network.py")
Infra.no_dependencies(this, job_folder, "domain", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_domain.py")
Infra.after_domain(this, job_folder, "certificate", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_certificate.py")
Infra.no_dependencies(this, job_folder, "package-bucket", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_package_bucket.py")
Infra.no_dependencies(this, job_folder, "kms", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_kms.py")
Infra.after_vpc(this, job_folder, "document-db", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_document_db.py")
Infra.after_domain(this, job_folder, "image-bucket", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_image_bucket.py")
Infra.after_vpc(this, job_folder, "rds", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_rds.py")
OAuth.job(this, job_folder, "oauth", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id, scm_cron, log_level)
Products.job(this, job_folder, "products", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id, scm_cron, log_level)
Stocks.job(this, job_folder, "stocks", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id, scm_cron, log_level)
Orders.job(this, job_folder, "orders", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id, scm_cron, log_level)
ContactBridge.job(this, job_folder, "contact-bridges", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id, scm_cron, log_level)