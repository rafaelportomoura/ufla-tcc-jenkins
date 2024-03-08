import org.jenkinsci.plugins.scriptsecurity.scripts.ScriptApproval

ScriptApproval.get().getPendingScripts().each { pendingScript ->
    ScriptApproval.get().approveScript(pendingScript.hash)
    println("Aprovado script pendente: ${pendingScript.script}")
}

ScriptApproval.get().getPendingSignatures().each { pendingSignature ->
    ScriptApproval.get().approveSignature(pendingSignature.signature)
    println("Aprovada assinatura pendente: ${pendingSignature.signature}")
}