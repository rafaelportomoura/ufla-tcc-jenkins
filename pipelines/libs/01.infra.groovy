class Infra {
  static job(dslFactory, name, is_disabled, git_url, git_default_branch, script) {
    dslFactory.job("${job_folder}/${name}") {
      disabled(is_disabled)
      logRotator(30, 10, 30, 10)
      scm {
        git {
          remote {
            url("${git_url}/ufla-tcc-infra")
          }
          branch(git_default_branch)
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