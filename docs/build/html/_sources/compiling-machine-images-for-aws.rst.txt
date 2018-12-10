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

To compile the OKD 3.9 machine images, set your environment variables and
launch the orchestrator container. You will not need to define all the
environment variables at this stage, only those required for compiling machine
images.

When you're ready run the following to start and enter the container
from the root of the project::

    $ ./okdo-start.sh

It is important to realise that the ``orc-start.sh`` script maps your
orchestrator working directory to the container directory
``$HOME/okd-orchestrator``, which is also the working directory when you
enter the container.

If this is the first time you're running the orchestrator the container image
will need to be downloaded from Docker. This might take a moment or two before
you eventually enter the container.

From the orchestrator container, move to the Yacker directory
and validate the OpensShift/OKD 3.9 template files::

    $ cd yacker/3.9/aws
    $ yacker validate bastion.yaml
    $ yacker validate os.yaml

Then, if successful, build each image::

    $ yacker build bastion.yaml
    $ yacker build os.yaml

The builds may take a minute or two. As long as you have not changed
the image ``ami_name`` variable the machine images (AMIs) Yacker creates
will be picked up automatically by the cluster orchestration.

You can stay in the container image and follow the :doc:`creating-your-cluster`
guide to create your cluster, but first return  to the project root from
the yacker directory::

    $ cd ../../..

Finding new base AWS Machine Images
-----------------------------------

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

This value should be used in an appropriate ``source_ami`` **builders**
section property in your Yacker YAML template file, where you will also
need to adjust the ``name`` and ``region`` properties accordingly.
