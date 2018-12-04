# A dockerfile to allow simplified (no-installation)
# execution of the OKD Orchestrator. The user is required to
# build the docker image (as it needs to contain their provate keyfile.
#
# The Docker image provides the OKD execution enviornment,
# the user simply needs to mount their OKD working dirctory into it and
# run from there.
#
# The user will need: -
#
# - The AMIs for the Bastion and Cluster nodes
# - Their AWS credentials
# - Their private cluster SSH keypair file
#
# To build the docker image: -
#
# The private keyfile used for the cloud-provider should be placed
# in this direcxtory and needs tobe called `keyfile`. then, the image
# can be built with docker-compose: -
#
#   docker-compose build
#
# Because the image conatins a private keyfile the user should
# not publish the image to a public respository.
#
# A typical container launch for AWS from this docker directory would be,
# if they've set their enviornment variables: -
#
#   docker run -it -v `pwd`/..:/okd \
#     -e TF_VAR_aws_os_ami=${TF_VAR_aws_os_ami} \
#     -e TF_VAR_aws_bastion_ami=${TF_VAR_aws_bastion_ami} \
#     -e TF_VAR_aws_secret_key=${TF_VAR_aws_secret_key} \
#     -e TF_VAR_aws_access_key=${TF_VAR_aws_access_key} \
#     -e TF_VAR_okd_admin_password=${TF_VAR_okd_admin_password} \
#     --rm okd-orchestrator:latest /bin/bash
#
# Then, from within the container the user can build
# the cluster (typically from their host) with: -
#
#   ./create.py --cluster

FROM python:3.6.7

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

# Install some required tools
RUN apt-get -y update && \
    apt-get install -y unzip graphviz

# Install Terraform
RUN curl https://releases.hashicorp.com/terraform/0.11.10/terraform_0.11.10_linux_amd64.zip --output /tmp/terraform.zip && \
    unzip /tmp/terraform.zip -d $HOME/bin && \
    chmod 0700 $HOME/bin/terraform

# Install Packer
RUN curl https://releases.hashicorp.com/packer/1.3.2/packer_1.3.2_linux_amd64.zip --output /tmp/packer.zip && \
    unzip /tmp/packer.zip -d $HOME/bin && \
    chmod 0700 $HOME/bin/packer

# The SSH key.
# Expected to be called 'keypair' in this directory.
# COpied to ~/.ssh/id_<type> (i.e. ~/.ssh/id_rsa)
ARG keypair=keypair
ARG keypair_type=rsa
WORKDIR /root/.ssh
COPY ${keypair} ./id_${keypair_type}
RUN chmod 0600 ./id_${keypair_type}

# Anticipated working directory.
# The user's orchestrator is expected to be mounted here.
WORKDIR /okd

## Force the binary layer of the stdout and stderr streams
# to be unbuffered
ENV PYTHONUNBUFFERED 1
