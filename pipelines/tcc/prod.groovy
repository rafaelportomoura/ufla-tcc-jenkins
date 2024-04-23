folder(job_folder) {
    displayName(stack_stage + "-" + stack_tenant)
}

Infra.job(this, "vpc", env_disable_pipes, codecommit, default_branch, "create_vpc.py")
Infra.job(this, "network", env_disable_pipes, codecommit, default_branch, "create_network.py")
Infra.job(this, "domain", env_disable_pipes, codecommit, default_branch, "create_domain.py")
Infra.job(this, "certificate", env_disable_pipes, codecommit, default_branch, "create_certificate.py")
Infra.job(this, "package-bucket", env_disable_pipes, codecommit, default_branch, "create_package_bucket.py")

OAuth.job(this, "oauth", env_disable_pipes, codecommit, default_branch)