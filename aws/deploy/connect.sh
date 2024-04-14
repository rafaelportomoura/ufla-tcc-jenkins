tenant=${1:-"tcc"}
export_name=${2:-"${tenant}-jenkins-instance-dns"}
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
dir=$(dirname $0)
chmod 400 "$dir/keys/jenkins"
ssh -i "$dir/keys/jenkins" ec2-user@${dns}
