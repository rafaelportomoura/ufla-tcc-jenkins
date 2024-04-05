folder('Tcc') {
    displayName('Tcc')
}
    
job('Tcc/entrypoint') {
    scm {
        git {
            remote {
                url('https://git-codecommit.us-east-2.amazonaws.com/v1/repos/ufla-tcc-jenkins')
            }
            branch('main')
        }
    }
    wrappers {
        preBuildCleanup {
            includePattern('**/target/**')
            deleteDirectories()
            cleanupParameter('CLEANUP')
        }
    }
    steps {
        dsl{
            external('pipelines/tcc/entrypoint.groovy')
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


job('Config/nodejs') {
    parameters{
        stringParam('NODE_VERSION', '20', 'Node version')
    }
    steps {
        sh("source \$HOME/.nvm/nvm.sh && nvm install \$NODE_VERSION && nvm use \$NODE_VERSION")
        sh("npm install -g pnpm")
    }
}

job('Config/git') {
    steps {
        sh("""
            git config --global credential.helper '!aws codecommit credential-helper \$@'
            git config --global credential.UseHttpPath true
        """)
    }
}