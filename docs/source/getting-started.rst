###############
Getting Started
###############

***************
Essential parts
***************

The orchestrator is designed to simplify the construction of an OpenShift
cluster on various cloud providers using **deployments** - high-level
configuration files written in `YAML`_. The deployment configurations are
described in the :doc:`deployment-configurations` section of the documentation.

At the moment we have working solutions for Amazon *EC2*, *OpenStack* and
*GCE* and a working example for *EC2* that we use as a tutorial.

    If this is your first time using the OKD Orchestrator make sure you've
    visited the :doc:`orientation` document, it guides you through the
    concepts of the orchestrator with a worked example on AWS.

The tools required by the orchestrator are packaged into a convenient
Docker image that you can run on your laptop or desktop. The essential
tools you *will* need are: -

-  **Git** (and a fork of the OKD Orchestrator repository)
-  **Docker**

Git
===

In order to use the orchestrator, an open source software project, you will
need the `Git`_ version control system installed. Using Git you should start
with a clone of a **fork** of the orchestrator project. A fork is preferred
because you may need to make changes to the configuration files or
create your own configurations.

#. Install Git
#. Visit the `orchestrator repository`_. Fork it and clone it to your
   development host.

You will be working from the clone of this project so start by navigating to
the root of your working copy.

.. _Git: https://git-scm.com
.. _Orchestrator Repository: https://github.com/InformaticsMatters/okd-orchestrator
.. _YAML: https://yaml.org

Docker
======

We use `Docker`_ because it is a tool designed to make it easier to create,
deploy, and run applications by using containers. Containers allow a developer
to package up an application with all of the parts it needs, such as libraries
and other dependencies, and ship it all out as one package.

#. Install Docker. You can refer to Docker's installation guide,
   which includes guides for various platforms.

We have been using Docker **18.09.0** but any recent version should be
suitable.

..  toctree::
    :maxdepth: 1
    :caption: See:

    deployment-configurations
    advanced/building-the-docker-image
    advanced/running-without-docker

.. _docker: https://www.docker.com
.. _installation guide: https://docs.docker.com/install/

************************
Getting Started with AWS
************************

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
-------

If you do not have an **AWS Account** visit https://aws.amazon.com where you can
sign-up.

API Access Keys
---------------

**Access Keys** and are described on the Amazon `Access Keys`_
page. You will need environment AWS-compliant environment variables defined::

    AWS_ACCESS_KEY
    AWS_SECRET_KEY

SSH Key Pair
------------

You can generate a key-pair that does not use a pass phrase for this example
using the ``ssh-keygen`` tool::

    $ ssh-keygen -f okdo-keypair -t rsa -b 2048 -N '' -C okdo-keypair

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

************************
Getting Started with GCE
************************

Provider Environment Variables
==============================

A number of parameters are required by the orchestrator. These are
defined in a cloud-provider-specific *template* file in the ``provider-env``
directory.

Copy ``setenv-gce-template.sh`` as ``setenv.sh``. You'll be using this file
throughout this example.

Account Preparation
===================

You should have a project in your GCE account that you want to use for the
OKD installation. You will need to download the credentials as a JSON file,
this is described in the
`Packer documentation <https://www.packer.io/docs/builders/googlecompute.html>`_

You use different types of security credentials depending on how you
interact with GCE and, in order to use the orchestrator, you will need: -

-   A **GCE account** for the Compute Engine
-   A project-based **credentials file**, a JSON file provided by Google that
    allows the orchestrator to make programmatic calls to the GCE API
    on your behalf
-   An **SSH Key Pair** that you and the OKD Orchestrator can use to create
    and access GCE objects.

Account
-------

If you do not have an **GCE Account** visit https://cloud.google.com where
you can sign-up.

Credentials File
----------------

You should place your credentials file in the root of the OKD Orchestrator
project clone. Name your credentials file ``gce-credentials.json`` and save
it in the root directory of the OKC Orchestrator clone (or fork). This file
will be used to create machine images with **Yacker** and instantiate the
cluster using **Terraform**.

SSH Key Pair
------------

You can generate a key-pair that does not use a pass phrase for this example
using the ``ssh-keygen`` tool::

    $ ssh-keygen -f okdo-keypair -t rsa -b 2048 -N '' -C centos

The keypairs (a private ``okdo-keypair`` and public ``okdo-keypair.pub`` file)
should be present in the root of the orchestrator project, not in your
``.ssh`` directory.

You should then upload the public (``.pub``) part to your GCE account
under ``Compute Engine -> Metadata -> SSH Keys`` for the given project.

Place the name of the keypair in your ``setenv.sh``. The value
should replace the existing value for::

    TF_VAR_keypair_name

Considerations
==============

-   Unlike the AWS deployment the GCE deployment does not use an internal
    subnet for OKD nodes. Consequently all physical nodes have a
    public-fading IP address.
-   All instances are created in zone **a**.

*********************
Building your Cluster
*********************

To build your cluster you will need to compile the base images for AWS
before create your cluster.

-  When you're ready, follow the instructions for AWS in the
   :doc:`compiling-machine-images` guide
-  With base images compiled, you're ready to create the OKD cluster,
   all of which is covered in the :doc:`creating-your-cluster` guide

Project and Credentials
=======================

*******************
Public IP Addresses
*******************

In all providers you will need static/fixed IP addresses that your domain
can map to to provide access to the *console API* and *applications*.

You will therefore need one or two pre-allocated **External IP addresses**
in your desired region depending on whether you're deploying a compact
(combined master/infra node) or standard (separate master and infra nodes).

The allocated IP address values become values for the following configuration
items in your deployment. In GCE this is simply the allocated IP addresses,
in AWS it's the floating IP identity. Here's the configuration setting
for an example GCE setup::

    cluster:
      master:
        fixed_ip_id: 35.198.72.215
      infra:
        fixed_ip_id: 35.198.131.227

