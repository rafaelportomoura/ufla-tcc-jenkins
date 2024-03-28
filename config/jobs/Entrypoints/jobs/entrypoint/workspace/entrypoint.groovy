folder('env') {
  displayName('env')
}

job('env/config') {
  description ''
  parameters {
    string('NodeVersion', 'NodeVersion')
    string('DefaultPackageManager', 'pnpm')
  }
  steps {
    shell("RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash")
    shell('. \$JENKINS_HOME/.nvm/nvm.sh')
    shell('nvm install \$NodeVersion')
    shell('nvm user \$NodeVersion')
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