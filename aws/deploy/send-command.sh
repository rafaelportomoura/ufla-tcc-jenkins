# =========================================== SCRIPT ===============================================
aws ssm send-command \
  --profile ${5:-tcc} \
  --region ${4:-us-east-2} \
  --instance-ids $1 \
  --document-name $2 \
  --parameters "Clone='${3:-False}'"
