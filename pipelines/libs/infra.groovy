class Infra {
  static no_dependencies(dslFactory, job_folder, name, is_disabled, git_url, git_default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, script) {
    dslFactory.job("${job_folder}/${name}") {
      disabled(is_disabled)
      logRotator(1, 5, 1, 5)
      triggers{
          scm("H/30 * * * *")
      }
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

  static after(dslFactory, job_folder, name, is_disabled, git_url, git_default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, script, after) {
    dslFactory.job("${job_folder}/${name}") {
      disabled(is_disabled)
      logRotator(1, 5, 1, 5)
      triggers{
          upstream(after, "SUCCESS")
      }
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