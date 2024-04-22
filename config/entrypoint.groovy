String pipelines_path = 'pipelines'
String codecommit="https://git-codecommit.us-east-2.amazonaws.com/v1/repos"
String default_branch = "origin/main"
String cron_expression = "H/05 * * * *"
String entrypoint_folder ="entrypoints"
String config_folder="config"
String python_version="python3.10"

folder(entrypoint_folder) {
    displayName('Entrypoints')
}

job("${entrypoint_folder}/tcc-prod") {
    scm {
        git {
            remote {
                url("${codecommit}/ufla-tcc-jenkins")
            }
            branch(default_branch)
        }
    }
    triggers {
        scm(cron_expression)
    }
    steps {
        shell("${python_version} ${pipelines_path}/tcc/prod.py")
        dsl {
            external("${pipelines_path}/tcc/prod.groovy")
            removeAction('DELETE')
            removeViewAction('DELETE')
        }
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


folder(config_folder) {
    displayName('Config')
}
    

job("${config_folder}/nodejs") {
    parameters{
        stringParam('NODE_VERSION', '20', 'Node version')
    }
    steps {
        shell("""
            curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash 
            . \$HOME/.nvm/nvm.sh 
            nvm install \$NODE_VERSION 
            nvm use \$NODE_VERSION
            npm install -g pnpm
        """)
    }
}

job("${config_folder}/git") {
    steps {
        shell("""
            git config --global credential.helper '!aws codecommit credential-helper \$@'
            git config --global credential.UseHttpPath true
        """)
    }
}

job("${config_folder}/git_pull") {
    parameters{
        stringParam('REPO_PATH', '/var/repositories/ufla-tcc-jenkins')
        stringParam('BRANCH', 'main')
    }
    triggers{
        cron(cron_expression)
    }
    steps {
        shell("""
            git config --global --add safe.directory /var/repositories/ufla-tcc-jenkins
            cd \$REPO_PATH
            git checkout \$BRANCH
            git pull
        """)
    }
}