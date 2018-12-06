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
#     -v ~/.ssh:/home/okdo/.ssh \
#     --rm informaticsmatters/okd-orchestrator:stable /bin/bash
#
# Refer to the project's documention for a detailed discussiomn of
# the orchestrator.

FROM python:3.6.7

# Base directory for the application
# Also used for user directory
ENV HOME /home/okdo

# Containers should NOT run as root
# (as good practice)
RUN useradd --shell /bin/bash --user-group --uid 6000 --home-dir ${HOME} okdo

# Install required system tools
COPY requirements.txt /tmp/
RUN apt-get -y update && \
    apt-get install -y jq unzip graphviz vim && \
    pip install -r /tmp/requirements.txt

# Install Terraform
ARG terraform_version=0.11.10
RUN curl https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_amd64.zip \
        --output /tmp/terraform.zip && \
    unzip /tmp/terraform.zip -d /usr/local/bin && \
    chmod 0755 /usr/local/bin/terraform

# Install Packer
ARG pacxker_version=1.3.2
RUN curl https://releases.hashicorp.com/packer/${pacxker_version}/packer_${pacxker_version}_linux_amd64.zip \
        --output /tmp/packer.zip && \
    unzip /tmp/packer.zip -d /usr/local/bin && \
    chmod 0755 /usr/local/bin/packer

RUN chown -R okdo.okdo ${HOME}
RUN chmod -R a+wrx ${HOME}
USER okdo
WORKDIR ${HOME}

ENV LANG C
ENV LC_ALL C
ENV LANGUAGE C

# Force the binary layer of the stdout and stderr streams
# to be unbuffered
ENV PYTHONUNBUFFERED 1
