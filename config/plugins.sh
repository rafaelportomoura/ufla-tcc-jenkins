dns=$1
auth=$2
cli=${3:-"/var/repositories/ufla-tcc-jenkins/config/jenkins-cli.jar"}
plugins=${4:-"/var/repositories/ufla-tcc-jenkins/config/plugins.txt"}

if [ -z $auth ]; then
  echo "Auth not found"
  exit 1
fi

install_plugin() {
  plugin=$1
  echo "Installing plugin $plugin"
  java -jar $cli -s $dns install-plugin $plugin
}

while IFS= read -r line; do
  install_plugin $line
done <$plugins
