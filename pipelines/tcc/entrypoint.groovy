// Carrega o script de utilidade
def createJob = evaluate(new File("pipelines/shared/createJob.groovy"))
def jenkins_repo = "https://git-codecommit.us-east-2.amazonaws.com/v1/repos/ufla-tcc-jenkins";
// Utiliza a função do script carregado
createJob("tcc/", "dev", jenkins_repo, "H/05 * * * *", "main", "echo 'Hello, World!'", {
    string('CLEANUP', 'false', 'Clean up the workspace?')
})
