class Products {
  static job(dslFactory, job_folder, name, is_disabled, git_url, git_default_branch, jenkins_scripts, stage, tenant, region, profile, python_exe, account_id) {
    dslFactory.job("${job_folder}/${name}-ecs") {
      disabled(is_disabled)
      logRotator(30, 10, 30, 10)
      parameters{
          choiceParam('LogLevel',['debug', 'verbose', 'info', 'log', 'warn', 'error'], 'Select compute services log level')
          stringParam('MinContainer', '1', 'Minimum number of containers')
          stringParam('MaxContainer', '1', 'Maximum number of containers')
          stringParam('ScaleOutCooldown', '60', 'Cooldown time to scale out')
          stringParam('ScaleInCooldown', '60', 'Cooldown time to scale in')
          stringParam('CpuUtilization', '70', 'CPU utilization to scale out')
      }
      scm {
        git {
          remote {
            url("${git_url}/ufla-tcc-products")
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
        cp $jenkins_scripts deploy/scripts -r
        ARGS="stage=$stage tenant=$tenant region=$region profile=$profile account_id=$account_id log_level_compute=\$LogLevel"
        ARGS="\$ARGS min_container=\$MinContainer max_container=\$MaxContainer"
        ARGS="\$ARGS scale_out_cooldown=\$ScaleOutCooldown scale_in_cooldown=\$ScaleInCooldown"
        ARGS="\$ARGS cpu_utilization=\$CpuUtilization"
        $python_exe deploy/create_ecs.py \$ARGS
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
    dslFactory.job("${job_folder}/${name}-ecr") {
      disabled(is_disabled)
      logRotator(30, 10, 30, 10)
      scm {
        git {
          remote {
            url("${git_url}/ufla-tcc-products")
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
        cp $jenkins_scripts deploy/scripts -r
        ARGS="stage=$stage tenant=$tenant region=$region profile=$profile account_id=$account_id"
        $python_exe deploy/create_ecr.py \$ARGS
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
  
    dslFactory.job("${job_folder}/${name}-network") {
      disabled(is_disabled)
      logRotator(30, 10, 30, 10)
      parameters{
          choiceParam('LogLevel',['debug', 'verbose', 'info', 'log', 'warn', 'error'], 'Select compute services log level')
          stringParam('AuthorizerResultTtlInSeconds', '300', 'Authorizer result time to live in seconds')
      }
      scm {
        git {
          remote {
            url("${git_url}/ufla-tcc-products")
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
        cp $jenkins_scripts deploy/scripts -r
        ARGS="stage=$stage tenant=$tenant region=$region profile=$profile log_level_compute=\$LogLevel"
        ARGS="\$ARGS  authorizer_result_ttl_in_seconds=\$AuthorizerResultTtlInSeconds"
        $python_exe deploy/create_network.py \$ARGS
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