###########################
Creating Post-OKD Playbooks
###########################

.. highlight:: none

The orchestrator is able to  execute Ansible playbooks once the OKD software
has been installed. These playbooks are named in your deployment's
``okd.post_okd`` section. Each playbook named here is expected to exist in
the project's ``ansible/post-okd`` directory.

In order to be recognised by the orchestrator the playbook must comply with
the following requirements: -

#.  Provide the playbook file
    ``ansible/post-okd/playbooks/<playbook-name>/deploy.yaml``
#.  Accept OKD URL and administrator details in the variables
    ``okd_api_hostname``, ``okd_admin`` and ``okd_admin_password``
#.  Accept OKD deployment name the variable ``okd_deployment``
#.  Ideally it will be implemented using an Ansible **Role**, with the Role
    located in ``ansible/post-okd/roles/<playbook-name>``

If you follow the above rules the ``deploy.yaml`` playbook for a ``my-app``
playbook, at its simplest, will look like this::

    ---

    - hosts: cli-node

      roles:
      - my-app


And can then be added to your deployment with the following ``post_okd``
section::

    okd:
      post_okd:
      - play: my-app

The playbook should use the ``oc`` command set and should expect the Master
API to be available at ``okd_api_hostname``.

Exposing Playbook Variables
===========================

If you need to expose variables in your playbook you can set values for them
in your deployment configuration. It's best practice, when using Roles, to
define your Role variables in your Role's ``defaults/main.yaml`` file.
This way users can quickly see any variables that are available by inspecting
one file.

Once you have defined the variables, setting them is as simple as adding
names and values in your deployment configuration. In the above example,
if your ``my-app`` playbook exposes the variables ``offset`` and ``gain``,
values for them are defined using a ``vars`` list in the ``post_okd`` section::

    okd:
      post_okd:
      - play: my-app
        vars:
        - offset=1.7
        - gain=6

.. epigraph::

   The variables are passed to your playbook by the orchestrator using the
   ``--extra-vars`` command-line option.
