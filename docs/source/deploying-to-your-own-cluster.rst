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
which would be part of the automatic step that would be managed by `Terraform`_
when using the Orchestrator to create the cluster. As *you* have created the
machines then you provide the values that Terraform would have provided.

Instructions for populating the configuration can be found in the reference
configuration file (``deployments/compact-aws-frankfurt-3-11``). Just look for
the annotated ``my_machines`` section in the configuration file.

.. _terraform: https://www.terraform.io

Deploying OKD
=============

With a ``my_machines`` section populated, the cluster setup is like any
other...

-   Craft a suitable ``setenv.sh`` and ``source`` it
-   Run ``create.py`` as normal using ``--cluster`` from your development
    environment/desktop. Then hop onto the *Bastion* and run it again using the
    ``--okd`` option

From here just follow the instructions in the :doc:`creating-your-cluster`
section.

If you have your own bastion you might want to use the OKD Orchestrator in
*just plan* mode so that you can render the OKD inventory file
based on your ``my_machines`` definition without resorting to configuring
the Bastion. If so you will need to copy the generated ``inventory.yaml`` file
to the Bastion for subsequent manual deployment of the OK platform. You
can run *just plan* by adding ``--just-plan`` to ``create.py``.
