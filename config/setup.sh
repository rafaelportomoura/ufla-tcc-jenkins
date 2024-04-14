#!/bin/bash

repository=${1-"/var/repositories/ufla-tcc-jenkins"}
casc=${2-"/var/jenkins_home/casc_configs"}

sudo wget -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo dnf update –y && sudo dnf upgrade &&
  sudo dnf install -y java-17-amazon-corretto-devel \
    fontconfig \
    jenkins \
    wget \
    curl \
    unzip \
    python3-pip \
    python3-devel \
    kernel-devel &&
  sudo dnf groupinstall "Development Tools" &&
  sudo mkdir /var/jenkins_home
chmod 777 /var/jenkins_home/
sudo mkdir -p $casc
cp $repository/config/jcasc.yaml $casc
sudo mkdir -p /usr/share/jenkins/ref/init.groovy.d
cp $repository/config/init.groovy.d/* /var/lib/jenkins/init.groovy.d/
export JAVA_OPTS="-Djenkins.install.runSetupWizard=false -Dcasc.jenkins.config=$casc"
sudo systemctl daemon-reload
sudo systemctl enable jenkins
sudo chkconfig jenkins on
sudo systemctl start jenkins
echo "JENKINS STARTED"
jenkins-plugin-cli -f $repository/config/plugins.txt
echo \"fim do script de setup\" >>/var/chegou_ao_fim.txt
