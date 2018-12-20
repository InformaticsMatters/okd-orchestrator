#!/usr/bin/env bash

# Builds a 'stable' docker image using your user and group IDs.
# Required on some systems in order to properly handle permissions
# in the volume mounted as the OKD working directory.
IMAGE_TAG=stable docker-compose build \
    --build-arg uid=$(id -u) \
    --build-arg gid=$(id -g)
