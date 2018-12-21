#############################
Deploying to Your Own Cluster
#############################

So you have your own hardware, it's all setup and you want to take
advantage of the OKD orchestrator to simplify the installation of
the OKD container platform. Here you just need to provide the
details of your cluster in a short `YAML`_ section of the deployment file.

.. _yaml: https://yaml.org

Prerequisites
=============

Before you can use the orchestrator on your own cluster you must satisfy
the system and environment requirements defined in the OKD official
documentation. For v3.11 this can be found `here`_.

Additionally, in case it's not obvious...

-   Your cluster must have access to the *outside world* so that additional
    packages can be downloaded
-   you need to have installed ``git`` so that this repository can be
    clones to the designated *control machine* in your cluster.

.. _here: https://docs.okd.io/3.11/install/prerequisites.html

The my_machines Deployment Section
==================================

You need to provide a ``my_machines`` section in the deployment configuration.
The values you provide are used to populate the rendered OKD inventory file,
an automatic step when using Terraform. You essentially just have to provide
the values that terraform would normally provide when it creates the machines.

Instructions for how to do this can be found in the reference configuration
``deployments/compact-aws-frankfurt-3-11.yaml``.

Running create.py
=================

You need to have cloned this repository onto your *control machine*
(essentially the Bastion or one of your Masters) and have followed the
basic setup instructions detailed in the :doc:`getting-started` section.

Run ``create.py`` from the root of the cloned project using the
using a deployment with a correctly populates ``my_machines`` section.
This will generate an OKD Ansible inventory file for your cluster avoiding
the terraform stage of the deployment::

    $ cd okd-orchestrator
    $ ./create.py --create my-deployment

Now use the ``--okd`` option to install the OKD container runtime::

    $ ./create.py --okd
