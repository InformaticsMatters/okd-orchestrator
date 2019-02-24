#####################
Sharing Cluster State
#####################

**********
Background
**********

In order to instantiate cloud-based hardware the OKD Orchestrator relies on
`Terraform`_, an *infrastructure as code* provisioning tool by `HashiCorp`_.

**Terraform** is a powerful tool that uses a *declarative* language, i.e.
language where you tell it what you want and it does what's required,
in the right order, to satisfy your needs.

As a side-effect, **Terraform** creates *state files* in order to track the
objects it creates. These files are kept in the orchestrator's ``terraform``
directory and it's therefore extremely important not to remove them.
If lost Terraform will have difficulty adjusting or removing your cluster
hardware.

The disadvantage of storing state files in the ``terraform`` directory
is that only *you* can manage (and destroy) the cluster and, importantly,
you have to keep the files until you do destroy the cluster.

.. _hashicorp: https://www.hashicorp.com
.. _terraform: https://www.terraform.io

********************
Shared state storage
********************

Instead of storing state files on your workstation you can use Terraform's
built-in remote state storage and locking feature.

For a detailed discussion of state storage and locking refer
to Terraform's own comprehensive
`State Storage and Locking <https://www.terraform.io/docs/backends/state.html>`_
documentation.

======
On AWS
======

the OKD Orchestrator exposes the ability to store Terraform state in an AWS
S3 bucket [#f1]_. You do this by defining the ``terraform_shared_state``
properties in your deployment configuration.

Before you can use shared state storage you will need to create a bucket
on S3 and a related DynamoDB table, which provides
state locking (preventing concurrent cluster modifications).

You need to provide the following and add the details to your deployment
configuration. The properties are documented in the example
``compact-aws-frankfurt-3-11`` configuration

-   An S3 bucket (which is a unique name in AWS)
-   A key in the bucket (a name in your bucket)
-   A dynamo DB table with a *primary key* string called `LockID`.
    The table name and the database region goes into your configuration.

.. rubric:: Footnotes

.. [#f1] Other backend types may be supported in future releases.
