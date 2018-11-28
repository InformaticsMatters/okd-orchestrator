####################
Destroying a Cluster
####################

.. highlight:: none

Destruction (tearing down) a Cluster and its Bastion involves two separate
steps. You must first destroy any and all Clusters managed by a Bastion
*before* you destroy the Bastion that you use to manage them.

At the moment the destruction process cannot determine whether
your bastion contains any deployed/active Clusters so it's up to you to
remember to destroy the Bastion's Clusters before you Destroy the Bastion.

If you destroy the bastion before destroying its clusters you are likely to
leave a large number of cloud objects deployed that will be difficult and
painstaking to remove manually.

Destroying a Cluster
====================

From the Bastion's ``okd-orchestrator`` clone you can destroy a cluster
after providing its name. From a Bastion SSH session you can destroy the
*simple AWS* example with the following commands::

    cd okd-orchestrator
    ./destroy.py simple-aws-frankfurt-3-9

Destruction is relatively fast. The utility simply relies on the underlying
**Terraform** utility, which quickly deletes all of the objects that were
originally created.

Destroying a Bastion
====================

Once the Bastion's clusters have been torn down you are free to delete it.
But be sure that all the clusters managed by the bastion have been
deleted before you consider deleting the Bastion.

Removal of the Bastion will remove all cluster information and the network
created to manage them.

From the original host machine you used to create the Bastion, navigate to the
OKD project clone and run ``destroy.py``. For example, if you checked out the
project in your workstation's home directory simply navigate there and run it::

    cd $HOME/okd-orchestrator
    ./destroy.py --bastion

As it's the Bastion you're destroying you are presented with a cautionary
reminder before you're able to continue.
