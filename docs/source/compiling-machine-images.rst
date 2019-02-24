########################
Compiling Machine Images
########################

************
Introduction
************

.. highlight:: none

The OKD cluster (and its Bastion) are formed from hardware
provided by your cloud provider. As the base image for each of our
physical machines needs some pre-installed software it's often
easier to compile a dedicated base image that all our compute instances
will use.

Once an image has been compiled for a cloud provider region it can be used
for any number of clusters for that provider's region.

To compile images we use `yacker`_ a YAML wrapper for `packer`_,
a HashiCorp tool dedicated to the the automated construction of machine images.

.. epigraph::

   **Yacker** configurations are defined *template* files written in YAML.
   Without going into great detail the files consist of ``variables``,
   ``builders`` and ``provisioners`` sections.

   The ``provisioners`` section contains the list of instructions that are
   executed on top of a base images. The cloud-specific details are held
   in the ``builders`` section and the ``variables`` provide some dynamic control.

The image templates are located in the ``yacker`` project directory
where you'll find templates organised according to OKD release and
cloud provider. For example, the OpenShift 3.11 AWS EC2 templates for the
Bastion and OpenShift cluster nodes can be found in the ``yacker/3.11/aws``
directory.

.. _yacker: https://pypi.org/project/matildapeak-yacker/
.. _packer: https://www.packer.io

********************************
Compiling Machine Images for AWS
********************************

Before you start, as Yacker will be creating a small EC2 compute instance
upon which it will run the build, you will need suitable AWS API Keys
and these need to be available in your provider environment script
(e.g. ``setenv.sh``).

    For some cloud providers, like AWS, you may need to build images for each
    **region** that you want to create an OpenShift cluster in.
    Yacker can build images for as many regions as you like. You simply need a
    ``builders`` section for each region in the template file. The template files
    in our example build images for the **Frankfurt** region.

Validate
========

To compile the OKD 3.11 machine images, set your environment variables and
launch the orchestrator container. You will not need to define all the
environment variables at this stage, only those required for compiling machine
images.

When you're ready run the following to start and enter the container
from the root of the project::

    $ ./okdo-start.sh

It is important to realise that the ``okdo-start.sh`` script maps your
orchestrator working directory to the container directory
``$HOME/okd-orchestrator``, which is also the working directory when you
enter the container.

If this is the first time you're running the orchestrator the container image
will need to be downloaded from Docker. This might take a moment or two before
you eventually enter the container.

From the orchestrator container you can validate the OpensShift/OKD 3.11
template files::

    $ yacker validate yacker/3.11/aws/bastion.yaml
    $ yacker validate yacker/3.11/aws/okd.yaml

Build
=====

Once validated, build each image::

    $ yacker build yacker/3.11/aws/bastion.yaml
    $ yacker build yacker/3.11/aws/okd.yaml

The builds may take a minute or two. As long as you have not changed
the image ``ami_name`` variable the machine images (AMIs) Yacker creates
will be picked up automatically by the cluster orchestration.

>   You do not need to create the bastion image if your deployment's **Master**
    instance is also acting as the Bastion machine. The Bastion machine image
    is only required if you're creating a dedicated Bastion in the cluster.

You can stay in the container image and follow the :doc:`creating-your-cluster`
guide to create your cluster.

Finding new base AWS Machine Images
===================================

The base image AMI that your Yacker template files use depends on the AWS
region you wish to deploy your cluster to. The orchestrator images
are based on an official CentOS Linux image. The example configuration uses
the *FREE TIER* CentOS 7 image version **1805_01** that is available in
Frankfurt called **"CentOS 7 (x86_64) - with Updates HVM"** (``ami-dd3c0f36``).

When creating Yacker templates for other regions you will need a compatible
CentOS 7 image.

You can use the ``aws`` command-line utility in the orchestration
container to find images on AWS. The command needs your API keys,
passed to it during configuration::

    $ aws configure

You only need to provide your access and secret keys. The default region
and output format can be left at **None**.

