# Stage de Construção
FROM jenkins/jenkins:2.448-jdk21 as builder

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

USER jenkins
COPY --chown=jenkins:jenkins ./config/plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli -f /usr/share/jenkins/ref/plugins.txt

COPY --chown=jenkins:jenkins ./config/jcasc.yaml /jenkins/casc_configs/jcasc.yaml
COPY --chown=jenkins:jenkins ./scripts/entrypoint.groovy /var/scripts/entrypoint.groovy
COPY --chown=jenkins:jenkins ./config/jobs /var/jenkins_home/jobs/

USER root
RUN cp -r /root/.nvm /var/jenkins_home/.nvm
RUN chmod -R 755 /usr/local/aws-cli
RUN chmod -R 755 /var/scripts
RUN chmod -R +x /var/scripts
RUN chown jenkins:jenkins -R /var/jenkins_home && chmod -R 777 /var/jenkins_home
RUN chown jenkins:jenkins -R /var/scripts

USER jenkins
ENV JAVA_OPTS -Djenkins.install.runSetupWizard=false -Dcasc.jenkins.config=/jenkins/casc_configs

ENV PATH="/usr/local/aws-cli/v2/current/bin:${PATH}"

CMD ["/bin/bash", "/usr/local/bin/jenkins.sh"]
