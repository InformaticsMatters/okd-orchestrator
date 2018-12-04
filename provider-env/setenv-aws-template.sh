# Environment variables for AWS Cluster deployment.
#
# Copy as `setenv-aws.sh`, edit and then install with
# `source setenv-aws.sh`

export TF_VAR_aws_os_ami=SetMe
export TF_VAR_aws_bastion_ami=SetMe
export TF_VAR_aws_secret_key=SetMe
export TF_VAR_aws_access_key=SetMe

export TF_VAR_okd_admin_password=SetMe
