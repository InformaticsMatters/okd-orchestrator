##################
Creating a Cluster
##################

.. highlight:: none

Orchestrating a cluster currently consists of two steps: orchestrating the
**Bastion** and then, from there, orchestrating the OpenShift OKD **Cluster**
itself.

Creating the Bastion
====================

    If you've made any local changes to the Orchestrator files
    you should commit them to revision control. The repository is
    cloned to the bastion so checking them in now means it will get
    an *up to date* copy of your files.

The **Bastion** is a small machine that allows you to create the cluster from
within an isolated network. With a Bastion you can create and access compute
nodes that would normally not have any visibility outside the network they're
on.

    For a given cloud provider you only need to create a single Bastion.
    From there you should be able to manage a number of individual OKD
    clusters.   As long as you're happy that they share the same network,
    which in AWS terms, means a common ``VPC`` and ``SubNet``.

To create the Bastion, from the root of the project run the ``create.py``
utility::

    ./create.py --bastion

If there's more than one deployment configuration in the project
you'll need to name thewone to use, e.g.::

    ./create.py simple-aws-frankfurt-3.9 --bastion


You'll be prompted to confirm the actions before the creation process
continues.

Creating the Bastion will take a few minutes.

Once created you can SSH to the Bastion n order to continue with the second
step, creating the **Cluster**. The address of the Bastion should be available
in the final steps of the Ansible playbook used to create it::

    PLAY RECAP ****************************************************************
    35.158.128.232             : ok=16   changed=9    unreachable=0    failed=0

You will need to use the key-pair used in the deployment. If you're deploying
the *simple AWS* example this is likely to be named ``aws-keypair``.

SSH to the Bastion::

    ssh -i ~/.ssh/aws-keypair centos@35.158.128.232

Creating the Cluster
====================

You will find a clone of the orchestrator in the Bastion user's home directory.
To create the **Cluster** navigate to the orchestrator clone's directory and
run ``create.py``::

    cd okd-orchestrator
    ./create.py

If there's more than one deployment configuration in the project
you'll need to name the one you want to use, e.g.::

    ./create.py simple-aws-frankfurt-3.9

Once it's complete, your OKD Cluster should be installed, with a console
available on the IP address or domain name that's routed to the Master node,
i.e. the address used for the deployment's ``cluster.public_hostname``.

    The Bastion is no longer needed once your cluster has been deployed and
    so you can **stop** it, if your cloud provider provides this functionality.
    This will reduce your costs. **Do not** delete the Bastion, you may need it
    to manage the cluster and you will need it to tear it down. So feel free to
    **stop** the instance, but **do not** delete it.
