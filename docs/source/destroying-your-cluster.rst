####################
Destroying a Cluster
####################

Destroying (tearing down) a Cluster, its network and Bastion is a simple
process, handled by the orchestrator.

.. epigraph::

   Tearing down a cluster relies on ``terraform`` **state files** that were
   generated when the cluster was created. These are located in the
   orchestrator's ``terraform`` directory. If you've lost these files
   or are running the orchestrator form another host you will not be able to
   destroy the cluster.

If you're not in the orchestrator container then, from the working copy
of the ``okd-orchestrator`` clone that you used to create your cluster,
start and enter the orchestrator::

    $ ./okdo-start.sh

You're in the container as the built-in ``okdo`` user. To destroy the
cluster you just need to set your environment variables and run
``destroy.py``, naming the deployment configuration that defines the cluster
you wish to delete. For the example AWS cluster this would require the
following commands::

    $ cd okd-orchestrator
    $ ./destroy.py simple-aws-frankfurt-3-9
    +---------------------------------------------------+
    | Simple AWS Deployment (OpenShift 3.9) [Frankfurt] |
    +---------------------------------------------------+

    CAUTION You are about to destroy the cluster.
    ------- Are you sure you want to do this?

    Enter "ok" to DESTROY this deployment:

Acknowledge the warning to destroy the cluster.

Destruction is generally very fast. ``destroy.py``, after seeking confirmation,
simply relies on the underlying **Terraform** utility, which rapidly deletes
all of the objects that were originally created.
