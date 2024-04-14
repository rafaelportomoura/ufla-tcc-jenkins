String pipelines_path = 'pipelines/tcc'


def scmConfig(
    String repo = 'https://git-codecommit.us-east-2.amazonaws.com/v1/repos/ufla-tcc-jenkins',
    String branch='main'
) {
    scm {
        remote {
            url(repo)
        }
        branch('main')
    }
}

def triggerConfig() {
    triggers {
        scm('H/05 * * * *')
    }
}

def publisherConfig() {
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
    $triggerConfig()
    $scmConfig()
    steps {
        dsl {
            external("${pipelines_path}/dev.groovy")
            removeAction('DELETE')
            removeViewAction('DELETE')
        }
    }
    $publisherConfig()
}
