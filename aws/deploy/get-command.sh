aws ssm get-command-invocation \
  --profile ${4:-tcc} \
  --region ${3:-us-east-2} \
  --command-id "$1" \
  --instance-id $2
