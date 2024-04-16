#!/bin/bash

repository=${1-"/var/repositories/ufla-tcc-jenkins"}

sudo wget --quiet -O /etc/yum.repos.d/jenkins.repo \
  https://pkg.jenkins.io/redhat-stable/jenkins.repo
sudo rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io-2023.key
sudo dnf update –y --quiet && sudo dnf upgrade -y --quiet
sudo dnf install -y --quiet java-17-amazon-corretto-devel \
  fontconfig \
  jenkins \
  unzip \
  python3-pip \
  python3-devel \
  kernel-devel \
  bzip2-devel \
  libffi-devel \
  openssl-devel
sudo dnf groupinstall "Development Tools" -y --quiet
echo "INSTALLED DEPENDENCIES"
sudo systemctl daemon-reload
sudo systemctl enable jenkins
sudo chkconfig jenkins on
sudo systemctl start jenkins
echo "JENKINS STARTED"
git config --global --add safe.directory $repository
sudo chmod 777 --recursive $repository/.git
sudo chown -R jenkins:jenkins $repository
sudo echo \"fim do script de setup\" >>$HOME/chegou_ao_fim.txt
