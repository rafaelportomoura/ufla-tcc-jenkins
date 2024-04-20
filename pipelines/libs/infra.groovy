class Infra {
  static job(dslFactory, job_folder, name, disabled, git_url, default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, script) {
    dslFactory.job("${job_folder}/${name}") {
      disabled(disabled)
      logRotator(30, 10, 30, 10)
      scm {
        git {
          remote {
            url("${git_url}/ufla-tcc-infra")
          }
          branch(default_branch)
        }
      }
      wrappers {
        colorizeOutput('xterm')
        preBuildCleanup {
          deleteDirectories()
          cleanupParameter('CLEANUP')
        }
      }
      steps {
        shell("""
        cp $jenkins_scripts scripts/scripts -r
        ARGS="stage=$stage tenant=$tenant region=$region profile=$profile"
        $python_exe scripts/${script} \$ARGS
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
        }
      }
    }
  }
}