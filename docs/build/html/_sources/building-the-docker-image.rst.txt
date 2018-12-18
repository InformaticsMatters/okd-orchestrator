#########################
Building the Docker Image
#########################

Building the official image
===========================

The official image is built using docker-compose and documented in the
``docker-compose.yml`` file. To build (and then push) the ``latest`` image
run::

    $ docker-compose build
    $ docker-compose push

To build (and then push) the official ``stable`` image run::

    $ IMAGE_TAG=stable docker-compose build
    $ IMAGE_TAG=stable docker-compose push

Building your own image
=======================

The official image used for the container to create your cluster is available
on `Docker Hub`_ and should work with MacOS and Unix.

The container image runs as the built-in user ``okdo`` using **User** and
**Group** IDs of ``40000``.

As the OKD Orchestrator working directory of your clone or fork of this
project is expected to be mounted within the container as a **volume**
you may have permission issues with some flavours of unix.

To get around this you can build your own container image using the
``docker4me.sh`` script in the project root. This script builds
the container image using the ``okdo`` user but with **User** and **Group**
ids that match yours::

    ./docker4me.sh

Once built you can then use the project's ``okdo-start.sh`` script from the
project root to use your personalised copy of the image.

.. _Docker Hub: https://hub.docker.com/r/informaticsmatters/okd-orchestrator/
