#######################
Building Machine Images
#######################

.. highlight:: none

The OKD cluster (and its Bastion machine) are formed from hardware
provided by your cloud provider. As the base image for each of our
physical machines needs some pre-installed software it's often
easier to build a dedicated base image that all our compute instances
will use.

To do this we use `packer`_, a HashiCorp tool dedicated to the the
automated construction of machine images.

The images we create, more specifically a Unique ID that is used to refer to
them, are written to the deployment configuration file. If you're
building AWS images for the simple example this would be
``deployments/simple-aws-frankfurt-3.9.yaml``

**Packer** configurations are defined *template* files written in JSON.
Without going into great detail the files consist of ``variables``,
``builders`` and ``provisioners`` sections.

The ``provisioners`` section contains the list of instructions that are
executed on top of a base images. The cloud-specific details are held
in the ``builders`` section and the ``variables`` provide some dynamic control.

The Packer templates are located in the ``packer`` project directory
where you'll find templates organised according to OKD release and
cloud provider. For example, the AWS EC2 template for OpenShift/3.9
can be found in the ``packer/3.9/aws/machine-image`` directory. This image
is valid for any OKD 3.9 deployment on AWS and may be shared between
deployments.

.. _packer: https://www.packer.io

Building Machine Images for AWS
===============================

Before you start, as Packer will be creating a small EC2 compute instance
upon which it will run the build, you will need suitable AWS API Keys
(See :doc:`getting-started-aws`). These need to be defined in the following
environment variables::

    export TF_VAR_aws_access_key=<myAccessKey>
    export TF_VAR_aws_secret_key=<mySecretKy>

To build the OKD 3.9 machine image, navigate to the appropriate template
directory and run the following packer command, which will validate the
template file::

    cd packer/3.9/aws/machine-image
    packer validate template.json

Then, if successful, start the build::

    packer build template.json

This may take a minute or two but, at the end you should be presented with
an Amazon Machine Image ID (or AMI) in at the output of the packer build.
Here's the example output for ``ami-01234567012345670``::

    ==> Builds finished. The artifacts of successful builds are:
    --> OpenShift 3.9 Base Image Frankfurt: AMIs were created:
    eu-central-1: ami-01234567012345670

Packer, in a single execution, can build images for as many regions as you
like. You simply need a ``builders`` section for each region. At the moment
the packer file in our example simply builds an image for the Frankfurt region.

Copy the ``ami`` identity (including the leading ``ami-``) and replace the
values for the ``bastion.machine_image.id`` and ``cluster.machine_image.id``
in your deployment configuration.