Once configured you can find the AMI for **"Canada (Central)"**
(``ca-central-1``) with the following command::

    $ aws --region ca-central-1 \
        ec2 describe-images --owners aws-marketplace \
        --filters Name=product-code,Values=aw0evgkw8e5c1q413zgy5pjce \
        --filters Name=description,Values="CentOS Linux 7 x86_64 HVM EBS ENA 1805_01" \
        | jq -r '.Images[0].ImageId'
    ami-e802818c

This value can be used on the command-line to execute a **builder**
for an image in that region. For example, the following can be added to the
yacker command to build images for the specific regions
(valid February 2019) [#f1]_: -

*   ``-var 'aws_region=us-east-1' -var 'aws_source_ami=ami-9887c6e7'``
*   ``-var 'aws_region=us-east-2' -var 'aws_source_ami=ami-9c0638f9'``
*   ``-var 'aws_region=us-west-1' -var 'aws_source_ami=ami-4826c22b'``
*   ``-var 'aws_region=us-west-2' -var 'aws_source_ami=ami-3ecc8f46'``
*   ``-var 'aws_region=ap-south-1' -var 'aws_source_ami=ami-1780a878'``
*   ``-var 'aws_region=ap-northeast-1' -var 'aws_source_ami=ami-8e8847f1'``
*   ``-var 'aws_region=ap-northeast-2' -var 'aws_source_ami=ami-bf9c36d1'``
*   ``-var 'aws_region=ap-southeast-1' -var 'aws_source_ami=ami-8e0205f2'``
*   ``-var 'aws_region=ap-southeast-2' -var 'aws_source_ami=ami-d8c21dba'``
*   ``-var 'aws_region=ca-central-1' -var 'aws_source_ami=ami-e802818c'``
*   ``-var 'aws_region=eu-west-1' -var 'aws_source_ami=ami-3548444c'``
*   ``-var 'aws_region=eu-west-2' -var 'aws_source_ami=ami-00846a67'``
*   ``-var 'aws_region=eu-west-3' -var 'aws_source_ami=ami-262e9f5b'``
*   ``-var 'aws_region=eu-north-1' -var 'aws_source_ami=ami-b133bccf'``
*   ``-var 'aws_region=sa-east-1' -var 'aws_source_ami=ami-cb5803a7'``

As an example, to build the base OKD base image for Singapore
(``ap-southeast-1``) you would run::

    $ yacker build \
        -var 'aws_region=ap-southeast-1' -var 'aws_source_ami=ami-8e0205f2' \
        yacker/3.11/aws/okd.yaml


.. rubric:: Footnotes

.. [#f1] Does not include Asia Pacific (Osaka-Local), China or GovCloud

********************************
Compiling Machine Images for GCE
********************************

To compile the OKD 3.11 machine images, set your environment variables and
launch the orchestrator container. You will not need to define all the
environment variables at this stage, only those required for compiling machine
images.

When you're ready run the following to start and enter the container
from the root of the project::

    $ ./okdo-start.sh

It is important to realise that the ``okdo-start.sh`` script maps your
orchestrator working directory to the container directory
``$HOME/okd-orchestrator``, which is also the working directory when you
enter the container.

If this is the first time you're running the orchestrator the container image
will need to be downloaded from Docker. This might take a moment or two before
you eventually enter the container.

From the orchestrator container you can validate the OpensShift/OKD 3.11
template files::

    $ yacker validate yacker/3.11/gce/bastion.yaml
    $ yacker validate yacker/3.11/gce/okd.yaml

Build
=====

Once validated, build each image::

    $ yacker build yacker/3.11/gce/bastion.yaml
    $ yacker build yacker/3.11/gce/okd.yaml

The builds may take a minute or two. As long as you have not changed
the image ``ami_name`` variable the machine images (AMIs) Yacker creates
will be picked up automatically by the cluster orchestration.

>   You do not need to create the bastion image if your deployment's **Master**
    instance is also acting as the Bastion machine. The Bastion machine image
    is only required if you're creating a dedicated Bastion in the cluster.

You can stay in the container image and follow the :doc:`creating-your-cluster`
guide to create your cluster.
