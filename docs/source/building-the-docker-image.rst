#########################
Building the Docker Image
#########################

The image used for the container to create your cluster is available
on `Docker Hub`_ and should work with MacOS.

The container image runs as the built-in user ``okdo`` using **User** and
**Group** IDs of ``40000``.

As the OKD Orchestrator working directory of your clone or fork of this
project is expected to be mounted within the container as a **volume**
you may have permission issues with some flavours of unix.

To get around this you can build your own container image using the
``build4me.sh`` script inside the ``docker`` directory. This script builds
the container image using the ``okdo`` user but with **User** and **Group**
ids that match yours::

    cd docker
    ./build4me.sh

Once built you can then use the project's ``okdo-start.sh`` script from the
project root to build your personalised copy of the image.

.. _Docker Hub: https://hub.docker.com/r/informaticsmatters/okd-orchestrator/
