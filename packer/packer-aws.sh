#!/usr/bin/env bash

# A convenient utility to run packer (yacker) on all the AWS images.

set -e

cd 3.9/aws/machine-image
YACKER_PACKER_DIR=~/bin yacker build template.yaml
cd ../../..
