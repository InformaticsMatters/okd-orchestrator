#!/usr/bin/env bash

# With the docker image built,
# environment set with `source setenv-aws.sh`
# the OKD Orchestrator image can be run with this command...
docker run -it -v `pwd`/..:/okd \
    -e TF_VAR_aws_os_ami=${TF_VAR_aws_os_ami} \
    -e TF_VAR_aws_bastion_ami=${TF_VAR_aws_bastion_ami} \
    -e TF_VAR_aws_secret_key=${TF_VAR_aws_secret_key} \
    -e TF_VAR_aws_access_key=${TF_VAR_aws_access_key} \
    -e TF_VAR_okd_admin_password=${TF_VAR_okd_admin_password} \
    --rm okd-orchestrator:latest /bin/bash
