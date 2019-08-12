# A dockerfile to allow simplified (no-installation) execution
# of the OKD Orchestrator.
#
# The Docker image provides you with an OKD orchestrattion enviornment.
# You simply need to mount your orchestrator working dirctory
# (and SSH directory) into it and run image building and orchestration
# from within the container. You can start an denter the container
# using the convenient project script: -
#
#   ./okdo-start.sh
#
# You will need to define suitable environment variables for your
# cloud-provide and, when orchestrating the image IDs for the Bastion and
# Cluster nodes and the OpenShift initial admin account password.
#
# Refer to the project's documention for a detailed discussion of
# the orchestrator.

FROM python:3.7.4

ARG terraform_version=0.11.14
ARG packer_version=1.4.2
ARG uid=40000
ARG gid=40000

# Install required system tools.
# - apache2-utils is required for 'htpasswd', used during OKD metrics installation
# - default-jdk is required for 'keytool', used during OKD metrics installation
COPY requirements.txt /tmp/
RUN apt-get -y update && \
    apt-get install -y jq unzip graphviz vim less \
        apache2-utils default-jdk && \
    pip install -r /tmp/requirements.txt --default-timeout=60

# Install Terraform
RUN curl https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_amd64.zip \
        --output /tmp/terraform.zip \
        --connect-timeout 60 \
        --max-time 300 && \
    unzip /tmp/terraform.zip -d /usr/local/bin && \
    chmod 0755 /usr/local/bin/terraform

# Install Packer
RUN curl https://releases.hashicorp.com/packer/${packer_version}/packer_${packer_version}_linux_amd64.zip \
        --output /tmp/packer.zip \
        --connect-timeout 60 \
        --max-time 300 && \
    unzip /tmp/packer.zip -d /usr/local/bin && \
    chmod 0755 /usr/local/bin/packer

# Containers should NOT run as root
# (as good practice)
#
ENV HOME /home/okdo
RUN groupadd --gid ${gid} --force okdo && \
    useradd --shell /bin/bash --gid ${gid} --uid ${uid} --home-dir ${HOME} okdo

WORKDIR ${HOME}/okd-orchestrator
COPY bashrc ${HOME}/.bashrc
RUN chown -R ${uid}.${gid} ${HOME}
USER ${uid}

ENV LANG C
ENV LC_ALL C
ENV LANGUAGE C

# Force the binary layer of the stdout and stderr streams
# to be unbuffered
ENV PYTHONUNBUFFERED 1
