#!/usr/bin/env bash

# Builds a 'stable' docker image using your user and group IDs.
# Required on some systems in order to properly handle permissions
# in the volume mounted as the OKD working directory.
docker build \
    --build-arg uid=$(id -u) \
    --build-arg gid=$(id -g) \
    --tag informaticsmatters/okd-orchestrator:stable \
    .
