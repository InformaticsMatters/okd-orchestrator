# Environment variables for AWS Cluster deployment.
#
# Copy as `setenv.sh`, edit and then install with
# `source setenv.sh`

# -----------------------------------------------------------------------------
# The following variables are required to compile machine images
# and orchestrate the cluster
# -----------------------------------------------------------------------------

# AWS API access and secret keys.
# Required by the orchestrator to create AWS resources.
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

# THe AWS AMIs for the Bastion and OpenShift cluster nodes
export TF_VAR_aws_ami_os=SetMe
export TF_VAR_aws_ami_bastion=SetMe

# Your Let's Encrypt/Certbot email address.
# `You need to set this is you are expecting the deployment
# to generate SSL certificates for your master instance.
# If you set the deployment's
export TF_VAR_master_certbot_email=SetMe

# -----------------------------------------------------------------------------
# The following variables are required to install OpenShift
# -----------------------------------------------------------------------------

# The password for the initial admin account
# that wil be created on the OpenShift cluster.
export TF_VAR_okd_admin_password=SetMe
