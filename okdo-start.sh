#!/usr/bin/env bash

# Start, and enter the OKD Orchestration container...
docker run -it \
    -v `pwd`:/home/okdo/okd-orchestrator:Z \
    --rm informaticsmatters/okd-orchestrator:stable /bin/bash
