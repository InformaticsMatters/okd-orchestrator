#!/usr/bin/env bash

# Set environment variables and tun the ssh-agent.
# The user is assumed to have created a setenv.sh script a suitable template.
# Importantly the TF_VAR_keypair_name must be set to a private keyfile name.

source ${HOME}/okd-orchestrator/provider-env/setenv.sh
eval $(ssh-agent) > /dev/null
ssh-add ${HOME}/okd-orchestrator/${TF_VAR_keypair_name} 2> /dev/null
