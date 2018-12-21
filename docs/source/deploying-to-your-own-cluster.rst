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

Before you can use the orchestrator on your own cluster the cluster instances
must satisfy the **system and environment requirements** defined in the
official OKD documentation. For v3.11 this can be found `here`_.

Additionally, in case it's not obvious...

-   Your cluster must have access to the *outside world* so that additional
    packages can be downloaded
-   You must be able to SSH to the designated Bastion from your development
    machine (i.e. where you have a copy of the orchestrator).
-   You need to have installed ``git`` so that this repository can be
    cloned to the designated *control machine* in your cluster.

.. _here: https://docs.okd.io/3.11/install/prerequisites.html

Populating my_machines
======================

In order to deploy OKD to you cluster the orchestrator has to know about
the machines that will be involved. This is achieved by adding a
``my_machines`` section to your deployment configuration.

The values you provide are used to populate the rendered OKD inventory file,
an automatic step when using Terraform. You essentially provide the values
that terraform would provide if *it* were to create the machines.

Instructions for how to do this can be found in the reference configuration
``deployments/compact-aws-frankfurt-3-11.yaml``. Look for the annotated
``my_machines`` section in the file.

Populating my_machines
======================

With a ``my_machines`` section populatyed the cluster setup is like any
other...

-   Setup a ``setenv.sh``
-   Run ``create.py`` as normal using ``--cluster``, hop onto the *Bastion*
    and run it again using the ``--okd`` option
