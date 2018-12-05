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

.. epigraph::

   If you've made any local changes to the Orchestrator files you should
   commit them to revision control now. Your repository is cloned to the
   Bastion as the cluster ius created so checking them in now means it will
   get an *up to date* copy of your files.

If you're not already in the orchestration container you can start and enter
it with the convenient start script in the root of the project::

    $ ./orc-start.sh

If you haven't done so already you need to set the password that will be
assigned to the OpenShift **admin** account the orchestrator creates. Choose
a suitable value and set it in your ``setenv.sh`` script, replacing
the value for::

    TF_VAR_okd_admin_password

If the SSH key-pair you are using (named in your ``setenv.sh``) is not
the default (i.e. `id_rsa`) then you will need to run `ssh-agent` in the
container to allow some stages of orchestration to run without prompting::

    $ eval $(ssh-agent)
    $ ssh-add ~/.ssh/aws-keypair

Now, to create the cluster (bastion, network and OpenShift nodes)
set your environment variables and run the ``create.py`` utility using
the ``--cluster`` option::

    $ source provider-env/setenv.sh
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

Creating the Cluster will take a few minutes.

When complete the public IP address of the bastion (and the master and
infrastructure nodes) will be presented to you. You should see a
``terraform output`` banner with the relevant addresses printed below.
The address of the bastion is needed for the next step::

    +----------------------+
    | terraform output ... |
    +----------------------+
    bastion_ip = 18.185.149.91
    openshift_infra_ip = 35.157.131.211
    openshift_master_ip = 18.184.254.113

Installing OpenShift
====================

The cluster creation step places a clone of your orchestrator project is in the
Bastion's home directory. Installation of OpenShift takes place from there.

You can ``ssh`` to the Bastion from within the orchestration container you're
currently in using the public IP address of the bastion presented to you in
the previous step.

``ssh`` to the Bastion using the built-in ``centos`` account. for the above
you'd run::

    $ ssh centos@18.185.149.91

From the Bastion you simply move to the cloned orchestrator directory and run
``create.py`` again, this time using the ``--openshift`` command-line option,
to install the OpenShift element of the cluster::

    $ cd okd-orchestrator
    $ ./create.py --openshift
    +---------------------------------------------------+
    | Simple AWS Deployment (OpenShift 3.9) [Frankfurt] |
    +---------------------------------------------------+
    Enter "go" to INSTALL OpenShift:

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

    The basic AWS example will be finished after approximately **14 minutes**.

Once ``create.py`` is complete, your OKD Cluster should be installed with a
console available on the IP address or domain name that's routed to the Master
node, i.e. the address used for the deployment's ``cluster.public_hostname`` or
via the IP address presented to you when the cluster was created.

You're connected to the bastion, when the cluster's complete you can exit
and return  to the orchestration container::

    $ exit

Using the terraform output from the cluster creation stage you
should see the OpenShift Master IP address. In the above example you'll
find the master's console at::

    https://18.184.254.113

You should be able to login as ``admin`` using the password you used
in your ``setenv.sh`` script.

    The Bastion is no longer needed once your cluster has been deployed and
    so you can **stop** it, if your cloud provider provides this functionality.
    This will reduce your costs. **Do not** delete the Bastion or any other
    cluster object. You **must** destroy the Cluster using the orchestrator.
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
