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
            branches(params['BRANCH'])
            scriptPath(params['ENTRYPOINT_PATH'])
        }
    }
    triggers {
        scm(params['SCM_CRON'])
    }
    steps {
        dslScript {
            external(params['ENTRYPOINT_PATH'])
        }
    }
    publishers {
        wsCleanup {
            patterns {
                pattern('.propsfile', 'EXCLUDE')
                pattern('.gitignore', 'INCLUDE')
            }
            deleteDirs(false)
        }
    }
}