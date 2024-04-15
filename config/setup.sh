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
  libffi-devel
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
sudo echo \"fim do script de setup\" >>/var/chegou_ao_fim.txt

sudo cd /tmp
sudo wget --quiet https://www.python.org/ftp/python/3.10.12/Python-3.10.12.tgz
sudo tar -xzf Python-3.10.12.tgz
cd Python-3.10.12
./configure --enable-optimizations --prefix=/usr/local
make -j 2
sudo make altinstall
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.10 get-pip.py
sudo echo \"fim do script de python\" >>/var/chegou_ao_fim.txt
