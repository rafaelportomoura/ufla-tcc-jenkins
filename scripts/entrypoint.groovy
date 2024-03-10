import javaposse.jobdsl.dsl.DslFactory

// Define parameters
def params = [
    'NAME': 'tcc',
    'ENTRYPOINT_PATH': 'tcc/entrypoint.groovy',
    'GIT_REPOSITORY': 'https://git-codecommit.us-east-2.amazonaws.com/v1/repos/ufla-tcc-pipelines',
    'BRANCH': 'main',
    'SCM_CRON': 'H/30 * * * *'
]

// Main job creation block
folder(params['NAME']) {
    displayName(params['NAME'])
}
    
job("${params['NAME']}/entrypoint") {
    description ''
    parameters {
        stringParam('NAME', params['NAME'])
        stringParam('ENTRYPOINT_PATH', params['ENTRYPOINT_PATH'])
        stringParam('GIT_REPOSITORY', params['GIT_REPOSITORY'])
        stringParam('BRANCH', params['BRANCH'])
        stringParam('SCM_CRON', params['SCM_CRON'])
    }
    scm {
        git {
            remote {
                url(params['GIT_REPOSITORY'])
            }
            branch(params['BRANCH'])
        }
    }
    triggers {
        scm(params['SCM_CRON'])
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
            external(params['ENTRYPOINT_PATH'])
            removeAction('DELETE')
            removeViewAction('DELETE')
        }
    }
    publishers {
        wsCleanup {
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