##################
Creating a Cluster
##################

.. highlight:: none

Orchestration currently consists of two steps: orchestrating the
**Cluster** and then installing the OpenShift **OKD software**.
All of this can be accomplished from within the orchestrator's Docker
container.

Creating the Cluster
====================

If you have a pre-existing cluster you should follow the steps described in
the :doc:`deploying-to-your-own-cluster` section.

If you haven't done so already you need to set the password that will be
assigned to the OpenShift **admin** account the orchestrator creates. Choose
a suitable value and set it in your ``setenv.sh`` script, replacing
the value for::

    TF_VAR_okd_admin_password

The default value in the template is valid but it isn't particularly secure!

>   You can also create a less-privileged ``developer`` user by
    providing a value for ``TF_VAR_okd_developer_password``.
    This is optional, you can leave it blank to avoid creating a *developer*.

Now you can start and enter the OKD orchestration container
with the convenient start script in the root of the project::

    $ ./okdo-start.sh

To create the cluster (bastion, network and OpenShift/OKD nodes)
run the ``create.py`` utility using the ``--cluster`` option::

    $ ./create.py --cluster

    +-----------------------------------------------+
    | Compact AWS Deployment (OKD 3.11) [Frankfurt] |
    +-----------------------------------------------+
    Enter "yes" to CREATE the Cluster:

If there's more than one deployment configuration in the project
you'll need to name the one you want to create, i.e.::

    $ ./create.py --cluster compact-aws-frankfurt-3.11

    +-----------------------------------------------+
    | Compact AWS Deployment (OKD 3.11) [Frankfurt] |
    +-----------------------------------------------+
    Enter "yes" to CREATE the Cluster:

Respond to the warning prompt to confirm the action and the creation process
will begin.

The simple AWS example cluster should be ready after approximately
**4 minutes**.

When complete the public IP address of the bastion will be presented to you.
You should see a ``terraform output`` banner with the relevant address exposed.
The address of the bastion is needed for the next step::

    +----------------------+
    | terraform output ... |
    +----------------------+
    bastion_ip = 18.185.149.91


Installing OpenShift/OKD
========================

The prior cluster creation step places a copy of key parts of your orchestrator
project in the Bastion's home directory. Installation of OpenShift/OKD takes
place from there.

You can ``ssh`` to the Bastion from within the orchestration container you're
currently in using the public IP address of the bastion presented to you in
the previous step::

    $ ssh centos@18.185.149.91

From the Bastion you simply move to the cloned orchestrator directory and run
``create.py``.,  You don't need to provide any options (although you
can use ``--okd``) as there's only one deployment configuration copied to it -
the one you used to create the cluster.

To install OpenShift/OKD::

    $ cd okd-orchestrator
    $ ./create.py

    +-----------------------------------------------+
    | Compact AWS Deployment (OKD 3.11) [Frankfurt] |
    +-----------------------------------------------+
    Enter "yes" to INSTALL OpenShift/OKD:

Acknowledge the warning prompt to begin the installation.

.. epigraph::

    You do not need to set any environment variables on the bastion or
    use ``ssh-agent`` as it and your variables are automatically configured
    on the Bastion as part of the cluster creation step.

It may take a significant period of time to install OpenShift, depending on
the configuration (i.e., the size of the cluster and whether logging,
metrics, gluster etc. are also being installed). You should allow up to
30 minutes for a typical small configuration.

The compact AWS example, which deploys metrics and prometheus,
should be ready after approximately **16 minutes**.

Once ``create.py`` is complete, your OKD Cluster should be installed with a
console available on the IP address or domain name that's routed to the Master
node, i.e. the address used for the deployment's ``cluster.public_hostname`` or
via the IP address presented to you when the cluster was created.

You should be able to login to the OpenShift/OKD console as ``admin``
using the password you supplied in your ``setenv.sh`` script.

    If you are using a Bastion it is no longer needed once your cluster has
    been deployed and so you can **stop** it, if your cloud provider provides
    this functionality and it likely to help will reduce your cluster costs.
    But **do not** *delete* the Bastion or any other cluster object.
    You **must** destroy the Cluster using the orchestrator.
    So feel free to **stop** the instance, but **do not** delete it.

When you're finished with the cluster you can follow the
:doc:`destroying-your-cluster` guide to delete it.

Cluster State Files
===================

The orchestrator state for each cluster is stored in files that are generated
and managed by the execution of **Terraform**, a tool used to create the
cluster objects. These files are located in the orchestrator’s ``terraform``
directory and their presence is crucial. **Do not** delete the project or
any files on the terraform directory until you have destroyed the clusters
created from it.

Although remote state storage and state locking is possible,
for this release, the orchestrator does not support such a feature.

For now, remember that your orchestrator directory contains and relies on
a number of dynamic files not under revision control.
