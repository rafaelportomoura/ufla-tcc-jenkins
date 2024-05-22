folder(job_folder) {
    displayName(stack_stage + "-" + stack_tenant)
}

def after_vpc = "${job_folder}/vpc"
def after_domain = "${job_folder}/domain"
def after_domain_and_certificate = "${job_folder}/domain,${job_folder}/certificate"

Infra.no_dependencies(this, job_folder, "vpc", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_vpc.py")
Infra.email(this, job_folder, "email_identity", env_disable_pipes, codecommit, default_branch, jenkins_scripts, region, profile, python_exe, "create_email_identity.py")
Infra.no_dependencies(this, job_folder, "package-bucket", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_package_bucket.py")
Infra.no_dependencies(this, job_folder, "domain", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_domain.py")
Infra.no_dependencies(this, job_folder, "kms", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_kms.py")
Infra.after(this, job_folder, "network", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_network.py", after_vpc)
Infra.after(this, job_folder, "certificate", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_certificate.py", after_domain)
Infra.after(this, job_folder, "document-db", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_document_db.py", after_vpc)
Infra.after(this, job_folder, "image-bucket", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_image_bucket.py", after_domain_and_certificate)
Infra.after(this, job_folder, "rds", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, "create_rds.py", after_vpc)

def network_after = "${job_folder}/vpc,${job_folder}/network,${job_folder}/domain,${job_folder}/certificate,${job_folder}/package-bucket,${job_folder}/kms,${job_folder}/document-db,${job_folder}/image-bucket,${job_folder}/rds"

OAuth.job(this, job_folder, "oauth", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id, scm_cron, log_levels, network_after)
Products.job(this, job_folder, "products", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id, scm_cron, log_levels, network_after)
Stocks.job(this, job_folder, "stocks", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id, scm_cron, log_levels, network_after)
Orders.job(this, job_folder, "orders", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id, scm_cron, log_levels, network_after)
ContactBridge.job(this, job_folder, "contact-bridges", env_disable_pipes, codecommit, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id, scm_cron, log_levels, network_after)