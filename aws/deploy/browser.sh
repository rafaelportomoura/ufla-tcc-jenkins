export_name=${2:-"tcc-jenkins-url"}
region=${3:-"us-east-2"}
profile=${4:-"tcc"}

get_dns() {
  aws --profile ${profile} --region ${region} cloudformation list-exports \
    --query "Exports[?Name=='${export_name}'].Value" \
    --output text
}

dns=$(get_dns)
if [ -z $dns ]; then
  echo "DNS not found"
  exit 1
fi

xdg-open $dns >/dev/null 2>&1
