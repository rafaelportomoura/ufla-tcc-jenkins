// ACCOUNT PARAMETERS
String profile="default"
String region="us-east-2"
// ENV PARAMETERS
String stage="prod"
String tenant="tcc"
String stack_stage="Prod"
String stack_tenant="Tcc"
String job_folder="$tenant/$stage"
// PIPE PARAMETERS
Boolean env_disable_pipes=false
String scm_cron="H/5 * * * *"
String codecommit="https://git-codecommit.us-east-2.amazonaws.com/v1/repos"
String default_branch = "origin/main"
String jenkins_repo_path="/var/repositories/ufla-tcc-jenkins"
String jenkins_scripts="${jenkins_repo_path}/scripts"
// AWS CMDS
String aws="aws --profile ${profile} --region ${region}"
String deploy="${aws} cloudformation deploy --no-fail-on-empty-changeset --capabilities CAPABILITY_NAMED_IAM"

folder(job_folder) {
    displayName(stack_stage)
}

job("${job_folder}/package-bucket") {
    disabled(env_disable_pipes)
    scm {
        git {
            remote {
                url("${codecommit}/ufla-tcc-infra")
            }
        }
    }
  wrappers {
        preBuildCleanup {
            deleteDirectories()
            cleanupParameter('CLEANUP')
        }
    }
    steps {
        shell("""
STACK_NAME="${stack_tenant}-${stack_stage}-Package-Bucket"
$deploy --template-file aws/s3/package_bucket.yaml --stack-name $STACK_NAME
        """)
    }
    publishers {
        cleanWs {
            cleanWhenAborted(true)
            cleanWhenFailure(true)
            cleanWhenNotBuilt(false)
            cleanWhenSuccess(true)
            cleanWhenUnstable(true)
            deleteDirs(true)
            notFailBuild(true)
            disableDeferredWipeout(true)
            patterns {
                pattern {
                    type('EXCLUDE')
                    pattern('.propsfile')
                }
                pattern {
                    type('INCLUDE')
                    pattern('.gitignore')
                }
            }
        }
    }
}

job("${job_folder}/infra") {
    disabled(env_disable_pipes)
    parameters {
        stringParam('SCRIPT_PATH', 'scripts', 'Script path')
        stringParam('ENTRYPOINT', 'scripts/deploy.py', 'Entrypoint')
    }
    scm {
        git {
            remote {
                url("${codecommit}/ufla-tcc-infra")
            }
        }
    }
  wrappers {
        preBuildCleanup {
            deleteDirectories()
            cleanupParameter('CLEANUP')
        }
    }

    steps {
        shell("""
        cp $jenkins_scripts \$SCRIPT_PATH/utils -r
        python3 $ENTRYPOINT stage=$stage tenant=$tenant region=$region profile=$profile
        """)
    }
    publishers {
        cleanWs {
            cleanWhenAborted(true)
            cleanWhenFailure(true)
            cleanWhenNotBuilt(false)
            cleanWhenSuccess(true)
            cleanWhenUnstable(true)
            deleteDirs(true)
            notFailBuild(true)
            disableDeferredWipeout(true)
            patterns {
                pattern {
                    type('EXCLUDE')
                    pattern('.propsfile')
                }
                pattern {
                    type('INCLUDE')
                    pattern('.gitignore')
                }
            }
        }
    }
}
