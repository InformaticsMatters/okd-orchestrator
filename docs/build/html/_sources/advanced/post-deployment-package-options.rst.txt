###############################
Post-Deployment Package Options
###############################

When the OKD software has been deployed the orchestrator allows you
to conveniently run additional `Ansible`_ playbooks that are designed to
install extra software.

A built-in post-OKD playbook exists, called ``acme-controller``. Ths
creates an OKD project and installs a utility to automatically
provision certificates using ACME protocol and manage their lifecycle.

.. _ansible: https://www.ansible.com

**************************
Running post-OKD playbooks
**************************

To execute a post-OKD installation playbook you simply need to name it in
your configuration [#f1]_. Essentially, you just need to add the name of the
playbook in the ``post_okd`` list::

    okd:
      post_okd:
      - play: acme-controller

********************
Adding new playbooks
********************

Pre-defined Variables
=====================

Special variables are passed to post-OKD playbooks, so adding your own
OKD applications that can operate the master API after the OKD software is
installed is easy. The playbooks are provided with the following variables by
the ``create`` utility: -

-   ``okd_api_hostname``. Essentially the https location of the master's API.
-   ``okd_admin_password``. The OKD administration user password.
    (the user is ``admin``)
-   ``okd_deployment``. The name of deployment.

If a developer password has been supplied the following variable is defined: -

-   ``okd_developer_password``. The OKD developer user password
    (the user is ``developer``)

If a template project has been created you also get: -

-   ``template_namespace``. The project/namespace of the template project

Adding plays
============

To add an ansible playbook you need to: -

#.  Create a directory for your playbook in the orchestrator's
    ``ansible/post-okd`` directory
#.  Your playbook must have a ``deploy.yaml``. It is this playbook that the
    ``create`` utility will call. The deploy playbook will be provided
    with the variables described above.

If you've added a ``my-play/deploy.yaml`` playbook you can add it the the list
of post-OKD plays that are run at the end of your deployment by adding it to
the ``post_okd`` list in your configuration::

      okd:
        post_okd:
        - play: acme-controller
        - play: my-play

You can organise your playbook into roles and add a directory to
``ansible/post-okd/roles`` if you wish, or just provide a playbook.
Regardless, you have to define a ``deploy.yaml`` to act as the entry
point of your playbook.

.. rubric:: Footnotes

.. [#f1] For up-to-date instructions refer to the built-in
         ``compact-aws-frankfurt-3-11`` configuration, which contains
         significant embedded documentation
