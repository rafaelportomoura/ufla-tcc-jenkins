aws ssm get-command-invocation \
  --profile ${4:-tcc} \
  --region ${3:-us-east-2} \
  --command-id "$2" \
  --instance-id $1
