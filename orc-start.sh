#!/usr/bin/env bash

# Start, and enter the orchestration container...
docker run -it \
    -v `pwd`:/home/okdo/okd-orchestrator \
    -v ~/.ssh:/home/okdo/.ssh \
    --rm informaticsmatters/okd-orchestrator:stable /bin/bash
