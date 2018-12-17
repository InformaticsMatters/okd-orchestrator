#!/usr/bin/env bash

# Environment variables for AWS Cluster deployment.
#
# Copy as `setenv.sh`, edit and then install with `source setenv.sh`

# -----------------------------------------------------------------------------
# The following variables are required to compile machine images
# and orchestrate the cluster on the cloud provider
# -----------------------------------------------------------------------------

# AWS API access and secret keys.
# Required by the orchestrator to create resources on the cloud provider.
export TF_VAR_aws_access_key=SetMe
export TF_VAR_aws_secret_key=SetMe

# -----------------------------------------------------------------------------
# The following variables are required to orchestrate the cluster
# -----------------------------------------------------------------------------

# The SSH key-pair name known by the cloud provider.
# Instances will be created using this key-pair and you will
# need it to connect to them. You need to change this if you have
# used a different key-pair.
export TF_VAR_keypair_name=okdo-keypair

# Your Let's Encrypt/Certbot email address.
# `You need to set this is you are expecting the deployment
# to generate SSL certificates for your master instance.
# If you set the deployment's
export TF_VAR_master_certbot_email=SetMe

# -----------------------------------------------------------------------------
# The following variables are required to interact with OpenShift/OKD
# -----------------------------------------------------------------------------

# The password for the initial 'admin' and 'developer' accounts.
# These will be created on the cluster after the OKD software is installed.
# The admin password must be defined.
# The developer password can be blank if you do not want a developer account.
export TF_VAR_okd_admin_password=SetMe
export TF_VAR_okd_developer_password=

# -----------------------------------------------------------------------------
# The following (Optional) variables can be defined
# -----------------------------------------------------------------------------

# The path to your deployments directory. If not defined the default directory
# (deployments) will be used to locate the named deployment configuration.
#
# DO NOT: use '$HOME' or '~' if you're using the container
#         as these will translate to the container user's home directory,
#         not yours.
#
# You must use the fully qualified path if using the container to launch
# the cluster and have the environment variable defined
# before entering the container, i.e. you should have done something like
# 'source provider-env/setenv.sh` before `./okdo-start.sh.
#export TF_VAR_deployments_directory=/Users/me/okd-deployments
