#!/bin/bash

repository=$1
casc=$2
plugins=$3

sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo dnf update –y && sudo dnf upgrade -y
sudo dnf install -y java-17-amazon-corretto-devel \
  fontconfig \
  jenkins \
  wget \
  curl \
  unzip \
  python3-pip \
  python3-devel
sudo dnf install kernel-devel -y
sudo dnf groupinstall "Development Tools" -y
sudo systemctl daemon-reload
sudo systemctl enable jenkins
sudo systemctl start jenkins
sudo mkdir /var/jenkins_home
chmod 777 /var/jenkins_home/
jenkins-plugin-cli -f $plugins
sudo mkdir -p $casc
cp $repository/config/jcasc.yaml $casc
sudo mkdir -p /usr/share/jenkins/ref/init.groovy.d
cp $repository/config/init.groovy.d/* /var/lib/jenkins/init.groovy.d/
export JAVA_OPTS="-Djenkins.install.runSetupWizard=false -Dcasc.jenkins.config=$casc"
sudo systemctl enable jenkins
sudo chkconfig jenkins on
sudo systemctl start jenkins
echo \"fim do script de setup\" >>/var/chegou_ao_fim.txt
