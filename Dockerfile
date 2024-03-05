# Stage de Construção
FROM jenkins/jenkins:2.447-jdk21 as builder

USER root

RUN apt-get update && apt-get install -y sudo wget curl unzip lsb-release build-essential python3-pip

RUN curl -L -O https://github.com/aws-cloudformation/cfn-lint/archive/refs/tags/v0.86.0.zip && \
  unzip v0.86.0.zip

RUN cd cfn-lint-0.86.0 && python3 setup.py clean --all && \
  python3 setup.py install


# Instalação do Node.js e outras ferramentas
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash && \
  . "/root/.nvm/nvm.sh" && nvm install 20 && npm install -g pnpm

# Instalação do Docker CLI
RUN curl -fsSLo /usr/share/keyrings/docker-archive-keyring.asc https://download.docker.com/linux/debian/gpg && \
  echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.asc] https://download.docker.com/linux/debian $(lsb_release -cs) stable" > /etc/apt/sources.list.d/docker.list && \
  apt-get update && apt-get install -y docker-ce-cli

# Instalação do AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" && \
  unzip /tmp/awscliv2.zip -d /tmp && \
  /tmp/aws/install

# Limpeza
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY config/jcasc.yaml /var/jenkins_home/jcasc.yaml
COPY config/plugins.txt /var/jenkins_home/plugins.txt

USER jenkins
# Stage Final
FROM jenkins/jenkins:2.447-jdk21
COPY --from=builder --chown=jenkins:jenkins /var/jenkins_home /var/jenkins_home
COPY --from=builder --chown=jenkins:jenkins /root/.nvm /root/.nvm
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /usr/local/aws-cli /usr/local/aws-cli

RUN chown -R jenkins:jenkins /var/jenkins_home && chmod -R 777 /var/jenkins_home

USER jenkins
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false
ENV CASC_JENKINS_CONFIG /var/jenkins_home/jcasc.yaml
RUN jenkins-plugin-cli -f /var/jenkins_home/plugins.txt

ENV PATH="/usr/local/aws-cli/v2/current/bin:${PATH}"

CMD ["/bin/bash", "/usr/local/bin/jenkins.sh"]
