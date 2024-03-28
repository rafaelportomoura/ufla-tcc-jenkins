job('Config/node') {
  description ''
  parameters {
    stringParam('NodeVersion', '20')
    stringParam('DefaultPackageManager', 'pnpm')
  }
  steps {
    shell('cp -r /root/.nvm \$JENKINS_HOME/.nvm')
    shell('source \$JENKINS_HOME/.nvm/nvm.sh')
    shell('nvm install \$NodeVersion')
    shell('nvm use \$NodeVersion')
    shell('npm install -g \$DefaultPackageManager')
  }
}

// Main job creation block
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