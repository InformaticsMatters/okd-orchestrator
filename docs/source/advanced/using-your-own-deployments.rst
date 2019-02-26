##########################
Using Your Own Deployments
##########################

The **Deployments** (the high-level configuration files that define your
cluster) are normally located in the project's ``deployments`` directory.
You can place your own deployments in this directory but you will need to
_fork_ this repository if you then want to commit them to revision control.
For various reasons you might not want to fork this repository, preferring
instead to work with a clone and managing your deployments in your own project.

You can maintain your deployments in a separate project and use the
orchestrator from this project, either from within Docker or from the
command-line.

To use deployments from your own project you just need to set the
``TF_VAR_deployments_directory`` environment variable to match the path
to your own deployments directory before entering the container [#f1]_.

Normally you do not need to run ``source provider-env/setenv.sh`` as the
container takes care of this for you. But, if you manage your own
deployments directory you must either run ``source provider-env/setenv.sh``
*before* running ``./okdo-start.sh`` or set ``TF_VAR_deployments_directory``::

    $ source provider-env/setenv.sh
    $ ./okdo-start.sh

.. rubric:: Footnotes

.. [#f1] If the variable is set, the ``okdo-start.sh`` script that starts the
         Docker container will automatically mount your deployments directory
         as a *volume* so the path is equally valid inside the container as it
         is outside
