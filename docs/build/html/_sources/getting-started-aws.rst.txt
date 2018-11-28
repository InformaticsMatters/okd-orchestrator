########################
Getting Started with AWS
########################

.. highlight:: none

At this stage, although we'll be working with a built-in example
you will need to make some minor changes to the files in order to
create your own cluster from them. It's therefore essential that you
work on a clone of your own *fork* of the OKD Orchestrator.
You will then be able to commit the changes you make and start to craft
your own deployments without being disturbed by changes in this, the
upstream project.

Here we're going to deploy the built-in OKD 3.9 release on a small cluster at
AWS. The deployment configuration is called ``simple-aws-frankfurt-3-9``.

We will be creating a small (``t2.small``) Bastion node from where we'll
deploy the OKD cluster using one *Master* node, one *Infrastructure* node and
one *Compute* node.

Once done we'll tear-down the Cluster and the Bastion.

    Some familiarity with with the Amazon **Elastic Compute Cloud**,
    commonly referred to as `EC2`_, is assumed here and costs will
    be incurred when following this example.

    If you are not familiar with EC2, Amazon's `What Is Amazon EC2`_ page
    provides comprehensive documentation.

Before you can create Amazon (AWS) resources you will need to prepare an
**EC2 Account** and, for the example cluster, two **Elastic IP** instances that
the orchestrator will attach to the *Master* and *Infrastructure* nodes.

Account Preparation
===================

You use different types of security credentials depending on how you
interact with AWS and, in order to use the orchestrator, you will need: -

-   An **AWS account** that allows you to sign in to the AWS Management Console
-   **API Access keys** that allow the orchestrator to make programmatic calls to
    the AWS API on your behalf
-   An **SSH Key Pair** that you and the OKD Orchestrator can use to create
    and access EC2 objects. If you don't want to make too many changes to the
    example then create a Key Pair named ``aws-keypair``.

Account
^^^^^^^

If you do not have an **AWS Account** visit https://aws.amazon.com where you can
sign-up.

API Access Keys
^^^^^^^^^^^^^^^

**Access Keys** and **Key Pairs** are described on the Amazon `Access Keys`_
page. You will need both the access ``key`` and the corresponding ``secret``
value.

Create and export two environment variables for the access keys. These will
be used by the ``terraform`` utility when creating your cluster::

    export TF_VAR_aws_access_key=<myAccessKey>
    export TF_VAR_aws_secret_key=<mySecretKy>

SSH Key Pair
^^^^^^^^^^^^

You can generate a key-pair that does not use a pass phrase for this example
using the ``ssh-keygen`` tool::

    ssh-keygen -f ~/.ssh/aws-keypair -t rsa -b 2048 -N ''

You should then upload the public (``.pub``) part to your AWS account.
You will need to upload the key-pair to each `region`_ that you intend to use.
Our example assumes you'll be deploying to ``Frankfurt``.

.. _Access Keys: https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-and-secret-access-keys
.. _EC2: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html
.. _Region: https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html
.. _What Is Amazon EC2: https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/concepts.html

Elastic IP Preparation
======================

You will need to create two *Elastic IPs*, one that will be used by the
orchestrator as the public IP address of the OpenShift *Master* node and the
other for the *Infrastructure* node.

You can create Elastic IPs form the AWS EC2 dashboard.

In the region that you'll be creating the cluster
(``Frankfurt`` in this example), create two Elastic IP instances. The IPs that
have been assigned are not of particular use to the orchestrator but the
**Allocation IDs** are.

    The IDs will begin ``eipalloc-`` followed by, typically, a 16-digit hex
    number.

For clarity you might want to provide a ``Name`` for each IP. One will be
associated for the **Master** OpenShift node and one will be associated with
the **Infrastructure** node. It might be beneficial to given them these names.

The assigned IDs need to placed in the **deployment** file, in this example
the file we're using is ``deployments/simple-aws-frankfurt-3.9.yaml``.

Edit the deployment file and replace the ``master1.fixed_ip_id`` and
``infra1.fixed_ip_id`` values with your EIP allocation IDs. Then, replace the
``public_hostname`` and ``cluster.router_basename`` with the IPs from
the Master and Infra IDs respectively.

    Remember that Elastic IPs not attached to EC2 instances incur a small cost.
    Once you have finished with the example cluster you may want to remove
    these objects from your EC2 account.

Normally you would have access to a domain through which you want to access
your cluster, ``mycluster.com`` for example. Instead of placing the IP
addresses in the ``public_hostname`` and ``cluster.router_basename`` you would
normally route two sub-domains to those IPs. If you do theses domaain names
would be used for the ``public_hostname`` and ``cluster.router_basename``,
i.e. `openshift.mycluster.com`` and ``apps.mycluster.com``. For this example
we'll stick to the Elastic IP values.

Building a machine image
========================

The final preparation step for AWS requires the building of base images for
your cluster, the identities of which are copied into your deployment
configuration.

When you're ready, follow the AWS instructions in the
:doc:`building-machine-images` guide.

Once complete, with a machine image built and its ID in your deployment
configuration, you're ready to launch your Bastion and an OKD cluster,
all of which is covered in the :doc:`creating-your-cluster` guide.
