#!/usr/bin/env bash

# Environment variables for JGU Cluster deployment.
#
# Copy as `setenv.sh`, edit and then install with `source setenv.sh`

# -----------------------------------------------------------------------------
# The following variables are required to use S3 state storage.
# -----------------------------------------------------------------------------

export AWS_ACCESS_KEY=SetMe
export AWS_SECRET_KEY=SetMe

# -----------------------------------------------------------------------------
# The following variables are required to orchestrate the cluster
# -----------------------------------------------------------------------------

# The SSH key-pair name known by the cloud provider and expected to be located
# in the root of this project. If you use 'okdo-keypair' (the default name)
# the project's .gitignore will prevent it from being committed to the
# repository. The private part fo the keypair file needs to have this name
# and be located in the orchestrator project's root directory.
#
# Cloud compute instances will be created using this key-pair and you will
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
# 'source provider-env/setenv.sh' before './okdo-start.sh'.
#export TF_VAR_deployments_directory=/Users/me/okd-deployments
