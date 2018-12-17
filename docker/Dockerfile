# A dockerfile to allow simplified (no-installation) execution
# of the OKD Orchestrator.
#
# The Docker image provides you with an OKD orchestrattion enviornment.
# You simply need to mount your orchestrator working dirctory
# (and SSH directory) into it and run image building and orchestration
# from within the container.
#
# You will need to define suitable environment variables for your
# cloud-provide and, when orchestrating the image IDs for the Bastion and
# Cluster nodes and the OpenShift initial admin account password.
#
# A typical container launch for AWS from your orchestrator directory
# would be: -
#
#   docker run -it \
#     -v `pwd`/..:/home/okdo/okd-orchestrator:Z \
#     --rm informaticsmatters/okd-orchestrator:stable /bin/bash
#
# Refer to the project's documention for a detailed discussion of
# the orchestrator.

FROM python:3.6.7

ARG terraform_version=0.11.11
ARG packer_version=1.3.3
ARG uid=40000
ARG gid=40000

# Install required system tools
COPY requirements.txt /tmp/
RUN apt-get -y update && \
    apt-get install -y jq unzip graphviz vim less && \
    pip install -r /tmp/requirements.txt

# Install Terraform
RUN curl https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_amd64.zip \
        --output /tmp/terraform.zip && \
    unzip /tmp/terraform.zip -d /usr/local/bin && \
    chmod 0755 /usr/local/bin/terraform

# Install Packer
RUN curl https://releases.hashicorp.com/packer/${packer_version}/packer_${packer_version}_linux_amd64.zip \
        --output /tmp/packer.zip && \
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
