String pipelines_path = 'pipelines/tcc'
String codecommit="https://git-codecommit.us-east-2.amazonaws.com/v1/repos"
String branch = "*/main"
String scm_cron = "H/05 * * * *"
String entrypoint_folder ="entrypoints/tcc"

folder('tcc') {
    displayName('Tcc')
}
folder('tcc/Prod') {
    displayName('Prod')
}
def scmConfig(String repo) {
    job.scm {
        git {
            remote {
                url("${codecommit}/${repo}")
            }
            branch(branch)
        }
    }
}

job("${entrypoint_folder}/prod") {
    scmConfig("ufla-tcc-jenkins")
    triggers {
        scm(scm_cron)
    }
    steps {
        dsl {
            external("${pipelines_path}/prod.groovy")
            removeAction('DELETE')
            removeViewAction('DELETE')
            remove
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
