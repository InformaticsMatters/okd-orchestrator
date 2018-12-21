########################
Getting Started with AWS
########################

At this stage, although we'll be working with a built-in example,
you may need to make some changes to the configuration files in order to
create your own cluster from them. It's therefore essential that you
work on a clone of your own **fork** of the OKD Orchestrator.
You will then be able to commit the changes you make and start to craft
your own deployment configurations without being disturbed by changes in this,
the upstream project.

Here we're going to deploy an example OKD 3.11 release on a small cluster at
AWS. The deployment configuration is called ``compact-aws-frankfurt-3-11``.

The orchestrator will be creating the the cluster network,
the cluster and installing OpenShift/OKD, all from within a Docker container
hosting the orchestrator's run-time tools.

At the end we'll tear-down the cluster using the orchestrator.

    Some familiarity with with the Amazon **Elastic Compute Cloud**,
    commonly referred to as `EC2`_, is assumed here and costs will
    be incurred when following this example.

    If you are not familiar with EC2, Amazon's `What Is Amazon EC2`_ page
    provides comprehensive documentation.

Before you can create Amazon (AWS) resources you will need to prepare an
**EC2 Account**.

Provider Environment Variables
==============================

A number of parameters are required by the orchestrator. These are
defined in a cloud-provider-specific *template* file in the ``provider-env``
directory.

Copy ``setenv-aws-template.sh`` as ``setenv.sh``. You'll be using this file
throughout this example.

Account Preparation
===================

You use different types of security credentials depending on how you
interact with AWS and, in order to use the orchestrator, you will need: -

-   An **AWS account** that allows you to sign in to the AWS Management Console
-   **API Access keys** that allow the orchestrator to make programmatic calls to
    the AWS API on your behalf
-   An **SSH Key Pair** that you and the OKD Orchestrator can use to create
    and access EC2 objects.

Account
^^^^^^^

If you do not have an **AWS Account** visit https://aws.amazon.com where you can
sign-up.

API Access Keys
^^^^^^^^^^^^^^^

**Access Keys** and **Key Pairs** are described on the Amazon `Access Keys`_
page. You will need both the access ``key`` and the corresponding ``secret``
value.

Put the access ``key`` and ``secret`` in your ``setenv.sh`` script.
These should replace any existing values for::

    TF_VAR_aws_access_key
    TF_VAR_aws_secret_key

SSH Key Pair
^^^^^^^^^^^^

You can generate a key-pair that does not use a pass phrase for this example
using the ``ssh-keygen`` tool::

    $ ssh-keygen -f okdo-keypair -t rsa -b 2048 -N ''

The keypair should be present in the root of the orchestrator project,
not in your ``.ssh`` directory.

You should then upload the public (``.pub``) part to your AWS account.
You will need to upload the key-pair to each `region`_ that you intend to use.
Our example assumes you'll be deploying to **Frankfurt**.

Place the name of the keypair in your ``setenv.sh``. The value
should replace the existing value for::

    TF_VAR_keypair_name

.. _Access Keys: https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys
.. _EC2: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html
.. _Region: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html
.. _What Is Amazon EC2: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html

Building your Cluster
=====================

To build your cluster you will need to compile the base images for AWS
before create your cluster.

-  When you're ready, follow the instructions for AWS in the
   :doc:`compiling-machine-images` guide
-  With base images compiled, you're ready to create the OKD cluster,
   all of which is covered in the :doc:`creating-your-cluster` guide
