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

If you haven't done so already you need to set the password that will be
assigned to the OpenShift **admin** account the orchestrator creates. Choose
a suitable value and set it in your ``setenv.sh`` script, replacing
the value for::

    TF_VAR_okd_admin_password

Now you can start and enter the OKD orchestration container
with the convenient start script in the root of the project::

    $ ./okdo-start.sh

To create the cluster (bastion, network and OpenShift/OKD nodes)
run the ``create.py`` utility using the ``--cluster`` option::

    $ ./create.py --cluster
    +---------------------------------------------------+
    | Simple AWS Deployment (OpenShift 3.9) [Frankfurt] |
    +---------------------------------------------------+
    Enter "okay" to CREATE the Cluster:

If there's more than one deployment configuration in the project
you'll need to name the one you want to create, i.e.::

    ./create.py --cluster simple-aws-frankfurt-3.9
    +---------------------------------------------------+
    | Simple AWS Deployment (OpenShift 3.9) [Frankfurt] |
    +---------------------------------------------------+
    Enter "okay" to CREATE the Cluster:

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
``create.py`` again, this time using the ``--okd`` command-line option,
to install the OpenShift/OKD element of the cluster::

    $ cd okd-orchestrator
    $ ./create.py --okd
    +---------------------------------------------------+
    | Simple AWS Deployment (OpenShift 3.9) [Frankfurt] |
    +---------------------------------------------------+
    Enter "go" to INSTALL OKD:

Acknowledge the warning prompt to begin the installation.

If there's more than one deployment configuration in your project you will
need to name the configuration to use for the OpenShift installation.

.. epigraph::

    You do not need to set any environment variables on the bastion or
    use ``ssh-agent`` as it and your variables are automatically configured
    on the Bastion as part of the cluster creation step.

    It may take a significant period fo time to install OpenShift, depending on
    the configuration (i.e., the size of the cluster and whether logging,
    metrics, gluster etc. are also being installed). You should allow around
    30 minutes for a typical small configuration.

    The simple AWS example, which does not deploy logging, metrics or
    GlusterFS, should be ready after approximately **14 minutes**.

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

You're connected to the bastion, when the cluster's complete you can exit
and return  to the orchestration container::

    $ exit

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
