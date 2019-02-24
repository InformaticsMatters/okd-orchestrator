#!/usr/bin/env bash

# Set environment variables and run the ssh-agent.
# The user is assumed to have created a setenv.sh script
# using a suitable template as a starting point.
# Importantly the TF_VAR_keypair_name must be set to the name
# of a private keyfile in the root of the orchestrator directory.

source ${HOME}/okd-orchestrator/provider-env/setenv.sh
eval $(ssh-agent) > /dev/null
ssh-add ${HOME}/okd-orchestrator/${TF_VAR_keypair_name} 2> /dev/null
