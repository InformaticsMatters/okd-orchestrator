#!/usr/bin/env bash

# Start, and enter the OKD Orchestration container.
# If the TF_VAR_deployments_directory variable is set then
# we mount that into the container...

if [ -z "$TF_VAR_deployments_directory" ]
then
    # No user-specific deployments directory
    docker run -it \
        -v `pwd`:/home/okdo/okd-orchestrator:Z \
        --rm informaticsmatters/okd-orchestrator:stable /bin/bash
else
    # A user-specific deployments directory
    docker run -it \
        -v ${TF_VAR_deployments_directory}:${TF_VAR_deployments_directory}:Z \
        -v `pwd`:/home/okdo/okd-orchestrator:Z \
        --rm informaticsmatters/okd-orchestrator:stable /bin/bash
fi
