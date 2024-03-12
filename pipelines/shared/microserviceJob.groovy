

def microserviceJob(String folder, String name, String repository, String scm, String branch, String shell, def params) {
    job(folder + name) {
        scm {
            git {
                remote {
                    url(repository)
                }
                branch(branch)
            }
        }
        parameters = params
        wrappers {
            preBuildCleanup {
                includePattern('**/target/**')
                deleteDirectories()
                cleanupParameter('CLEANUP')
            }
        }
        steps {
          sh(shell)
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
}