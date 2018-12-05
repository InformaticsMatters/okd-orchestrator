################################
Compiling Machine Images for AWS
################################

.. highlight:: none

Before you start, as Yacker will be creating a small EC2 compute instance
upon which it will run the build, you will need suitable AWS API Keys
(See :doc:`getting-started-aws`) and these need to be available in your
provider environment script (e.g. ``setenv.sh``).

    For some cloud providers, like AWS, you may need to build images for each
    **region** that you want to create an OpenShift cluster in.
    Yacker can build images for as many regions as you like. You simply need a
    ``builders`` section for each region in the template file. The template files
    in our example build images for the **Frankfurt** region.

To build the OKD 3.9 machine images, set your environment variables and
launch the orchestrator container. You will not need to define all the
environment variables at this stage, only those required for compiling machine
images.

When you're ready run the following to start and enter the container
from the root of the project::

    $ ./orc-start.sh

If this is the first time you;re running the orchestrator the container image
will need to be downloaded from Docker. This might take a moment before
you eventually enter the container.

From the orchestrator container, move to the orchestration directory,
set your environment variables and validate the template files::

    $ cd okd-orchestrator
    $ source provider-env/setenv.sh
    $ cd yacker/3.9/aws
    $ yacker validate bastion.yaml
    $ yacker validate os.yaml

Then, if successful, build each image::

    $ yacker build bastion.yaml
    $ yacker build os.yaml

The builds may take a minute or two. At the end you should be presented with
an Amazon Machine Image ID (or AMI). Here's the example output for an
image that results in an AMI with the ID ``ami-01234567012345670``::

    ==> Builds finished. The artifacts of successful builds are:
    --> OpenShift 3.9 Base Image Frankfurt: AMIs were created:
    eu-central-1: ami-01234567012345670

Take the two AMIs you are presented with and place them in your provider
environment. For AWS these *AMIs* replace the existing values for::

   TF_VAR_aws_ami_os
   TF_VAR_aws_ami_bastion

You can stay in the container image and follow the :doc:`creating-your-cluster`
guide to create your cluster, but first return  to the project root from
the yacker directory::

    $ cd ../../..
