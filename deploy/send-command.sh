# =========================================== SCRIPT ===============================================
aws ssm send-command \
  --profile ${4:-tcc} \
  --region ${3:-us-east-2} \
  --instance-ids $1 \
  --document-name jenkins-document \
  --parameters "Clone='${2:-False}'"
